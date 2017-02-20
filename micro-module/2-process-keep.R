# read data and remove invalid entry
# total valid entry = 116
# variables available after reading:
# rawdata       : without invalid entry, others same
# keep_used     : factor "Yes" or "No"
# keep_response : 1 or NA (blank) for option a to g
# keep_option   : full description for option a to g
# tag           : valid entry (their tag num)
source("1-read-keep.R")

# --------- ~ functions ~ -----------
# response are data with possible values specified in choice
# choice, converted_num are same length,
#   as if a lookup data when rbind
# retrun : same length as response, transformed to numbers
quantify <- function(response, choice, converted_num) {
  sapply(as.factor(response), function(x) converted_num[which(x == choice)])
}

# ------- ~ Basic Stat/Graph ~ --------
# KEEP usage count ----
table(keep_used)

# Reason not using KEEP ----
s <- colSums(keep_response, na.rm = T)
sx <- barplot(s, main = "Reason of not using KEEP", xlab = "option", ylab = "count", ylim = c(0, 80))
text(x = sx, y = s, label = s, pos = 3, cex = 0.8, col = "red")
keep_option

# Text read ----
text_read_option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
text_read_num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)
text_read_response <- rawdata$Q18
chi_read_response <- rawdata$Q19

t <- table(text_read_response)[text_read_option]
tx <- barplot(t, main = "Text Read", ylab = "count", ylim = c(0, 45))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Chinese text read ----
t <- table(chi_read_response)[text_read_option]
tx <- barplot(t, main = "Chinese Text Read", ylab = "count", ylim = c(0, 45))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of text read ----
text_read_response <- quantify(text_read_response, text_read_option, text_read_num)
names(text_read_response) <- tag
mean(text_read_response)

# Mean of Chinese text read ----
chi_read_response <- quantify(chi_read_response, text_read_option, text_read_num)
names(chi_read_response) <- tag
mean(chi_read_response)

# RJ time ----
rj_time_option <- levels(as.factor(rawdata$Q20))[c(5,2:4,1,6)]
rj_time_num <- c(0.5, 2, 4.5, 8, 12.5, 16)
rj_time_response <- rawdata$Q20

t <- table(rj_time_response)[rj_time_option]
tx <- barplot(t, main = "Time spent on RJ", ylab = "count", ylim = c(0, 60))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of RJ time ----
rj_time_response <- quantify(rj_time_response, rj_time_option, rj_time_num)
names(rj_time_response) <- tag
mean(rj_time_response)

# Text Reading time ----
text_time_option <- levels(as.factor(rawdata$Q21))[c(5,1:4,6)]
text_time_num <- c(0.5, 1.5, 2.5, 3.5, 4.5, 6)
text_time_response <- rawdata$Q21

t <- table(text_time_response)[text_time_option]
tx <- barplot(t, main = "Time spent on Text Reading", ylab = "count", ylim = c(0, 60))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of Text Reading time ----
text_time_response <- quantify(text_time_response, text_time_option, text_time_num)
names(text_time_response) <- tag
mean(text_time_response)

# Attendance ----
attend_option <- levels(as.factor(rawdata$Q22))
attend_num <- c(0, .10, .30, .50, .70, .90)

lec_attend_response <- factor(rawdata$Q22, levels = attend_option)
tut_attend_response <- factor(rawdata$Q23, levels = attend_option)

t <- table(lec_attend_response)
tx <- barplot(t, main = "Lecture attendance", ylab = "count", ylim = c(0, 110))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

t <- table(tut_attend_response)
tx <- barplot(t, main = "Tutorial attendance", ylab = "count", ylim = c(0, 110))
text(x = tx, y = t, label = t, pos = 3, cex = 0.8, col = "red")

# Mean of Lecture Attendance ----
lec_attend_response <- quantify(lec_attend_response, attend_option, attend_num)
names(lec_attend_response) <- tag
mean(lec_attend_response)

# Mean of Tutorial Attendance ----
tut_attend_response <- quantify(tut_attend_response, attend_option, attend_num)
names(tut_attend_response) <- tag
mean(tut_attend_response)

# ---------- ~ Course Engagement ~ --------------
# Text read by KEEP usage ----
# difference in text read for student used / didnt used keep
# (no significant result)
t.test(text_read_response ~ keep_used)

