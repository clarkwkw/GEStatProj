# Incomplete
level1_summarize <- function(questionPair){
  q1PossibleAns <- formatDF[[questionPair[1]]]
  q1PossibleAns <- q1PossibleAns[q1PossibleAns!="" & !is.na(q1PossibleAns)]
  
  q2PossibleAns <- formatDF[[questionPair[2]]]
  q2PossibleAns <- q2PossibleAns[q2PossibleAns!="" & !is.na(q2PossibleAns)]
  # Check whether 2 columns are having same set of possible answers
  if(length(q1PossibleAns) != length(q2PossibleAns) || any(q1PossibleAns != q2PossibleAns)){
    stop("Incompatible Columns.")
  }
  # Initialize a distribution table
  distributionTable <- matrix(data = NA, nrow = length(q1PossibleAns) + 1, ncol = 4)
  colnames(distributionTable) <- c("Before - Count", "Before - %", "After - Count", "After - %")
  rownames(distributionTable) <- c(q1PossibleAns, "Total")
  
  # Summarize the distribution seperately
  simpleResult1 <- as.matrix(table(rawdata[[questionPair[1]]]))
  simpleResult2 <- as.matrix(table(rawdata[[questionPair[2]]]))
  
  # Combine the distribution in to one matrix
  distributionTable[rownames(simpleResult1), "Before - Count"] <- simpleResult1
  distributionTable[rownames(simpleResult2), "After - Count"] <- simpleResult2
  
  # If NA is one of the valid answer, include it in the table 
  if("NA" %in% q1PossibleAns){
    distributionTable["NA", "Before - Count"] <- sum(is.na(rawdata[[questionPair[1]]]))
    distributionTable["NA", "After - Count"] <- sum(is.na(rawdata[[questionPair[2]]]))
  }
  
  # Calculate total
  distributionTable["Total", "Before - Count"] <- sum(distributionTable[, "Before - Count"], na.rm = TRUE)
  distributionTable["Total", "After - Count"] <- sum(distributionTable[, "After - Count"], na.rm = TRUE)
  
  # If the total no. of respondants for "before" is not equal to "after"
  # or total no. of respondants is not equal to the no. of rows in rawdata
  # output warning
  if(distributionTable["Total", "Before - Count"] != distributionTable["Total", "After - Count"]){
    warning("Total no. of records in two columns are not the same")
  }else if(distributionTable["Total", "Before - Count"] != nrow(rawdata)){
    warning("Total no. of records in summary does not equal to total no. of records in original dataframe.")
  }
  
  # Calculate percentage
  total1 <- distributionTable["Total", "Before - Count"]
  total2 <- distributionTable["Total", "After - Count"]
  distributionTable[, "Before - %"] <- round(distributionTable[, "Before - Count"]/total1*100, digit = 2)
  distributionTable[, "After - %"] <- round(distributionTable[, "After - Count"]/total1*100, digit = 2)
  
  distributionGraph <- NA
  
  return (distributionTable)
  
  
}