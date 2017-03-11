# read data and remove invalid entry
# total valid entry = 116
# variables available after reading:
# rawdata       : without invalid entry, others same
# keep_used     : factor "Yes" or "No"
# keep_response : 1 or NA (blank) for option a to g
# keep_option   : full description for option a to g
# tag           : valid entry (their tag num)
source("1-read-keep.R")
source("functions.R")

# ------- ~ Basic Stat/Graph ~ --------
# KEEP usage count ----
table(keep_used)

# Reason not using KEEP ----
s <- colSums(keep_response, na.rm = T)
sx <- barplot(s, main = "Reason of not using KEEP", xlab = "option", ylab = "count", ylim = c(0, 400))
text(x = sx, y = s, label = s, pos = 3, cex = 0.8, col = "red")
keep_option

# Text read ----
text_read_option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
text_read_num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)
text_read_response <- rawdata$Q18
chi_read_response <- rawdata$Q19

t <- table(text_read_response)[text_read_option]
tx <- barplot(t, main = "Text Read", ylab = "count", ylim = c(0, 400))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Chinese text read ----
t <- table(chi_read_response)[text_read_option]
tx <- barplot(t, main = "Chinese Text Read", ylab = "count", ylim = c(0, 400))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of text read ----
text_read_response <- rawdata$Q18
names(text_read_response) <- tag
text_read_response <- text_read_response[text_read_response != "12"]
text_read_response <- quantify(removeNA(text_read_response), text_read_option, text_read_num)
mean(text_read_response)

# Mean of Chinese text read ----
chi_read_response <- rawdata$Q19
names(chi_read_response) <- tag
chi_read_response <- quantify(removeNA(chi_read_response), text_read_option, text_read_num)
mean(chi_read_response)

# RJ time ----
rj_time_option <- levels(as.factor(rawdata$Q20))[c(5,2:4,1,6)]
rj_time_num <- c(0.5, 2, 4.5, 8, 12.5, 16)
rj_time_response <- rawdata$Q20

t <- table(rj_time_response)[rj_time_option]
tx <- barplot(t, main = "Time spent on RJ", ylab = "count", ylim = c(0, 400))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of RJ time ----
rj_time_response <- rawdata$Q20
names(rj_time_response) <- tag
rj_time_response <- quantify(removeNA(rj_time_response), rj_time_option, rj_time_num)
mean(rj_time_response)

# Text Reading time ----
text_time_option <- levels(as.factor(rawdata$Q21))[c(5,1:4,6)]
text_time_num <- c(0.5, 1.5, 2.5, 3.5, 4.5, 6)
text_time_response <- rawdata$Q21

t <- table(text_time_response)[text_time_option]
tx <- barplot(t, main = "Time spent on Text Reading", ylab = "count", ylim = c(0, 400))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of Text Reading time ----
names(text_time_response) <- tag
text_time_response <- quantify(removeNA(text_time_response), text_time_option, text_time_num)
mean(text_time_response)

# Attendance ----
attend_option <- levels(as.factor(rawdata$Q22))
attend_num <- c(0, .10, .30, .50, .70, .90)

lec_attend_response <- factor(rawdata$Q22, levels = attend_option)
tut_attend_response <- factor(rawdata$Q23, levels = attend_option)

t <- table(lec_attend_response)
tx <- barplot(t, main = "Lecture attendance", ylab = "count", ylim = c(0, 800))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

t <- table(tut_attend_response)
tx <- barplot(t, main = "Tutorial attendance", ylab = "count", ylim = c(0, 800))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of Lecture Attendance ----
names(lec_attend_response) <- tag
lec_attend_response <- quantify(removeNA(lec_attend_response), attend_option, attend_num)
mean(lec_attend_response)

# Mean of Tutorial Attendance ----
names(tut_attend_response) <- tag
tut_attend_response <- quantify(removeNA(tut_attend_response), attend_option, attend_num)
mean(tut_attend_response)

