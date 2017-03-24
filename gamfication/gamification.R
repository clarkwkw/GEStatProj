#install.packages("ggplot2")
library(ggplot2)

#Import csv file, auto-convert N/A as NA, preserve original column names
rawdata <- read.csv("201617T1 KM Gaming 0220(finalized) (student version).csv", header = TRUE, sep = ",", na.strings=c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"), check.names = FALSE, stringsAsFactors = FALSE)
#formatDF <- read.csv("rangeOfValues_1617T1.csv", header = TRUE, sep = ",", na.strings = c("--"), check.names = FALSE, stringsAsFactors = FALSE) 

#group by 1)sex 2)faculty 3) english proficiency 4)year of study 5)Q46 also, then compare it with the result grouped by game, using chi-square test
#analyse also grade, quiz, rj
#better labeling in graphs

#Quantifying Q18-Q23, borrowed from Danny
quantify <- function(response, choice, converted_num) {
  sapply(as.factor(response), function(x) converted_num[which(x == choice)])
}

ttestResult=NULL

#questionaire Q1-17
for(i in 8:58)
{
  png(paste(names(rawdata)[i],".png",sep=""))
  print(
    ggplot(rawdata)+
      aes(x=rawdata$`Civ 4?`, fill=factor(rawdata[,i])) +
      geom_bar(position = "fill"))
  dev.off()
  ttestResult=rbind(ttestResult,unlist(t.test(rawdata[,i]~rawdata$`Civ 4?`)))
}

#questionaire Q18-19
option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)
for(i in 59:60)
{ 
  response <- rawdata[,i]
  png(paste(names(rawdata)[i],".png",sep=""))
  print(
    ggplot(rawdata)+
      aes(x=rawdata$`Civ 4?`, fill=factor(rawdata[,i])) +
      geom_bar(position = "fill"))
  dev.off()
  ttestResult=rbind(ttestResult,
                    unlist(t.test(quantify(response, option, num)~rawdata$`Civ 4?`)))
}

#questionaire Q20
option <- c("less than 1", "1 to <3", "3 to <6", "6 to <10", "10 to <15", "more than 15")
num <- c(0.5, 2, 4.5, 8, 12.5, 16)
response <- rawdata$`Q20 (Time/RJ)`
png("Q20.png")
print(
  ggplot(rawdata)+
  aes(x=rawdata$`Civ 4?`, fill=factor(rawdata$`Q20 (Time/RJ)`)) +
  geom_bar(position = "fill"))
  dev.off()
  ttestResult=rbind(ttestResult,
                    unlist(t.test(quantify(response, option, num)~rawdata$`Civ 4?`)))
 
#questionaire Q21
option <- c("less than 1", "1 to <2", "2 to <3", "3 to <4", "4 to <5", "more than 5")
num <- c(0.5, 1.5, 2.5, 3.5, 4.5, 6)
response <- rawdata$`Q21 (Time/reading)`
png("Q21.png")
print(
  ggplot(rawdata)+
  aes(x=rawdata$`Civ 4?`, fill=factor(rawdata$`Q21 (Time/reading)`)) +
  geom_bar(position = "fill"))
dev.off()
ttestResult=rbind(ttestResult,
                  unlist(t.test(quantify(response, option, num)~rawdata$`Civ 4?`)))
  
#questionaire Q22-23
option <- c("0", "1-20%", "21-40%", "41-60%", "61-80%", "81-100%")
num <- c(0, .10, .30, .50, .70, .90)
for(i in 63:64)
{ 
  response <- rawdata[,i]
  png(paste('Q',i-41,".png",sep=""))
  print(
    ggplot(rawdata)+
      aes(x=rawdata$`Civ 4?`, fill=factor(rawdata[,i])) +
      geom_bar(position = "fill"))
  dev.off()
  ttestResult=rbind(ttestResult,
                    unlist(t.test(quantify(response, option, num)~rawdata$`Civ 4?`)))
}  

