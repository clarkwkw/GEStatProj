#install.packages("reshape")
library(reshape)

data <- read.csv("data.csv", header = TRUE, sep = ",",row.names = 1)
group <- read.csv("group.csv", header = TRUE, sep = ",", na.string=c("NA","Others"),row.names = 1)
comb=cbind(group,data)
groupLabel=(1:ncol(group))*-1

for(i in 1:(ncol(group)-1))
  {
  if(length(levels(factor(comb[,i])))==2)
    {
    testResult=t(apply(comb[,groupLabel],2, function(x) unlist(t.test(x~comb[,i]))))
    outputName=paste(names(comb)[i],".csv")
    write.csv(testResult,file=outputName)
    }
  }

#t test grouped by year
#year 1 has no cGPA before
testResult=t(apply(comb[,c(-83,groupLabel)],2, function(x) unlist(t.test(x~comb$Year))))
write.csv(testResult,file="Year.csv")

#t test of bad DSE Eng. student grouped by civ 4 player or not
badEng=subset(comb, Eng=="DSE 4 or below")
testResult=t(apply(badEng[,groupLabel],2, function(x) unlist(t.test(x~badEng$Civ4))))
write.csv(testResult,file="Bad_Eng_DSE.csv")

#t test of civ 4 player grouped by english proficiency
civPlayer=subset(comb, Civ4==1)
testResult=t(apply(civPlayer[,groupLabel],2, function(x) unlist(t.test(x~civPlayer$Eng))))
write.csv(testResult,file="Lower_Eng_DSE.csv")
