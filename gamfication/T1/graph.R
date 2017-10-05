install.packages("ggplot2")
library(ggplot2)

#Import csv file, auto-convert N/A as NA, preserve original column names
rawdata <- read.csv("201617T1 KM Gaming 0220(finalized) (student version).csv", header = TRUE, sep = ",", na.strings=c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"), check.names = FALSE, stringsAsFactors = FALSE)

#group by 1)sex 2)faculty 3) english proficiency 4)year of study 5)Q46 also, then compare it with the result grouped by game, using chi-square test
#analyse also grade, quiz, rj
#better labeling in graphs

data <- read.csv("data.csv", header = TRUE, sep = ",",row.names = 1)
group <- read.csv("group.csv", header = TRUE, sep = ",", na.string=c("NA","Others"),row.names = 1)

for(i in 1:ncol(group))
{
  for(j in 1:ncol(data))
  {
    png(paste(names(group)[i],"_",names(data)[j],".png",sep=""))
    print(
      ggplot(data)+
      aes(x=group[,i], fill=factor(data[,j])) +
      geom_bar(position = "fill"))
    dev.off()
  }
}
