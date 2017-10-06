T1data <- read.csv("201617T1 KM Gaming 0220(finalized) (student version).csv", header = TRUE, sep = ",", na.strings=c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"), check.names = FALSE, stringsAsFactors = FALSE)
T2data <- read.csv("201617_KaiMing.csv", header = TRUE, sep = ",", na.strings=c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"), check.names = FALSE, stringsAsFactors = FALSE)
T2data <- T2data[which(!is.na(T2data[,1])),]

#Quantifying Q18-Q23, borrowed from Danny
quantify <- function(response, choice, converted_num) {
  sapply(as.factor(response), function(x) converted_num[which(x == choice)])
}

part1to3=rbind(T1data[,8:76],T2data[,5:73])

OD=rbind(T1data[which(T1data$`Civ 4?`==0),137:141],T2data[which(is.na(T2data$Q41)),111:115])
Civ4=rbind(T1data[which(T1data$`Civ 4?`==1),142:146],T2data[which(!is.na(T2data$Q41)),116:120])
names(OD)=c("LA1","LA2","LA3","LA4","LA5")
names(Civ4)=c("LA1","LA2","LA3","LA4","LA5")
part4=rbind(Civ4,OD)

grade=rbind(T1data[,97:100],T2data[,94:97])


#demographic
game=factor(c(T1data$`Civ 4?`,!is.na(T2data$Q41)),levels=0:1,labels = c("OD","Civ4"))
sex=factor(c(T1data$Sex,T2data$Sex))
lang=factor(c(T1data$Language,T2data$Language))
eng=factor(c(T1data$`English Proficiency`,T2data$`English Proficiency`))
fac=factor(c(T1data$Faculty,T2data$Faculty))
coll=factor(c(T1data$College,T2data$College))
year=factor(c(T1data$`Year of Study`,T2data$`Year of Study`))
first=factor(c(T1data$`First GEF?`,T2data$`First GEF?`))

demographic=data.frame("Outside Class Activity"=game,"Sex"=sex, "First Language"=lang, "DSE English Grade"=eng, "Faculty"=fac, "College"=coll, "Year of Study"=year, "First GEF"=first)
varname=c("Outside Class Activity","Sex", "First Language", "DSE English Grade", "Faculty", "College", "Year of Study", "First GEF")
elec=rbind(T1data[,78:91],T2data[,75:88])


#Quantification
#questionaire Q18
option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)
response <- part1to3$`Q18 (Assigned Text Read Completely)`
part1to3$`Q18 (Assigned Text Read Completely)`=quantify(response, option, num)

#questionaire Q19
option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)
response <- part1to3$`Q19 (Chinese Translation)`
part1to3$`Q19 (Chinese Translation)`=quantify(response, option, num)

#questionaire Q20
option <- c("less than 1", "1 to <3", "3 to <6", "6 to <10", "10 to <15", "more than 15")
num <- c(0.5, 2, 4.5, 8, 12.5, 16)
response <- part1to3$`Q20 (Time/RJ)`
part1to3$`Q20 (Time/RJ)`=quantify(response, option, num)

#questionaire Q21
option <- c("less than 1", "1 to <2", "2 to <3", "3 to <4", "4 to <5", "more than 5")
num <- c(0.5, 1.5, 2.5, 3.5, 4.5, 6)
response <- part1to3$`Q21 (Time/reading)`
part1to3$`Q21 (Time/reading)`=quantify(response, option, num)

#questionaire Q22
option <- c("0", "1-20%", "21-40%", "41-60%", "61-80%", "81-100%")
num <- c(0, .10, .30, .50, .70, .90)
response <- part1to3$`Q22 (% Lecture)`
part1to3$`Q22 (% Lecture)`=quantify(response, option, num)

#questionaire Q23
option <- c("0", "1-20%", "21-40%", "41-60%", "61-80%", "81-100%")
num <- c(0, .10, .30, .50, .70, .90)
response <- part1to3$`Q23 (% tutorial participation)`
part1to3$`Q23 (% tutorial participation)`=quantify(response, option, num)

#Sex
#option <- c("F", "M")
#num <- c(0,1)
#response <- data$Sex
#data$Sex=quantify(response, option, num)

#Grade
option <- c("A", "A-","B+","B","B-","C+","C","C-","D+","D","F")
num <- c(4, 3.7, 3.3, 3, 2.7, 2.3, 2, 1.7, 1.3, 1, 0)
response <- grade$Grade
grade$Grade=quantify(response, option, num)

#cGPA Before
grade$`cGPA (Before)`[which(grade$`cGPA (Before)`==0)]=NA
