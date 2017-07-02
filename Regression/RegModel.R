library(dplyr)
source("functions.R")

gradeToPoint <- function(response) {
  grade <- c('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F')
  point <- c(4.0,  3.7,  3.3, 3.0,  2.7,  2.3, 2.0,  1.7,  1.3, 1.0, 0.0)
  quantify(response, choice = grade, converted_num = point)
}

# calculate intended learning outcome by mean of each group
# any group with all NA => remove that row
# extend the original dataset by columns G1 - G5
calGroup <- function(raw) {
  # Q1 - Q17 responses at entry
  surveyRsp <- raw %>% select(matches("Q.*Before"))
  groupCat <- list(G1 = c(1,3,4,5),
                   G2 = c(6,7,8),
                   G3 = c(9,10,11,12),
                   G4 = c(13,15), 
                   G5 = c(2,14,16,17))
  
  # ignore NA, calculate mean of other questions in that group
  groupMean <- do.call(cbind, lapply(groupCat, function(i) rowMeans(surveyRsp[, i], na.rm = T))) 
  # remove row with mean NA
  cbind(raw, groupMean) %>%
    filter(!is.na(G1) & !is.na(G2) & !is.na(G3) & !is.na(G4) & !is.na(G5))
}

# dataset for constructing the model ----
uge <- read.csv(file = "201516T1T2TS.csv", 
               na.strings = c("NA", "BLANK", "", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"))
uge <- tbl_df(uge)

uge <- calGroup(uge)

# not a good model, probably violate assumption of normal distributed error term
fit <- 
    uge %>% 
        # also filter out NA in cGPA (Before)
        filter(!is.na(Grade) & cGPA..Before. != 0) %>%  
        mutate(GradePoint = gradeToPoint(Grade)) %>%
        lm(GradePoint ~ cGPA..Before. + G1 + G2 + G3 + G4 + G5, data = .)

# # access model
# plot(fit)

# dataset for testing the model ----
testData <- read.csv(file = "201617T1.csv", 
                    na.strings = c("NA", "BLANK", "", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"))
testData <- tbl_df(testData)

testData <- calGroup(testData)

testData <- 
  testData %>% 
  # also filter out NA in cGPA (Before)
  filter(!is.na(Grade) & cGPA..Before. != 0) %>%  
  mutate(GradePoint = gradeToPoint(Grade))

# # use the test data instead of the previous data to contruct the model
# fit2 <-
#   testData %>%
#   # also filter out NA in cGPA (Before)
#   filter(!is.na(Grade) & cGPA..Before. != 0) %>%
#   mutate(GradePoint = gradeToPoint(Grade)) %>%
#   lm(GradePoint ~ cGPA..Before. + G1 + G2 + G3 + G4 + G5, data = .)

predictGP <- predict(fit, testData)
# root mean square error
rms <- (predictGP - testData$GradePoint)^2 %>% mean %>% sqrt
