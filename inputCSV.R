source("utilities.R")

#Import csv file, auto-convert N/A as NA, preserve original column names
rawdata <- read.csv("1415T2 Data (0924 version_ for student trial).csv", header = T, sep = ",", na.strings = c("N/A"), check.names = F)

#Remove empty rows
rawdata <- rawdata[rowSums(is.na(rawdata) | rawdata == "") != ncol(rawdata),]

#Remove redundant columns (tag1 to 4)
for(i in c(1:4))
  rawdata[[paste("Tag", as.character(i), sep = "")]] <- NULL

# ---check for "out-of-range" records---
formatDF <- read.csv("rangeOfValues.csv", header = TRUE, sep = ",", na.strings = c("--"),check.names = FALSE)
invalidDF <- sapply(colnames(formatDF), function(x) checkdata(rawdata, formatDF[[x]], x))
invalidDF <- as.data.frame(do.call(rbind, invalidDF))
rownames(invalidDF) <- NULL

#---Check for dependant answer (Eng Proficiency & DSE Grade)---#
tmpDF <- rawdata[!is.na(rawdata[["Eng Proficiency"]]), ]
tmpDF <- tmpDF[tmpDF[["Eng Proficiency"]] == "DSE" & is.na(tmpDF[["DSE Eng Grade"]]), "Tag Number", drop = FALSE]
tmpDF[["Reason"]] = "Missing DSE Eng Grade"
invalidDF <- mergeInvalidDF(invalidDF, tmpDF)
remove(tmpDF)