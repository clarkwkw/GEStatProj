install.packages("reshape")
library(reshape)

data <- read.csv("data.csv", header = TRUE, sep = ",",row.names = 1)
group <- read.csv("group.csv", header = TRUE, sep = ",", na.string=c("NA","Others"),row.names = 1)
comb=cbind(group,data)
groupLabel=(1:ncol(group))*-1

for(i in 1:ncol(group))
  {
  if(length(levels(factor(comb[,i])))==2)
    {
    testResult=t(apply(comb[,groupLabel],2, function(x) unlist(t.test(x~comb[,i]))))
    outputName=paste(names(comb)[i],".csv")
    write.csv(testResult,file=outputName)
    }
  }

