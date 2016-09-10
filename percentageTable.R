# Initialize a data structure for storing result
# identityMatrix: a nx2 matrix, identifies the subset, where n is the number of grouping question
# resultDF: a data frame of this format:
# ---------------
# | Var1 | Freq |
# ---------------
# |  0%  |  10  |
# ---------------
# |10-20%|  20  |
# ---------------
# | ........... |
# ---------------
# which means there are 10 records who chose 0%, while 20 records for 10-20%, etc

PercentageTuple <- setRefClass("PercentageTuple",
                           fields = list(identityMatrix = "matrix", resultDF = "data.frame")
)

# This function finds out the distribution of different groups of participants over different options of a question
# rawDf: a dataframe
# question: a character variable, which contains the name of that question
# groupings: a vector of character, which contains the name of questions that used to seperate records into different groups
# toGraph: a boolean value, if it is TRUE, a graph will also be generated
# toPercentage: a boolean value, if it is TRUE, percentage will be displayed, otherwise, record count will be displayed
generatePercentages <- function(rawDF, question, groupings, toGraph = FALSE, toPercentage = TRUE){
  
  # orderedOptions: a vector of character extracted from formatDF, which contains the options of questions in a particular order
  orderedOptions <- orderedOptions <- formatDF[[question]]
  if(!is.null(orderedOptions)){
    orderedOptions <- orderedOptions[orderedOptions != ""]
  }
  
  # A function which converts PercentageTuple's "indentity" matrix into a readable format
  toReadable <- function(x){
    result <- paste(paste(x$identityMatrix[1, ], x$identityMatrix[2, ], sep = "=", collapse = "&"), collapse = ",")
  }
  
  # Find out the possible answers of the question
  possibleAns <- sort(unique(rawDF[is.na(rawDF[[question]]) == FALSE, question]))
  # Divide records into disjoint subsets and count the number of records for each answers
  tuples <- subsetNCalculate(rawDF, question, groupings)

  # Initialize a data frame for storing data for the graph
  graphDF <- matrix(NA, nrow = length(tuples)*length(possibleAns), ncol = 4)
  colnames(graphDF) <- c("options", "groups", "percentage", "order")
  graphDF <- as.data.frame(graphDF, check.names = FALSE)
  
  # Initialize a data frame for storing return value
  resultDF <- matrix(NA, nrow = length(tuples), ncol = length(possibleAns)+1)
  colnames(resultDF) <- c("group", possibleAns)
  resultDF <- as.data.frame(resultDF, check.names = FALSE)
  
  counter <- 1
  counterForGroup <- 1
  
  # Loop for each tuple obtained
  lapply(tuples, FUN = function(x){
    
    # Sum up the total number of record of this group
    total <- sum(x$resultDF[["Freq"]])
    # Retrieve group name
    groupName <- toReadable(x)
    resultDF[counterForGroup, 1] <<- groupName
    
    # Loop for each row inside tuple$resultDF  
    by(x$resultDF, 1:nrow(x$resultDF), FUN = function(y){
      optionName <- levels(droplevels(y[["Var1"]]))
      
      # Put the details into graphDF
      graphDF[counter, "groups"] <<- groupName
      graphDF[counter, "options"] <<- optionName
      if(toPercentage){
        graphDF[counter, "percentage"] <<- round(y[["Freq"]]/total*100, digits = 2)
        
        # Put them in resultDF also
        resultDF[counterForGroup, levels(droplevels(y[["Var1"]]))] <<- round(y[["Freq"]]/total*100, digits = 2)
      }else{
        graphDF[counter, "percentage"] <<- y[["Freq"]]
        
        resultDF[counterForGroup, levels(droplevels(y[["Var1"]]))] <<- y[["Freq"]]
      }
      
      if(!is.null(orderedOptions)){
        graphDF[counter, "order"] <<- which(orderedOptions == optionName)
      }
      
      
      
      counter <<- counter + 1
    })
    
    counterForGroup <<- counterForGroup + 1
  })
  
  # Sometimes, some options are not chosen by anyone of the group, the size of graphDF needs to be shrinken
  if(counter <= nrow(graphDF)){
    graphDF <- graphDF[-c(counter:nrow(graphDF)),]
  }
  
  # Plot the graph if toGraph is TRUE
  if(toGraph){
    
    # Import library
    library(ggplot2)
    library(scales)
    # Set x, y axis, values and the style of the graph
    graph <- NA
    if(is.null(orderedOptions)){
      graph <- ggplot(graphDF, aes(x = groups, y = percentage,fill = options, label), environment = environment())
    }else{
      graph <- ggplot(graphDF[order(graphDF$order, decreasing = TRUE), ], aes(x = groups, y = percentage,fill = factor(options, levels = orderedOptions), label), environment = environment()) 
        
    }
    graph <- graph +
      geom_bar(position = "fill",stat = "identity", aes(y = percentage, ymax = percentage)) +
      geom_text(aes(label = ifelse(percentage < .05, NA, percentage), ymax = percentage), position = position_fill()) +
      scale_y_continuous(labels = percent_format()) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      ggtitle(paste(question, "By Group", sep = " ")) +
      labs(x = "Groupings", y = "Percentage") +
      guides(fill=guide_legend(title="Options"))
    
    print(graph)
  }
  return(resultDF)

}

# This function recursively subsets the records and counts the number of records of each option in question
subsetNCalculate <- function(rawDF, question, grouping, identifier){
  
  # If the subset procedure is done, find out the distribution
  if(length(grouping) == 0){
    
    tmpTuple <- PercentageTuple$new(identityMatrix = identifier, resultDF = as.data.frame(table(rawDF[[question]])))
    return(tmpTuple)
    
  }
  
  # Initialize a matrix for identifying different subsets
  if(missing(identifier)){
    identifier <- matrix(character(), nrow = 2, ncol = length(grouping))
    colnames(identifier) <- grouping
    identifier[1, ] <-grouping 
  }
  
  # If the subset procedure is not done, start from the last grouping question
  currentGrouping <- grouping[length(grouping)]
  tmpDF <- rawDF[!is.na(rawDF[currentGrouping]), ]
  
  # Find out the possible answers in the grouping question, e.g. if grouping is "sex", it should find out "F" and "M"
  possibleGPs <- unique(tmpDF[, currentGrouping])
  
  
  # For each group, subset the records and continue on other grouping questions
  result<-sapply(possibleGPs, function(x){
    
    # Subset records
    tmpDF <- tmpDF[tmpDF[currentGrouping] == x, ]
    
    # Specify the identity of the group
    identifier[[2, currentGrouping]] <-  x
    
    
    # Recursively subset the records and find out the correlation
    return(subsetNCalculate(tmpDF, question, grouping[-length(grouping)], identifier))
  })
  
  return (unlist(result))
}