# ---------- ~ Course Engagement ~ --------------
# Text read by KEEP usage ----
# difference in text read for student used / didnt used keep
# ** 95% CI for (Not_used - used) = (-1.23, -0.47)
t.test(text_read_response ~ keep_used[names(text_read_response)])

# Chinese Text read by KEEP usage ----
# difference in chinese text read for student used / didnt used keep
# ** 95% CI for (Not_used - used) = (-1.22, -0.08)
t.test(chi_read_response ~ keep_used[names(chi_read_response)])

# Text read by busy ----
# difference in text read for student responsed / didnt response busy
# ** 95% CI for (Not_busy - busy) = (0.13, 0.86)
busy <- keep_response$e %in% 1
names(busy) <- tag
t.test(text_read_response ~ busy[names(text_read_response)])

# Chinese text read by busy ----
# difference in chinese text read for student responsed / didnt response busy
# ** 95% CI for (Not_busy - busy) = (0.08, 1.05)
busy <- keep_response$e %in% 1
names(busy) <- tag
t.test(chi_read_response ~ busy[names(text_read_response)])

# Time spent on RJ by KEEP usage ----
# difference in time spent on RJ for students used / didnt used KEEP
# ** 95% CI for (Not_used - used) = (-1.45, -0.15)
t.test(rj_time_response ~ keep_used[names(rj_time_response)])

# Time spent of Text Reading by KEEP usage ----
# difference in time spent on text reading for students used / didnt used KEEP
# (no significant result)
t.test(text_time_response ~ keep_used[names(text_time_response)])

# Lecture/Tutorial attendance by KEEP usage ----
# difference in attendance for students used / didnt used KEEP

# ** 95 CI for (Not_used - used) = (-14%, -5%)
#                for 12 lectures ~ (-1.6, -0.6)
t.test(lec_attend_response ~ keep_used[names(lec_attend_response)])
# (no significant result)
t.test(tut_attend_response ~ keep_used[names(tut_attend_response)])

# -------- ~ Student Background ~ -----------
# KEEP usage by Sex ----
table(rawdata$Sex, keep_used)[, 2:1]
# prop 1 = used KEEP among female
# prop 2 = used KEEP among male
# (no significant result)
prop.test(table(rawdata$Sex, keep_used)[, 2:1])

# KEEP usage by Faculty ----
table(rawdata$Faculty, keep_used)[, 2:1]
prop.table(table(rawdata$Faculty, keep_used)[, 2:1], margin = 1)
# (no significant result)
prop.test(table(rawdata$Faculty, keep_used)[
  c("ART", "BAF", "EDU", "ENF", "MED", "SCF", "SLAW", "SSF"), 2:1])

# KEEP usage by first/second GE
table(rawdata$`First GEF?`, keep_used)[3:2, 2:1]
# prop 1 = First GE
# prop 2 = second GE
# (no significant result)
prop.test(table(rawdata$`First GEF?`, keep_used)[3:2, 2:1])

# KEEP usage by English Proficiency ----
table(rawdata$`English Proficiency`, keep_used)[1:2, 2:1]
# prop 1 = used KEEP among DSE 4 or below
# prop 2 = used KEEP among DSE 5 or above
# (no significant result)
prop.test(table(rawdata$`English Proficiency`, keep_used)[1:2, 2:1])

# KEEP usage by Sci taken ----
n_sci_taken <- rawdata$`ScienceSubject`
sci_taken <- n_sci_taken > 0

table(n_sci_taken, keep_used)[, 2:1]
table(sci_taken, keep_used)[2:1, 2:1]
# prop 1 = used KEEP among students who did take sci subj
# prop 2 = used KEEP among students who didnt take sci subj
# (no significant result)
prop.test(table(sci_taken, keep_used)[2:1, 2:1])


# KEEP usage by Humanities taken ----
n_hum_taken <- rawdata$`HumanitiesSub`
hum_taken <- n_hum_taken > 0

table(n_hum_taken, keep_used)[, 2:1]
table(hum_taken, keep_used)[2:1, 2:1]
# prop 1 = used KEEP among students who did take humanities subj
# prop 2 = used KEEP among students who didnt take humanities subj
# (no significant result)
prop.test(table(hum_taken, keep_used)[2:1, 2:1])