# Chinese Text read by KEEP usage ----
# difference in chinese text read for student used / didnt used keep
# (no significant result)
t.test(chi_read_response ~ keep_used)

# Text read by busy ----
# difference in text read for student responsed / didnt response busy
# (no significant result)
busy <- keep_response$e %in% 1
names(busy) <- tag
t.test(text_read_response ~ busy)

# Chinese text read by busy ----
# difference in chinese text read for student responsed / didnt response busy
# (no significant result)
busy <- keep_response$e %in% 1
names(busy) <- tag
t.test(chi_read_response ~ busy)

# Time spent on RJ by KEEP usage ----
# difference in time spent on RJ for students used / didnt used KEEP
# (no significant result)
t.test(rj_time_response ~ keep_used)

# Time spent of Text Reading by KEEP usage ----
# difference in time spent on text reading for students used / didnt used KEEP
# (no significant result)
t.test(text_time_response ~ keep_used)

# Lecture/Tutorial attendance by KEEP usage ----
# difference in attendance for students used / didnt used KEEP
# (no significant result)
t.test(lec_attend_response ~ keep_used)
t.test(tut_attend_response ~ keep_used)

# -------- ~ Student Background ~ -----------
# KEEP usage by Sex ----
table(rawdata$Sex, keep_used)[, 2:1]
# prop 1 = used KEEP among female
# prop 2 = used KEEP among male
# (** significant : usage of KEEP is greater among female than among male)
prop.test(table(rawdata$Sex, keep_used)[, 2:1])

# KEEP usage by English Proficiency ----
table(rawdata$`English Proficiency`, keep_used)[1:2, 2:1]
# prop 1 = used KEEP among DSE 4 or below
# prop 2 = used KEEP among DSE 5 or above
# (** significant : usage of KEEP is greater among 
#     students with higher English proficiency)
# But there are many Cantonese videos in KEEP
prop.test(table(rawdata$`English Proficiency`, keep_used)[1:2, 2:1])

# KEEP usage by Sci taken ----
subject <- !is.na(rawdata[, 74:87])
n_sci_taken <- apply(subject[, 1:5], MARGIN = 1, sum)
sci_taken <- n_sci_taken > 0

table(n_sci_taken, keep_used)[, 2:1]
table(sci_taken, keep_used)[2:1, 2:1]
# prop 1 = used KEEP among students who did take sci subj
# prop 2 = used KEEP among students who didnt take sci subj
# (warning : inaccurate test (anyway no significant result),
#  probably because of small sample size for non-sci students)
prop.test(table(sci_taken, keep_used)[2:1, 2:1])

# KEEP usage by Non-sci taken ----
subject <- !is.na(rawdata[, 74:87])
n_ns_taken <- apply(subject[, 6:14], MARGIN = 1, sum)
ns_taken <- n_ns_taken > 0

table(n_ns_taken, keep_used)[, 2:1]
table(ns_taken, keep_used)[2:1, 2:1]
# prop 1 = used KEEP among students who did take non-sci subj
# prop 2 = used KEEP among students who didnt take non-sci subj
# (no significant result)
prop.test(table(ns_taken, keep_used)[2:1, 2:1])

# KEEP usage by Art taken ----
subject <- !is.na(rawdata[, 74:87])
n_art_taken <- apply(subject[, 6:12], MARGIN = 1, sum)
art_taken <- n_art_taken > 0

table(n_art_taken, keep_used)[, 2:1]
table(art_taken, keep_used)[2:1, 2:1]
# prop 1 = used KEEP among students who did take art subj
# prop 2 = used KEEP among students who didnt take art subj
# (warning : inaccurate test (anyway no significant result),
#  probably because of small sample size for art students)
prop.test(table(art_taken, keep_used)[2:1, 2:1])

# KEEP usage by Econ taken ----
subject <- !is.na(rawdata[, 74:87])
econ_taken <- subject[, 13]

table(econ_taken, keep_used)[2:1, 2:1]
# prop 1 = used KEEP among students who did take Econ
# prop 2 = used KEEP among students who didnt take Econ
# (no significant result)
prop.test(table(econ_taken, keep_used)[2:1, 2:1])
