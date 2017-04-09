# file for functions definition

# response are data with possible values specified in choice
# choice, converted_num are same length,
#   as if a lookup table when rbind
# retrun : same length as response, transformed to numbers
quantify <- function(response, choice, converted_num) {
  result <- sapply(as.factor(response), function(x) converted_num[which(x == choice)])
  names(result) <- names(response)
  result
}

# only keep non-NA entry
removeNA <- function(x) {
  x[!is.na(x)]
}

# l = list of test
log.test <- function(l, filepath, test.names = NULL) {
  r <- Reduce(function(result, test) result <- rbind(result, unlist(test)), l, init = NULL)
  rownames(r) <- test.names
  write.csv(r, file = filepath)
}