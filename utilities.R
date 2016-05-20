#This func is to merge two dataframes containing two columns: "Tag Number" & "Reason"
mergeInvalidDF <- function(a, b){
  merge(a, b, by = c("Tag Number", "Reason"), all=TRUE)
}

#check data in data frame in a specified column (colname)
#compare it with pre-specified range of values (rng, a list)
#return a data frame of invalid records with tag number and colname
checkdata <- function(df, rng, colname){
  isNAValue = any(rng == "N/A", na.rm = TRUE)
  rng <- rng[rng != "" & rng != "N/A" & !is.na(rng)]
  if(length(levels(rng)))rng <- levels(droplevels(rng))
  else rng <- c(rng)
  if (isNAValue) rng <- c(rng, NA)
  tmpdf <- df[which(names(df) %in% c(colname, "Tag Number"))]
  tmpdf <- tmpdf[(tmpdf[[colname]] %in% rng) == FALSE, "Tag Number", drop = FALSE]
  if(nrow(tmpdf))tmpdf[["Reason"]] = colname
  return (tmpdf)
}