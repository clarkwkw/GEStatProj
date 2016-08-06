# Import some settings for testing
bfSettingDF <- read.csv("correlationVar.csv", header = TRUE, sep = ",", check.names = FALSE, stringsAsFactors = FALSE)
grouping <- getFullRows(bfSettingDF["Grouping"])
questions <- getFullRows(bfSettingDF["Var"])

# Initialize a data structure for storing result
SimpleTuple <- setRefClass("SimpleTuple",
                           fields = list(col1 = "character", col2 = "character", group = "character", correlation = "numeric", numberOfRecord = "numeric")
)


generateCor <- function(grouping, questions, resultLimit, minRecord, isPositive, isReadable = FALSE){
  # Import priority queue for processing tuples
  source("dataStructure/priorityQueue.R")
  
  # Initialize a function for comparing correlation
  SimpleTupleCmp <- function(a, b){
    return (a$correlation < b$correlation)
  }
  
  # A function specifies how to format the output to semi-readable manner
  toReadable <- function(x){
    return (paste(x$group, "=", round(x$correlation, digits = 2), "; "))
  }
  
  # Generate combination of questions for calculating correlation
  combination <- combn(questions, 2)
  
  # Divide the records into distinct subsets and calculate correlation for all combination of questions
  # ** Since the number of grouping question is variable, it needs to be recursively subsetted in another function
  tuples <- subsetNCalculate(rawdata, grouping, combination, minRecord)
  
  # After the above function call, correaltion of all groups under all combination of question is calculated and saved in tuples list
  
  # Create an empty matrix for processing the tuples
  resultMatrix <- matrix(list(), nrow = length(questions), ncol = length(questions))
  rownames(resultMatrix) <- questions
  colnames(resultMatrix) <- questions
  
  # Put all tuples into corresponding priority queue in the matrix
  lapply(tuples, function(x){
    
    # If the corresponding priority queue does not exist, create one
    if(is.null(resultMatrix[[x$col1, x$col2]])){
      resultMatrix[[x$col1, x$col2]] <<- PriorityQueue$new("SimpleTuple", customComparator = SimpleTupleCmp)
    }
    
    # If it we need to find out the smallest correlation, we need to negate all correlation, so that the same algorithm can be reused
    if(!isPositive){
      x$correlation <- x$correlation * -1
    }
    
    # The tuple will be added to the priority queue of the corresponding question, if
    #   1. the number of tuples in the queue is less than resultLimit, OR
    #   2. the correlation of new tuple is larger than the smallest tuple in the queue
    if(resultMatrix[[x$col1, x$col2]]$size < resultLimit || resultMatrix[[x$col1, x$col2]]$front()$correlation < x$correlation){
      resultMatrix[[x$col1, x$col2]]$insert(x)
    }
    
    # If there is any excess tuple, remove it
    if(resultMatrix[[x$col1, x$col2]]$size > resultLimit){
      resultMatrix[[x$col1, x$col2]]$pop()
    }
  })
  
  # Convert priority queue in each cell into a simple sorted list/ readable context
  result <- apply(resultMatrix, 2, FUN = function(x){
    result <- lapply(x, function(y){
      # If there is no priority created, it is either due to:
      # 1. it is in the lower triangler matrix
      # 2. there is no grouping which has "valid" correlation coefficient
      # In both cases, they can be presented as "NULL"
      if(class(y) == "NULL"){
        return(NULL)
      }
      
      # Convert priority queue into list
      tmpResult<-y$toList()
      
      # Negate the correlation back to original one if it is negated before
      if(!isPositive){
        sapply(tmpResult, function(x){
          x$correlation<-x$correlation * -1
          return(x)
        })
      }
      
      if(isReadable == FALSE){
        return(tmpResult)
      }else{
        
        #If isReadable is TRUE, further convert it into readable context by toReadable function
        return(do.call(paste, lapply(tmpResult, FUN = toReadable)))
      }
    })

    return (result)
  })
  
  result<-t(do.call(rbind, result))
  return(result)
}




# This function is a kind of utility function, not intended to be directly used,
# which can subset a dataframe according to columns specified by grouping
# rawDF: a dataframe
# grouping: a vector containing column names for classifying different groups of records
# minRecord: an integer, if the no. of record of the group is less than minRecord, the group will be ignored
# identifier: a zero-length string on default, used to store the identity of different groups during recursion 
subsetNCalculate <- function(rawDF, grouping, combination, minRecord, identifier = ""){
  # Check for minRecord condition
  if(nrow(rawDF) < minRecord)return()
  
  # If the subset procedure is done, calculate correlation coefficient
  if(length(grouping) == 0){
    
    # Correlation is calculated for each combination of question
    result <- apply(combination, 2, function(x){

      tmpCor <- as.numeric(cor(rawDF[x[1]], rawDF[x[2]], use = "na.or.complete", method = "pearson"))
      
      if(!is.na(tmpCor)){
        
        # Result is packed in a "SimpleTuple"
        tmpTuple <- SimpleTuple$new(col1 = x[1], col2 = x[2], group = identifier, correlation = tmpCor, numberOfRecord = nrow(rawDF))
        return (tmpTuple)
      }
    })
    return (result)
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
    newIdentifier <-  paste(currentGrouping, ":", x)
    if(nchar(identifier)>0){
      newIdentifier <- paste(identifier, "&", newIdentifier)
    }
    
    # Recursively subset the records and find out the correlation
    return(subsetNCalculate(tmpDF, grouping[-length(grouping)], combination, minRecord, newIdentifier))
  })
  
  return (unlist(result))
}