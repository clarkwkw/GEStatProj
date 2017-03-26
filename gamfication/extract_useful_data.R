rawdata <- read.csv("201617T1 KM Gaming 0220(finalized) (student version).csv", header = TRUE, sep = ",", na.strings=c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"), check.names = FALSE, stringsAsFactors = FALSE)

#Quantifying Q18-Q23, borrowed from Danny
quantify <- function(response, choice, converted_num) {
  sapply(as.factor(response), function(x) converted_num[which(x == choice)])
}

part1to3=rawdata[,8:76]

OD=rawdata[,137:141]
Civ4=rawdata[,142:146]
OD[which(rawdata$`Civ 4?`==1),]=Civ4[which(rawdata$`Civ 4?`==1),]
names(OD)=c("LA1","LA2","LA3","LA4","LA5")
part4=OD

grade=rawdata[,98:100]
quiz=rawdata[,115:121]
rJ=rawdata[,123:128]
tP=rawdata[,130:135]

group=cbind(rawdata$`Civ 4?`,rawdata$Sex,rawdata$`English Proficiency`,rawdata$Q46,rawdata$Faculty,rawdata$`Year of Study`)
data=cbind(part1to3,part4,grade,rawdata$`Raw Mark (Performance)`,quiz,rJ,tP,rawdata$Total)
colnames(group)=c("Civ4","Sex","Eng","KEEP","Fac","Year")

#Quantification
#questionaire Q18
option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)
response <- data$`Q18 (Assigned Text Read Completely)`
data$`Q18 (Assigned Text Read Completely)`=quantify(response, option, num)

#questionaire Q19
option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)
response <- data$`Q19 (Chinese Translation)`
data$`Q19 (Chinese Translation)`=quantify(response, option, num)

#questionaire Q20
option <- c("less than 1", "1 to <3", "3 to <6", "6 to <10", "10 to <15", "more than 15")
num <- c(0.5, 2, 4.5, 8, 12.5, 16)
response <- data$`Q20 (Time/RJ)`
data$`Q20 (Time/RJ)`=quantify(response, option, num)

#questionaire Q21
option <- c("less than 1", "1 to <2", "2 to <3", "3 to <4", "4 to <5", "more than 5")
num <- c(0.5, 1.5, 2.5, 3.5, 4.5, 6)
response <- data$`Q21 (Time/reading)`
data$`Q21 (Time/reading)`=quantify(response, option, num)

#questionaire Q22
option <- c("0", "1-20%", "21-40%", "41-60%", "61-80%", "81-100%")
num <- c(0, .10, .30, .50, .70, .90)
response <- data$`Q22 (% Lecture)`
data$`Q22 (% Lecture)`=quantify(response, option, num)

#questionaire Q23
option <- c("0", "1-20%", "21-40%", "41-60%", "61-80%", "81-100%")
num <- c(0, .10, .30, .50, .70, .90)
response <- data$`Q23 (% tutorial participation)`
data$`Q23 (% tutorial participation)`=quantify(response, option, num)

#Sex
#option <- c("F", "M")
#num <- c(0,1)
#response <- data$Sex
#data$Sex=quantify(response, option, num)

#Grade
option <- c("A", "A-","B+","B","B-","C+","C","C-","D+","D","F")
num <- c(4, 3.7, 3.3, 3, 2.7, 2.3, 2, 1.7, 1.3, 1, 0)
response <- data$Grade
data$Grade=quantify(response, option, num)

write.csv(data,file="data.csv")
write.csv(group,file="group.csv")