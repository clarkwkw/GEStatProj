# Incomplete
# Require: ggplot2 plyr reshape2 scales
level1_summarize <- function(question){
  appendPercentage <- function(x){
    return (paste(x, "%", sep = ""))
  }
  
  questionPair <- paste(question, c("(Before)", "(After)"))
  q1PossibleAns <- formatDF[[questionPair[1]]]
  q1PossibleAns <- q1PossibleAns[q1PossibleAns!="" & !is.na(q1PossibleAns)]
  
  q2PossibleAns <- formatDF[[questionPair[2]]]
  q2PossibleAns <- q2PossibleAns[q2PossibleAns!="" & !is.na(q2PossibleAns)]
  # Check whether 2 columns are having same set of possible answers
  if(length(q1PossibleAns) != length(q2PossibleAns) || any(q1PossibleAns != q2PossibleAns)){
    stop("Incompatible Columns.")
  }
  # Initialize a distribution table
  distributionTable <- matrix(data = NA, nrow = length(q1PossibleAns) + 1, ncol = 5)
  
  colnames(distributionTable) <- c("Value", "Before", "Before - %", "After", "After - %")
  rownames(distributionTable) <- c(q1PossibleAns, "Total")
  distributionTable <- as.data.frame(distributionTable)
  distributionTable[, "Value"] <- rownames(distributionTable)
  
  # Summarize the distribution seperately
  simpleResult1 <- as.matrix(table(rawdata[[questionPair[1]]]))
  simpleResult2 <- as.matrix(table(rawdata[[questionPair[2]]]))
  
  # Combine the distribution in to one matrix
  distributionTable[rownames(simpleResult1), "Before"] <- simpleResult1
  distributionTable[rownames(simpleResult2), "After"] <- simpleResult2
  
  # If NA is one of the valid answer, include it in the table 
  if("NA" %in% q1PossibleAns){
    distributionTable["NA", "Before"] <- sum(is.na(rawdata[[questionPair[1]]]))
    distributionTable["NA", "After"] <- sum(is.na(rawdata[[questionPair[2]]]))
  }
  #return(distributionTable)
  # Calculate total
  distributionTable["Total", "Before"] <- sum(distributionTable[, "Before"], na.rm = TRUE)
  distributionTable["Total", "After"] <- sum(distributionTable[, "After"], na.rm = TRUE)
  
  # If the total no. of respondants for "before" is not equal to "after"
  # or total no. of respondants is not equal to the no. of rows in rawdata
  # output warning
  if(distributionTable["Total", "Before"] != distributionTable["Total", "After"]){
    warning("Total no. of records in two columns are not the same")
  }else if(distributionTable["Total", "Before"] != nrow(rawdata)){
    warning("Total no. of records in summary does not equal to total no. of records in original dataframe.")
  }
  
  # Calculate percentage
  total1 <- distributionTable["Total", "Before"]
  total2 <- distributionTable["Total", "After"]
  distributionTable[, "Before - %"] <- round(distributionTable[, "Before"]/total1*100, digit = 2)
  distributionTable[, "After - %"] <- round(distributionTable[, "After"]/total1*100, digit = 2)

  
  distributionGraph <- NA
  graphDF <- melt(distributionTable[1:(nrow(distributionTable)-1), c("Value", "Before - %", "After - %")], id = "Value")
  graphDF <- rename(graphDF, c("value"="Percentage"))
  
  distributionGraph <- ggplot(graphDF, aes(x = Value, y = Percentage, fill = factor(variable, levels = c("Before - %", "After - %"))), environment = environment())
  distributionGraph <- distributionGraph + 
    ggtitle(paste(question, "- Distribution")) +
    geom_bar(width = 0.8, stat = "identity", position = "dodge") +
    theme(axis.title.x = element_blank()) +
    theme(axis.title.y = element_blank()) +
    theme(legend.title = element_blank()) +
    scale_y_continuous(breaks = round(seq(0, ceiling(max(graphDF[["Percentage"]])/10)*10, by = 10),1), labels = appendPercentage)
     
  
  print(distributionGraph)
  
  distributionTable[, "Value"] <- NULL
  return (distributionTable)
  
  
}