# need to install package plyr
library(plyr)

# Import csv file, auto-convert N/A as NA, preserve original column names
rawdata <- read.csv("201617T1_KMKonly_data.csv", header = TRUE, sep = ",", na.strings=c("NA", "BLANK", "MULT", "ERROR #3100", "#VALUE!", "Not Asked"), check.names = FALSE, stringsAsFactors = FALSE)
# Remove empty rows
rawdata <- rawdata[rowSums(is.na(rawdata) | rawdata == "") != ncol(rawdata),]

# description for Q46_no_a to Q46_no_g
keep_option <- c(  a = "lack of promotion"
                 , b = "unrelated to course grade"
                 , c = "materials not interesting"
                 , d = "difficult to access"
                 , e = "too busy"
                 , f = "knowledge acquired elsewhere"
                 , g = "others")

# data on micro-modules
keep_used <- rawdata$Q46
names(keep_used) <- rawdata$`Tag number`
keep_used <- revalue(factor(keep_used), c("0" = "No", "1" = "Yes"))

# remove those who did not attempt Q46
# (removed tag number 47)
valid_response <- !is.na(keep_used)
rawdata <- subset(rawdata, valid_response)
keep_used <- subset(keep_used, valid_response)

keep_response <- rawdata[, 101:107]
colnames(keep_response) <- letters[1:7]

count_blank <- apply(keep_response, MARGIN = 1, function(r) sum(is.na(r)))
all_blank <- count_blank == length(keep_option)
# # show num of valid/invalid response
# table(all_blank, keep_used)

# invalid if used keep but not all blank (tag 17, 74); or
# did not used keep but all blank (tag 84)

# remove invalid response (by their tag number)
invalid_tag <- c(names(which(keep_used == "Yes" & !all_blank))
               , names(which(keep_used == "No"  &  all_blank)))
rawdata <- subset(rawdata, !(rownames(rawdata) %in% invalid_tag))
keep_used <- subset(keep_used, !(names(keep_used) %in% invalid_tag))
keep_response <- subset(keep_response, !(rownames(keep_response) %in% invalid_tag))

tag <- rownames(rawdata)

# will not use these var anymore
rm(all_blank, count_blank, invalid_tag, valid_response)

