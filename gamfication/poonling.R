#Import csv file, auto-convert N/A as NA, preserve original column names
rawdata <- read.csv("201617T1_KMKonly_data.csv", header = TRUE, sep = ",", na.strings=c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"), check.names = FALSE, stringsAsFactors = FALSE)
formatDF <- read.csv("rangeOfValues_1617T1.csv", header = TRUE, sep = ",", na.strings = c("--"), check.names = FALSE, stringsAsFactors = FALSE) 

#Tag out OD and Civ 4 participants
tag_civ=which(!is.na(rawdata$Q41))
tag_OD=which(!is.na(rawdata$Q36))

#doubt students who play civ4 would join OD, therefore excluding those already in tag_Civ
tag_OD=tag_OD[!tag_OD%in%tag_civ]


#Remove Subject, Sub-class, Class no.
rawdata[1:3]<-list(NULL)

#Remove empty rows
rawdata <- rawdata[rowSums(is.na(rawdata) | rawdata == "") != ncol(rawdata),]

for(i in 1:7){rawdata[rawdata[,52]==formatDF[i,52],52]=2*i-1.5}

for(i in 1:6){rawdata[rawdata[,53]==formatDF[i,53],53]=2*i-1.5}

rawdata[rawdata[,54]==formatDF[1,54],54]=0.5
for(i in 2:5){rawdata[rawdata[,54]==formatDF[i,54],54]=mean(as.numeric(unlist(strsplit(formatDF[i,54]," to <"))))}
rawdata[rawdata[,54]==formatDF[6,54],54]=15

for(i in 1:6){rawdata[rawdata[,55]==formatDF[i,55],55]=i-0.5}

for(i in 1:6){rawdata[rawdata[,56]==formatDF[i,56],56]=max(0.2*(i-1)-0.1,0)}

for(i in 1:6){rawdata[rawdata[,57]==formatDF[i,57],57]=max(0.2*(i-1)-0.1,0)}

for(i in 52:57){rawdata[,i]=as.numeric(rawdata[,i])}

rawdata=cbind(rep(0,nrow(rawdata)),rawdata)
# ---Check for "out-of-range" records---
#Import rangeOfValues.csv, which specifies possible answers for each question, to formatDF dataframe

rawdata[rawdata$Q41 %in% 1:6,1]="Civ"
rawdata[!rawdata$Q41 %in% 1:6,1]="OD"
for(i in 2:70)
{
boxplot(rawdata[,i]~rawdata[,1],main=names(rawdata)[i])
points(1:2,aggregate(rawdata[,i],list(rawdata[,1]),mean,na.rm=TRUE, na.action=NULL)[,2],col="red")
print(names(rawdata[i]))
print(t.test(rawdata[,i]~rawdata[,1]))
}