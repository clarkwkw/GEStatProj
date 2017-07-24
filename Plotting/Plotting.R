library(dplyr)
library(ggplot2)

uge <- read.csv(file = "201617T1 - 2017.07.24 ver.csv", 
                na.strings = c("NA", "BLANK", "", "MULT", "ERROR #3100", "#VALUE!", "#N/A", "Not Asked"))
uge <- tbl_df(uge)

uge <- uge %>%
  filter(!is.na(Q18.Converted)) %>%  # Text Read
  filter(!is.na(Q20.Converted)) %>%  # RJ Time
  filter(!is.na(Q21.Converted)) %>%  # Time per text
  filter(!is.na(Q22.Converted)) %>%  # Attended Lec Hr
  filter(!is.na(Q23.Converted)) %>%  # Attended Tut Hr
  filter(!is.na(Grade.Point))
  
uge <- uge %>% mutate(Effort = Q18.Converted * Q21.Converted + 
                               Q20.Converted + Q22.Converted + Q23.Converted)

# Visualise distribution of Grade
p <- uge %>% ggplot(aes(x=Grade)) + geom_bar()
p + scale_x_discrete(limits=c("F","D","D+","C-","C","C+","B-","B","B+","A-","A")) +
  labs(title='Distribution of Grade')

# Visualise distribution of Effort
uge %>% ggplot(aes(x=Effort)) + geom_histogram(binwidth=7, fill='white', colour='black') + 
  labs(title='Distribution of Effort', x='Effort (hours)')

# GradePoint vs. Effort Plot
uge %>% ggplot(aes(x=Effort, y=Grade.Point)) + geom_point() +
  labs(title='Grade Point vs. Effort', y='Grade Point', x='Effort (hours)')

# GradePoint vs. Effort Plot (with color by faculty)
uge %>% ggplot(aes(x=Effort, y=Grade.Point)) + geom_point(aes(colour=Faculty)) +
  labs(title='Grade Point vs. Effort', y='Grade Point', x='Effort (hours)')
