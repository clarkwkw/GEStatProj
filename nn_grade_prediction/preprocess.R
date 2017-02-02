
preprocess <- function(){
  # --- Definition of conversion functions --- #
  
  # Normalize column to 0 to 1
  # If multiple columns are provided, it will first take an average of those columns
  # Resultant values <0 or >1 will be converted to 0 and 1 respectively
  normalize <- function(resultDF, rawdata, oriCol, minVal, maxVal, targetCol){
    resultVect <- vector(mode = "numeric", length = nrow(rawdata))
    sapply(oriCol, FUN = function(x){
      resultVect <<- resultVect + rawdata[, x]/length(oriCol)
    })
    resultDF[, targetCol] <- (resultVect - minVal)/(maxVal - minVal)
    resultDF[resultDF[,targetCol] > 1 & !is.na(resultDF[,targetCol]), targetCol] <- 1
    resultDF[resultDF[,targetCol] < 0 & !is.na(resultDF[,targetCol]), targetCol] <- 0
    return(resultDF)
  }
  
  # Convert a column with multiple possible values to binary
  # Mapping:  1. NA valus remain NA
  #           2. Values in trueVals will be 1, values in falseVals will be 0
  #           3. If trueVals is not specified, values not in falseVals will be 1
  #           4. If falseVals is not specified, values not in trueVals will be 0
  binarize <- function(resultDF, rawdata, oriCol, falseVals = NA, trueVals = NA, targetCol){
    resultDF[, targetCol] <- -1
    resultDF[is.na(rawdata[, oriCol]), targetCol] <- NA
    if(is.na(falseVals) && is.na(trueVals)){
      stop(paste("At least either of trueVals or falseVals must be specified. (", targetCol, ")", sep = ""))
    }
    complementVal <- -1
    if(is.na(trueVals) || !is.na(falseVals)){
      resultDF[rawdata[, oriCol] %in% falseVals & !is.na(rawdata[, oriCol]), targetCol] <- 0
      complementVal <- 1
    }
    if(is.na(falseVals) || !is.na(trueVals)){
      resultDF[rawdata[, oriCol] %in% trueVals & !is.na(rawdata[, oriCol]), targetCol] <- 1
      complementVal <- 0
    }
    resultDF[resultDF[, targetCol] == -1 & !is.na(resultDF[, targetCol]), targetCol] <- complementVal
    return(resultDF)
  }
  
  # Convert grade in alphabet to decimal
  gradeToDec <- function(resultDF, rawdata, oriCol, targetCol){
    resultDF[, targetCol] <- rawdata[, oriCol]
    resultDF[resultDF[, targetCol] == "A" & !is.na(resultDF[, targetCol]), targetCol] <- 4
    resultDF[resultDF[, targetCol] == "A-" & !is.na(resultDF[, targetCol]), targetCol] <- 3.7
    resultDF[resultDF[, targetCol] == "B+" & !is.na(resultDF[, targetCol]), targetCol] <- 3.3
    resultDF[resultDF[, targetCol] == "B" & !is.na(resultDF[, targetCol]), targetCol] <- 3
    resultDF[resultDF[, targetCol] == "B-" & !is.na(resultDF[, targetCol]), targetCol] <- 2.7
    resultDF[resultDF[, targetCol] == "C+" & !is.na(resultDF[, targetCol]), targetCol] <- 2.3
    resultDF[resultDF[, targetCol] == "C" & !is.na(resultDF[, targetCol]), targetCol] <- 2
    resultDF[resultDF[, targetCol] == "C-" & !is.na(resultDF[, targetCol]), targetCol] <- 1.7
    resultDF[resultDF[, targetCol] == "D+" & !is.na(resultDF[, targetCol]), targetCol] <- 1.3
    resultDF[resultDF[, targetCol] == "D" & !is.na(resultDF[, targetCol]), targetCol] <- 1
    resultDF[resultDF[, targetCol] == "F" & !is.na(resultDF[, targetCol]), targetCol] <- 0
    return(resultDF)
  }
  textToDec <- function(resultDF, rawdata, oriCol, targetCol){
    resultDF[, targetCol] <- NA
    resultDF[!is.na(rawdata[, oriCol]) & (rawdata[, oriCol] == "12" | rawdata[, oriCol] == "10 to 11"), targetCol] <- 1
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "8 to 9", targetCol] <- 0.8
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "6 to 7", targetCol] <- 0.6
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "4 to 5", targetCol] <- 0.4
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "2 to 3", targetCol] <- 0.2
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "0 to 1", targetCol] <- 0
    return(resultDF)
  }
  percentToDec <- function(resultDF, rawdata, oriCol, targetCol){
    resultDF[, targetCol] <- NA
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "81 to 100%", targetCol] <- 1
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "61 to 80%", targetCol] <- 0.8
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "41 to 60%", targetCol] <- 0.6
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "21 to 40%", targetCol] <- 0.4
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "1 to 20%", targetCol] <- 0.2
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "0%", targetCol] <- 0
    return(resultDF)
  }
  timeToDec <- function(resultDF, rawdata, oriCol, targetCol){
    resultDF[, targetCol] <- NA
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "more than 4", targetCol] <- 1
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "3 to < 4hrs", targetCol] <- 0.75
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "2 to < 3hrs", targetCol] <- 0.5
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "1 to < 2hrs", targetCol] <- 0.25
    resultDF[!is.na(rawdata[, oriCol]) & rawdata[, oriCol] == "less than 1", targetCol] <- 0
    return(resultDF)
  }
  # Calculate English proficiency (0 - 2)
  # Mapping:  1. Students whose Language is English,        2
  #           2. Students with DSE Eng Grade "5 or above",  1
  #           3. Cantonese non DSE students,                1
  #           4. Students with DSE Eng Grade "4 or below",  0
  #           5. Mandarin non DSE students,                 0
  #           Otherwise, mark their proficiency as NA (to be excluded)
  #           Including a. Cantonese/Mandarin DSE students without DSE grade
  #                     b. Students who did not choose any of the languages with no DSE grade
  eng_prof <- function(resultDF, rawdata, targetCol){
    resultDF[, targetCol] <- NA
    resultDF[is.na(resultDF[, targetCol]) & !is.na(rawdata[, "Language"]) & rawdata[, "Language"] == "English", targetCol] <- 2
    resultDF[is.na(resultDF[, targetCol]) & !is.na(rawdata[, "DSE Eng Grade"]) & rawdata[, "DSE Eng Grade"] == "5 or above", targetCol] <- 1
    resultDF[is.na(resultDF[, targetCol]) & !is.na(rawdata[, "DSE?"]) & !is.na(rawdata[, "Language"]) & rawdata[, "DSE?"] != "Yes" & rawdata[, "Language"] == "Cantonese", targetCol] <- 1
    resultDF[is.na(resultDF[, targetCol]) & !is.na(rawdata[, "DSE Eng Grade"]) & rawdata[, "DSE Eng Grade"] == "4 or below", targetCol] <- 0
    resultDF[is.na(resultDF[, targetCol]) & !is.na(rawdata[, "DSE?"]) & !is.na(rawdata[, "Language"]) & rawdata[, "DSE?"] != "Yes" & rawdata[, "Language"] == "Putonghua", targetCol] <- 0
    return(resultDF)
  }
  
  # --- End of conversion functions definition --- #
  
  
  resultDF <- rawdata[, "Tag Number", drop = FALSE]
  resultDF <- normalize(resultDF, rawdata, c("Q1 (Before)", "Q3 (Before)", "Q4 (Before)", "Q5 (Before)"), 1, 6, "Logical")
  resultDF <- normalize(resultDF, rawdata, c("Q6 (Before)", "Q7 (Before)", "Q8 (Before)"), 1, 6, "Appreciation of Science")
  resultDF <- normalize(resultDF, rawdata, c("Q9 (Before)", "Q10 (Before)", "Q11 (Before)", "Q12 (Before)"), 1, 6, "Understanding of Science")
  resultDF <- normalize(resultDF, rawdata, c("Q13 (Before)", "Q15 (Before)"), 1, 6, "Understanding of Good life")
  resultDF <- normalize(resultDF, rawdata, c("Q2 (Before)", "Q14 (Before)", "Q16 (Before)", "Q17 (Before)"), 1, 6, "Appreciation of Diversity")
  resultDF <- binarize(resultDF, rawdata,"Sex", "F", "M", "Sex")
  resultDF[, "nSci"] <- rowSums(rawdata[, c("Phy", "Chem", "Bio", "Com Sci", "Inter Sci")], na.rm = TRUE)
  resultDF <- normalize(resultDF, resultDF, "nSci", 0, 3, "nSci")
  resultDF[, "nNonSci"] <- rowSums(rawdata[, c("Eng Lit", "Chin Lit", "History", "Chin History", "Ethics & RS", "Music", "Visual Art", "Econ", "Geog")], na.rm = TRUE)
  resultDF <- normalize(resultDF, resultDF, "nNonSci", 0, 3, "nNonSci")
  
  resultDF <- eng_prof(resultDF, rawdata, "Eng prof")
  resultDF <- normalize(resultDF, resultDF, "Eng prof", 0, 2, "Eng prof")
  resultDF <- normalize(resultDF, rawdata, "Year of Study", 1, 4, "Year of Study")
  resultDF <- binarize(resultDF, rawdata, "Faculty", NA, c("ART", "CCST", "EDU","SLAW","SSF"), "Faculty_Art")
  resultDF <- binarize(resultDF, rawdata, "Faculty", NA, c("BASCI", "ENF", "ENSCF", "MED", "SCF"), "Faculty_Sci")
  resultDF <- binarize(resultDF, rawdata, "Faculty", NA, c("BAF", "BASCI", "BASSF"), "Faculty_Bus")
  resultDF <- gradeToDec(resultDF, rawdata, "Grade", "Grade_dec")
  resultDF <- normalize(resultDF, rawdata, "cGPA (Before)", 0, 4, "cGPA (Before)")
  resultDF[rawdata[, "cGPA (Before)"] == 0 & rawdata[, "Enrollment Term"] == "1516T1" & rawdata[, "Year of Study"] == 1, "cGPA (Before)"] <- NA
  resultDF <- binarize(resultDF, rawdata, "Medium of Instruction", NA, "Cantonese", "Medium_Can")
  resultDF <- binarize(resultDF, rawdata, "Medium of Instruction", NA, "English", "Medium_Eng")
  resultDF <- binarize(resultDF, rawdata, "Medium of Instruction", NA, "Putonghua", "Medium_Put")
  resultDF <- binarize(resultDF, rawdata, "First GEF?", "No", NA, "First GEF")
  
  
  resultDF <- textToDec(resultDF, rawdata, "Q18 (Assigned Text Read)", "Q18 (Assigned Text Read)")
  resultDF <- textToDec(resultDF, rawdata, "Q19 (Chinese Translation)", "Q19 (Chinese Translation)")
  resultDF <- percentToDec(resultDF, rawdata, "Q20 (Text/week)", "Q20 (Text/week)")
  resultDF <- timeToDec(resultDF, rawdata, "Q21 (Time/week)", "Q21 (Time/week)")
  resultDF <- percentToDec(resultDF, rawdata, "Q22 (% Lecture)", "Q22 (% Lecture)")
  # Eliminate records with NA values
  resultDF <- resultDF[rowSums(is.na(resultDF)) == 0, ]
  return(resultDF)
}
resultDF <- preprocess()
write.csv(resultDF, file = "./nn_grade_prediction/preprocessed_witheffort.csv", row.names = FALSE)