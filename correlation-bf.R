#This function finds correlated question by Brute force search
#Usage: Import & Run inputCSV.R first, and then run this script

#Import some sample setting (you can also create your own setting)
bfSettingDF <- read.csv("correlationVar.csv", header = TRUE, sep = ",", check.names = FALSE, stringsAsFactors = FALSE)
grouping <- getFullRows(bfSettingDF["Grouping"])
questions <- getFullRows(bfSettingDF["Var"])


#This function can search for highly correlated questions based on different grouping
#Grouping is a vector of column names, where these columns are used to identify participants' identity
#Questions is a vector of column names, where these columns are questions that may be correlated
#ResultLimit is a numeric value which limits the maximum number of related question that the function should return
#MinRecord is a numeric value, if number of records of a group is less than minRecord, that group will be ignored
#IsPositive is a boolean value, which indicates where the function ranks the correlations from 1 to -1 (TRUE) or -1 to 1 (FALSE) 

#Example: grouping <- c("Faculty", "No Science")
#         questions <- c("Q1 Change", "Q2 Change", "Q3 Change")
#         generateCor(grouping, questions, 10, 30, TRUE)

#The function will exhaust all combination of questions
#i.e. Q1 Change - Q2 Change, Q1 Change - Q3 Change, Q2 Change - Q3 Change

#Under each combination, the function will exhaust all groupings and its groups to calulate its correlation
#i.e. Q1 Change - Q2 Change (Faculty = ART), Q1 Change - Q2 Change (Faculty = MED), Q1 Change - Q2 Change (Faculty = ERG),...
#     Q1 Change - Q2 Change (No Science = 0), Q1 Change - Q2 Change (No Science = 1), Q1 Change - Q2 Change (No Science = 2),...

#If the number of valid records belong to the grouping is less than 30, the correlation will be ignored
#At the end, the 10 highest correlation combination will be returned
generateCor <- function(grouping, questions, resultLimit, minRecord, isPositive){

  source("dataStructure/priorityQueue.R")
  #Initialize a data structure for storing result
  Tuple <- setRefClass("Tuple",
                       fields = list(col1 = "character", col2 = "character", groupCol = "character", group = "character", correlation = "numeric", numberOfRecord = "numeric")
  )
  #Initialize a function for comparing correlation
  TupleCmp <- function(a, b){
    return (a$correlation < b$correlation)
  }

  #Initialize a priority queue for storing correlations
  resultQ <- PriorityQueue$new("Tuple", customComparator = TupleCmp)
  
  #Generate combination of questions for calculating correlation
  combination <- combn(questions, 2)
  
  #Loop for each combination of questions
  result <- apply(combination, 2, function(x){
    
    #Extract those related columns from rawdata
    dfWithTwoCols <- rawdata[, x]
    
    #Loop for each grouping question 
    result <- sapply(grouping, function(y){
      
      possibleGPs <- unique(rawdata[!is.na(rawdata[y]), y])
      
      #Try to calulate correlation for individual group
      result <- sapply(possibleGPs, function(z){
        
        #Only records belong to the corresponding group is considered
        dfWithTwoColsFiltered <- dfWithTwoCols[!is.na(rawdata[y]) & rawdata[y] == z,]
        
        if(nrow(dfWithTwoColsFiltered) >= minRecord){
          #Calculate correlation
          tmpCor <- cor(dfWithTwoColsFiltered[x[1]], dfWithTwoColsFiltered[x[2]], use = "na.or.complete", method = "pearson")

          if(!isPositive)tmpCor <- -1*tmpCor
          
          #If it is higher than the lowest correlation in the queue, add it into the queue
          if(!is.na(tmpCor) && (resultQ$size < resultLimit ||  tmpCor > (resultQ$front())$correlation)){

            tmpTuple <- Tuple$new(col1 = x[1], col2 = x[2], groupCol = y, group = as.character(z), correlation = as.numeric(tmpCor), numberOfRecord = nrow(dfWithTwoColsFiltered))
 
            resultQ$insert(tmpTuple)

            #If there is any excess correlation, remove it
            if(resultQ$size > resultLimit){
              resultQ$pop()
            }
          }
        }
      })
    })
  })
  
  #Turn the result into an organized manner
  negation <- 1
  if(!isPositive)negation <- -1
  resultDF <- data.frame(Col1 = character(), Col2 = character(), groupCol = character(), group = character(), correlation = numeric(), numberOfRecord = numeric(), check.names = FALSE, stringsAsFactors = FALSE)
  while(resultQ$size){
    tmpTuple <- resultQ$pop()
    tmpRow <- list(Col1 = tmpTuple$col1, Col2 = tmpTuple$col2, groupCol = tmpTuple$groupCol, group = tmpTuple$group, correlation = negation*tmpTuple$correlation, numberOfRecord = tmpTuple$numberOfRecord)
    resultDF[nrow(resultDF)+1, ]<-tmpRow
  }
  return (resultDF)
}
