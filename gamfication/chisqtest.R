group <- read.csv("group.csv", header = TRUE, sep = ",", na.string=c("NA","Others"),row.names = 1)
chisqtest=NULL
for(i in 2:(ncol(group)))
{
  chisqtest=rbind(chisqtest,
                  unlist(chisq.test(table(group$Civ4,group[,i])))[1:4])
  row.names(chisqtest)[i-1]=names(group)[i]
}

write.csv(chisqtest,"chisqtest.csv")
