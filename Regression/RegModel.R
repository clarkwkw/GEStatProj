library(dplyr)
source("functions.R")

uge <- read.csv(file = "201516T1T2TS.csv", 
               na.strings = c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"))
uge <- tbl_df(uge)

gradeToPoint <- function(response) {
  grade <- c('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F')
  point <- c(4.0,  3.7,  3.3, 3.0,  2.7,  2.3, 2.0,  1.7,  1.3, 1.0, 0.0)
  quantify(response, choice = grade, converted_num = point)
}

# not a good model, probably violate assumption of normal distributed error term
fit <- 
    uge %>% 
        # also filter out NA in cGPA (Before)
        filter(!is.na(Grade) & cGPA..Before. != 0) %>%  
        mutate(GradePoint = gradeToPoint(Grade)) %>%
    #    select(cGPA..Before., Grade, GradePoint) %>%
        lm(GradePoint ~ cGPA..Before., data = .)

# visualise
plot(fit$model[2:1])
abline(fit, col='red')

# access model
plot(fit)