#questionaire Q24-35
for(i in 65:76)
{
  png(paste(names(rawdata)[i],".png",sep=""))
  print(
    ggplot(rawdata)+
      aes(x=rawdata$`Civ 4?`, fill=factor(rawdata[,i])) +
      geom_bar(position = "fill"))
  dev.off()
  ttestResult=rbind(ttestResult,unlist(t.test(rawdata[,i]~rawdata$`Civ 4?`)))
}

#Sex
option <- c("F", "M")
num <- c(0,1)
response <- rawdata$Sex
png("Sex.png")
print(
  ggplot(rawdata)+
    aes(x=rawdata$`Civ 4?`, fill=factor(rawdata$Sex)) +
    geom_bar(position = "fill"))
dev.off()
ttestResult=rbind(ttestResult,
                  unlist(t.test(quantify(response, option, num)~rawdata$`Civ 4?`)))

#questionaire part 4 "Learning Activities(LA)" (Q36-45)
#match Q36 and Q41, Q37 and Q42, etc.
dataOD=subset(rawdata,rawdata$`Civ 4?`==0)
dataOD=cbind(dataOD$`Civ 4?`,dataOD[,137:141])
names(dataOD)=c("Civ 4?","LA1","LA2","LA3","LA4","LA5")
dataCiv=b=subset(rawdata,rawdata$`Civ 4?`==1)
dataCiv=cbind(dataCiv$`Civ 4?`,dataCiv[,142:146])
names(dataCiv)=c("Civ 4?","LA1","LA2","LA3","LA4","LA5")
dataComb=rbind(dataCiv,dataOD)
#graph and t test
for(i in 2:6)
{
  png(paste(names(dataComb)[i],".png",sep=""))
  print(
    ggplot(dataComb)+
      aes(x=dataComb$`Civ 4?`, fill=factor(dataComb[,i])) +
      geom_bar(position = "fill"))
  dev.off()
  ttestResult=rbind(ttestResult,unlist(t.test(dataComb[,i]~dataComb$`Civ 4?`)))
}

#Grade
option <- c("A", "A-","B+","B","B-","C+","C","C-","D+","D","F")
num <- c(4, 3.7, 3.3, 3, 2.7, 2.3, 2, 1.7, 1.3, 1, 0)
response <- rawdata$Grade
png("Grade.png")
print(
  ggplot(rawdata)+
    aes(x=rawdata$`Civ 4?`, fill=factor(rawdata$Grade)) +
    geom_bar(position = "fill"))
dev.off()
ttestResult=rbind(ttestResult,
                  unlist(t.test(quantify(response, option, num)~rawdata$`Civ 4?`)))

#cGPA before and After
for(i in 99:100)
{
  rawdata[rawdata[,i]==0,i]=NA
  png(paste(names(rawdata)[i],".png",sep=""))
  print(
    ggplot(rawdata)+
      aes(x=rawdata$`Civ 4?`, fill=factor(rawdata[,i])) +
      geom_bar(position = "fill"))
  dev.off()
  ttestResult=rbind(ttestResult,unlist(t.test(rawdata[,i]~rawdata$`Civ 4?`)))
}

#Raw Mark
png("Raw Mark.png")
print(
  ggplot(rawdata)+
    aes(x=rawdata$`Civ 4?`, fill=factor(rawdata$`Raw Mark (Performance)`)) +
    geom_bar(position = "fill"))
dev.off()
ttestResult=rbind(ttestResult,
                  unlist(t.test(rawdata$`Raw Mark (Performance)`~rawdata$`Civ 4?`)))

#ttestResult naming and exporting
row.names(ttestResult) <- c(names(rawdata[,8:77]),names(dataComb[,2:6]),names(rawdata[,98:100]),"Raw Mark (Performance)")
write.csv(ttestResult,file ="ttestResult.csv" )