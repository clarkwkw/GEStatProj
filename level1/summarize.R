# Import these packages
library(ggplot2)
library(plyr)
library(reshape2)
library(scales)
library(grid)

# Question: a question name which has both "XX (Before)" and "XX (After)" columns.
# e.g. level1_summarize("Q1")
# toPDF: If set to True, the graphs will be saved as ./output/lv1-Summary-%Question%-distribution.pdf and ./output/lv1-Summary-%Question%-tracking.pdf
# Distribution table will be returned as a data frame
# There will be two graphs (distribution graph and tracking graph) printed
level1_summarize <- function(question, toPDF = FALSE){
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
  
  # Reformat distribution table to generate distribution graph
  graphDF <- melt(distributionTable[1:(nrow(distributionTable)-1), c("Value", "Before - %", "After - %")], id = "Value")
  graphDF <- rename(graphDF, c("value"="Percentage"))
  
  # Plot the distribution graph
  distributionGraph <- ggplot(graphDF, aes(x = Value, y = Percentage, fill = factor(variable, levels = c("Before - %", "After - %"))), environment = environment())
  distributionGraph <- distributionGraph + 
    ggtitle(paste(question, "- Distribution")) +
    geom_bar(width = 0.8, stat = "identity", position = "dodge") +
    theme(axis.title.x = element_blank()) +
    theme(axis.title.y = element_blank()) +
    theme(legend.title = element_blank()) +
    scale_y_continuous(breaks = round(seq(0, ceiling(max(graphDF[["Percentage"]])/10)*10, by = 10),1), labels = appendPercentage)
  
  print(distributionGraph)
  if(toPDF){
    fileName <- paste("./output/lv1Summary-", question, "-distribution.pdf", sep = "")
    ggsave(fileName, distributionGraph)
  }
  
  # Initialize a tracking table
  trackingTable <- matrix(NA, nrow = length(q1PossibleAns)*length(q2PossibleAns), ncol = 4)
  colnames(trackingTable) <- c("Before", "After", "Count", "Percentage")
  trackingTable <- as.data.frame(trackingTable)
  
  # Fill in some initial values
  trackingTable[, c("After", "Before")] <- expand.grid(q2PossibleAns, q1PossibleAns)
  
  # Initialize a vector to store mean value
  trackingMean <- vector(mode = "double", length = length(q1PossibleAns))
  names(trackingMean) <- q1PossibleAns
  
  # Fill in the table
  sapply(q1PossibleAns, FUN = function(x){
   if (x == "NA")return();
    sumScore <- 0
    totalcount <- 0
    sapply(q2PossibleAns, FUN = function(y){
      if (y == "NA")return();
      # Count no. of respondants who belong to this category
      count <- nrow(rawdata[rawdata[[questionPair[1]]] == x & rawdata[[questionPair[2]]] == y, ])
      trackingTable[trackingTable[["Before"]] == x & trackingTable[["After"]] == y, "Count"] <<- count
      
      # Sum the values for calculation of weighted mean
      totalcount <<- totalcount + count
      sumScore <<- sumScore + count * as.numeric(y)
      
    })
    # Calulate weighted mean
    trackingTable[trackingTable[["Before"]] == x, "Percentage"] <<- trackingTable[trackingTable[["Before"]] == x, "Count"]/sum(trackingTable[trackingTable[["Before"]] == x, "Count"], na.rm = TRUE)*100
    trackingMean[x] <<- round(sumScore/totalcount, digits = 2)
  })
  # Remove category with name NA
  trackingTable <- trackingTable[trackingTable[["Before"]] != "NA" & trackingTable[["After"]] != "NA",]
  
  # Plot the tracking graph
  trackingGraph <- ggplot(trackingTable, aes(x = Before, y = Percentage, fill = factor(After, levels = rev(levels(After)))), environment = environment())
  trackingGraph <- trackingGraph +
    geom_bar(width = 0.6, position = "fill", stat = "identity") +
    ggtitle(paste(question, "- Tracking Analysis")) +
    labs(x = "Before", y = "After") +
    geom_text(aes(x = Before, y = 1.15, label = trackingMean[Before], hjust = 1), size = 3) +
    guides(fill=guide_legend(title="After", nrow = 1, reverse = TRUE)) +
    scale_y_continuous(breaks = seq(0, 1, by = 0.1), labels = percent_format()) +
    theme(legend.position = "bottom", legend.box = "horizontal", axis.title.x = element_blank()) +
    annotation_custom(
      grob = textGrob(label = "Mean (After)", hjust = 0, gp = gpar(cex = 1.5, fontsize = 5)),
      ymin = 1,    
      ymax = 1,
      xmin = 6.5, 
      xmax = 6.5) +
    coord_flip()
  
  
  print(trackingGraph)
  if(toPDF){
    fileName <- paste("./output/lv1Summary-", question, "-tracking.pdf", sep = "")
    ggsave(fileName, trackingGraph)
  }
  
  distributionTable[, "Value"] <- NULL
  return (distributionTable)
}