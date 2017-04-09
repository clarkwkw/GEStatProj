# ---- ~ Read and extract data ~ ----
source("1-read-keep.R")
source("functions.R")

# for both assigned text and chi text, need change for UGFH
text_read_option <- c("0 to 1", "2 to 3", "4 to 5", "6 to 7", "8 to 9", "10 to 11")
text_read_num <- c(0.5, 2.5, 4.5, 6.5, 8.5, 10.5)

text_read_response <- rawdata$Q18
names(text_read_response) <- tag
text_read_response <- text_read_response[text_read_response != "12"]
text_read_response <- quantify(removeNA(text_read_response), text_read_option, text_read_num)

chi_read_response <- rawdata$Q19
names(chi_read_response) <- tag
chi_read_response <- quantify(removeNA(chi_read_response), text_read_option, text_read_num)

rj_time_option <- c("less than 1", "1 to <3", "3 to <6", "6 to <10", "10 to <15", "more than 15")
rj_time_num <- c(0.5, 2, 4.5, 8, 12.5, 16)
rj_time_response <- rawdata$Q20
names(rj_time_response) <- tag
rj_time_response <- quantify(removeNA(rj_time_response), rj_time_option, rj_time_num)

text_time_option <- c("less than 1", "1 to <2", "2 to <3", "3 to <4", "4 to <5", "more than 5")
text_time_num <- c(0.5, 1.5, 2.5, 3.5, 4.5, 6)
text_time_response <- rawdata$Q21
names(text_time_response) <- tag
text_time_response <- quantify(removeNA(text_time_response), text_time_option, text_time_num)

attend_option <- c("0", "1-20%", "21-40%", "41-60%", "61-80%", "81-100%")
attend_num <- c(0, .10, .30, .50, .70, .90)

lec_attend_response <- factor(rawdata$Q22, levels = attend_option)
names(lec_attend_response) <- tag
lec_attend_response <- quantify(removeNA(lec_attend_response), attend_option, attend_num)

tut_attend_response <- factor(rawdata$Q23, levels = attend_option)
names(tut_attend_response) <- tag
tut_attend_response <- quantify(removeNA(tut_attend_response), attend_option, attend_num)

# ---- ~ Log t-test by KEEP usage to csv ~ ----
l <- NULL  # list of test
n <- NULL  # name of test
t.test(text_read_response ~ keep_used[names(text_read_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Text Read")

t.test(chi_read_response ~ keep_used[names(chi_read_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Chi Read")

t.test(rj_time_response ~ keep_used[names(rj_time_response)])
l <- append(l, list(.Last.value))
n <- append(n, "RJ Time")

t.test(text_time_response ~ keep_used[names(text_time_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Time Per Reading")

t.test(lec_attend_response ~ keep_used[names(lec_attend_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Lecture Attendance")

t.test(tut_attend_response ~ keep_used[names(tut_attend_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Tutorial Attendance")


category <- list(G1 = c(1, 3, 4, 5)
                 , G2 = c(6, 7, 8)
                 , G3 = c(9, 10, 11, 12)
                 , G4 = c(13, 15)
                 , G5 = c(2, 14, 16, 17))
change <- rawdata[grep("Change", colnames(rawdata))]

t.test(rowMeans(change[, category$G1], na.rm = T) ~ keep_used)
l <- append(l, list(.Last.value))
n <- append(n, "Outcome G1")

t.test(rowMeans(change[, category$G2], na.rm = T) ~ keep_used)
l <- append(l, list(.Last.value))
n <- append(n, "Outcome G2")

t.test(rowMeans(change[, category$G3], na.rm = T) ~ keep_used)
l <- append(l, list(.Last.value))
n <- append(n, "Outcome G3")

t.test(rowMeans(change[, category$G4], na.rm = T) ~ keep_used)
l <- append(l, list(.Last.value))
n <- append(n, "Outcome G4")

t.test(rowMeans(change[, category$G5], na.rm = T) ~ keep_used)
l <- append(l, list(.Last.value))
n <- append(n, "Outcome G5")

face <- rawdata$Q28
names(face) <- tag
face <- removeNA(face)
t.test(face ~ keep_used[names(face)])
l <- append(l, list(.Last.value))
n <- append(n, "Prefer face-to-face")

online <- rawdata$Q29
names(online) <- tag
online <- removeNA(online)
t.test(online ~ keep_used[names(online)])
l <- append(l, list(.Last.value))
n <- append(n, "Prefer Online")

grade_outcome <- c("A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F")
grade_num     <- c(4.0, 3.7,  3.3,  3.0, 2.7,  2.3,  2.0, 1.7,  1.3,  1.0, 0.0)
grade <- rawdata$Grade
names(grade) <- tag
grade <- as.factor(subset(grade, !(grade %in% c(""))))
grade <- quantify(grade, grade_outcome, grade_num)
t.test(grade ~ keep_used[names(grade)])
l <- append(l, list(.Last.value))
n <- append(n, "Course Grade")

cgpa <- rawdata$`cGPA (After)`
names(cgpa) <- tag
t.test(cgpa ~ keep_used[names(cgpa)])
l <- append(l, list(.Last.value))
n <- append(n, "cGPA")

log.test(l, filepath = "result/ttest_by_keep.csv", test.names = n)

# ---- ~ Log test of KEEP used proportion ~ ----
l <- NULL
n <- NULL
prop.test(table(rawdata$Sex, keep_used)[, 2:1])
l <- append(l, list(.Last.value))
n <- append(n, "Female/Male")

prop.test(table(rawdata$`First GEF?`, keep_used)[3:2, 2:1])
l <- append(l, list(.Last.value))
n <- append(n, "First/Second GE")

prop.test(table(rawdata$`English Proficiency`, keep_used)[1:2, 2:1])
l <- append(l, list(.Last.value))
n <- append(n, "DSE Eng Low/High")

n_sci_taken <- rawdata$`ScienceSubject`
sci_taken <- n_sci_taken > 0
prop.test(table(sci_taken, keep_used)[2:1, 2:1])
l <- append(l, list(.Last.value))
n <- append(n, "Taken/Not Taken Sci")

n_hum_taken <- rawdata$`HumanitiesSub`
hum_taken <- n_hum_taken > 0
prop.test(table(hum_taken, keep_used)[2:1, 2:1])
l <- append(l, list(.Last.value))
n <- append(n, "Taken/Not Taken Humanity")

log.test(l, filepath = "result/keep_proportion.csv", test.names = n)

# --- ~ Log t-test by busy to csv ~ ----
busy <- keep_response$e %in% 1
names(busy) <- tag
l <- NULL
n <- NULL

t.test(text_read_response ~ busy[names(text_read_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Text Read")

t.test(chi_read_response ~ busy[names(text_read_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Chi Read")

t.test(rj_time_response ~ busy[names(rj_time_response)])
l <- append(l, list(.Last.value))
n <- append(n, "RJ Time")

t.test(text_time_response ~ busy[names(text_time_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Time Per Reading")

t.test(lec_attend_response ~ busy[names(lec_attend_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Lecture Attendance")

t.test(tut_attend_response ~ busy[names(tut_attend_response)])
l <- append(l, list(.Last.value))
n <- append(n, "Tutorial Attendance")

log.test(l, filepath = "result/ttest_by_busy.csv", test.names = n)