# ----------- ~ Learning Outcomes ~ ----------
# Analysis by 5 Categories
category <- list(G1 = c(1, 3, 4, 5)
               , G2 = c(6, 7, 8)
               , G3 = c(9, 10, 11, 12)
               , G4 = c(13, 15)
               , G5 = c(2, 14, 16, 17))

cat_description <- c(G1 = "Logical Thinking and Communication Skills"
                   , G2 = "Appreciation of Science"
                   , G3 = "Understanding of Science"
                   , G4 = "Understanding of Good Life and Society"
                   , G5 = "Appreciation of Diversity")

change <- rawdata[grep("Change", colnames(rawdata))]

# mean of change (after - before) in general by categories
# all positive change
# maximum change = G3 (~ 1)
c(  G1 = mean(as.matrix(change[, category$G1]), na.rm = T)
  , G2 = mean(as.matrix(change[, category$G2]), na.rm = T)
  , G3 = mean(as.matrix(change[, category$G3]), na.rm = T)
  , G4 = mean(as.matrix(change[, category$G4]), na.rm = T)
  , G5 = mean(as.matrix(change[, category$G5]), na.rm = T))

# calculate mean of change for each category,
# then compare between students used / didn't use KEEP

# G1 to G4 : no significant result
t.test(rowMeans(change[, category$G1], na.rm = T) ~ keep_used)
t.test(rowMeans(change[, category$G2], na.rm = T) ~ keep_used)
t.test(rowMeans(change[, category$G3], na.rm = T) ~ keep_used)
t.test(rowMeans(change[, category$G4], na.rm = T) ~ keep_used)
# ** 95% CI for (Not_used - used) = (-0.26, -0.05)
t.test(rowMeans(change[, category$G5], na.rm = T) ~ keep_used)

# ----------- ~ Social Presence ~ -----------
# Communication preference (Q28, Q29) ----
face <- rawdata$Q28
names(face) <- tag
face <- removeNA(face)

online <- rawdata$Q29
names(online) <- tag
online <- removeNA(online)

diff <- rawdata$Q28 - rawdata$Q29
names(diff) <- tag
diff <- removeNA(diff)

# face-to-face preference by KEEP usage
# difference in preference to face-to-face communication
# (no significant result)
t.test(face ~ keep_used[names(face)])

# online preference by KEEP usage
# diff in preference to online communication
# ** 95% CI for (Not_used - used) = (-0.33, -0.11)
# (students who used KEEP give higher mark)
t.test(online ~ keep_used[names(online)])

# diff in marks of face-to-face and online given by same person
# ** 95% CI for paired marks diff = (0.004, 0.121)
# (face-to-face mark > online mark)
t.test(diff, mu = 0)

# diff in marks for students used KEEP
# (no significant result)
t.test(split(diff, keep_used[names(diff)])$Yes, mu = 0)

# diff in marks for students didnt use KEEP
# ** 95% CI for paired marks diff = (0.04, 0.17)
t.test(split(diff, keep_used[names(diff)])$No, mu = 0)

# ------------ ~ Grade / GPA ~ -------------
grade_outcome <- c("A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F")
grade_num     <- c(4.0, 3.7,  3.3,  3.0, 2.7,  2.3,  2.0, 1.7,  1.3,  1.0, 0.0)

# GEF grade by KEEP usage ----
grade <- rawdata$Grade
names(grade) <- tag
grade <- as.factor(subset(grade, !(grade %in% c(""))))
grade <- quantify(grade, grade_outcome, grade_num)

# diff in GE grade for students used / didn't used KEEP
# ** 95% CI for (Not_used - used) = (-0.206, -0.035)
t.test(grade ~ keep_used[names(grade)])

# cGPA (After) by KEEP usage ----
cgpa <- rawdata$`cGPA (After)`
names(cgpa) <- tag

# diff in cGPA after taking GEF for students used / didn't used KEEP
# (no significant result)
t.test(cgpa ~ keep_used[names(cgpa)])
