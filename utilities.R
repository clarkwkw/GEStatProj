# This func is to read csv/xslx file by respective function
# To read xlsx file, please install openxlsx library first
readData <- function(file, ...){
  # Split file names by dot
  fileNames <- strsplit(file, "\\.")[[1]]
  if(length(fileNames) < 2){
    stop("File name without extension")
  }
  
  # Check file extension
  ext <- fileNames[length(fileNames)]
  if(tolower(ext) == "csv"){
    return (read.csv(file, header = TRUE, sep = ",", stringsAsFactors = FALSE, ...))
  }else if(tolower(ext) == "xlsx"){
    library("openxlsx")
    df <- openxlsx::read.xlsx(file, sheet = 1, ...)
    # In openxlsx, spaces in column names are automatically converted to dots
    # which is not desirable, so convert it back
    colnames(df)<-gsub("\\.", " ", colnames(df))
    return(df)
  }else{
    stop("Unrecognized file extension")
  }
}

#This func. is to merge two dataframes containing two columns: "Tag Number" & "Column Name"
mergeInvalidDF <- function(a, b){
  merge(a, b, by = c("Tag Number", "Column Name"), all=TRUE)
}

#check data in a specified column (colname) of dataframe (df)
#compare it with pre-specified range of values (rng, a list)
#return a data frame of invalid records with tag number and column name
checkdata <- function(df, rng, colname){
  #record N/A value of rng seperately
  #isNAValue = any(rng == "NA", na.rm = TRUE) KMK note: redundant line
  
  #remove all invalid values of rng
  rng <- rng[rng!="" & !is.na(rng)]

  #try to vectorize rng, if it is factor, use method 1. Otherwise, method 2
  if(length(levels(rng)))
    rng <- levels(droplevels(rng)) # method 1
  else
    rng <- c(rng) #method 2
  
  #try to convert rng vector to numeric if possible
  numericConvertible <- FALSE
  if(all(suppressWarnings(!is.na(as.numeric(rng))))){
    rng<-as.numeric(rng)
    numericConvertible <- TRUE
  } 
  
  #add the NA value back to the rng vector if necessary
  #if (isNAValue) KMK note: do not want to count those recognized NA values in the invalid list
  rng <- c(rng, NA)
  
  #extract related columns from df
  tmpdf <- df[which(names(df) %in% c(colname, "Tag Number"))] 
  
  #If the values in the specific column is not one of the values specified in rng, the record is invalid
  #Tag Numbers of invalid records are extracted
  tmpdf <- tmpdf[(tmpdf[[colname]] %in% rng) == FALSE, "Tag Number", drop = FALSE]
  
  #If no. of invalid records > 0, set their column names
  if(nrow(tmpdf)) 
    tmpdf[["Column Name"]] = colname
  
  #Set invalid cells in rawdata to NA 
  #KMK note: this line is buggy
  #df[(df[[colname]] %in% rng) == FALSE,colname] <- NA
  
  #Some columns are saved as factor, remove unused levels if applicable
  if(length(levels(df[[colname]])))
    df[[colname]] <- droplevels(df[[colname]])
  
  #Some columns can be converted into numeric
  #KMK note: this line is buggy. It curiously generates extra columns in the rawdata
  #if(numericConvertible){
  #  df[,colname] <- as.numeric(df[,colname])
  #}
  rawdata<<-df
  return (tmpdf)
}

#Example: generateRecordsByTeacher(rawdata, "df", "") will generate those dataframes:
#df_Amber, df_Andy, df_Balwin, ...
#while generateRecordsByTeacher(rawdata, "", "data") will generate
#Amber_data, Andy_data, Balwin_data, ...
generateRecordsByTeacher <- function(df, dfPrefix = "", dfSuffix = ""){
  #Split the orginal dataframe according to teachers' names, dfs will be a list of dataframes
  dfs <- split(df, f = df$"Name")
  
  #For each dataframe in the dfs list, assign it to a global variable, whose name is dfPrefix_(teacher name)
  #Invisible() is for hiding the return value from appearing in console
  invisible(lapply(dfs, function(x){
    #initialize dfname to the teacher's name
      dfname<-x[1, "Name"]
      
      #if dfPrefix is not an empty string, append it to dfname
      if(dfPrefix != "")
        dfname<-paste(dfPrefix, dfname, sep="_")
      
      #if dfSuffix is not an empty string, append it to dfname
      if(dfSuffix != "")
        dfname<-paste(dfname, dfSuffix, sep="_")
      
      #assign dataframe as a dataframe global variable whose name is dfname
      assign(dfname, x, envir = .GlobalEnv)
  }))
}

#Convert strings that contain numbers to numeric
#If any element in dfCol cannot be converted, the conversion will be cancelled
chartoNumeric <- function(dfCol){
  if(mode(dfCol[1]) == "character"){
    
    #Check if all elements (except NA values) are convertible to numeric
    if(all(suppressWarnings(!is.na(as.numeric(dfCol[!is.na(dfCol)]))))){
      
      #Convert to numeric
      dfCol<-suppressWarnings(as.numeric(dfCol))
    }
  }
  return (dfCol)
}

#This func can extract all columns in df that contains numeric values
getNumericMatrix <- function (df){
  #For every columns in df, check if it is numeric, if it is not, turn all of its values to NA
  df <- lapply(df, function(x){
    if(mode(x[1]) == "numeric"){
      return(x)
    }
    return (NA)
  })
  #Combine the result generated above
  df <- as.data.frame(df, check.names = FALSE, stringsAsFactors = FALSE)
  
  #Remove all columns that only contain NAs (i.e. non-numeric columns)
  df <- df[, colSums(is.na(df)) != nrow(df), drop = FALSE]
  
  #Finally, convert the dataframe into matrix
  df <- data.matrix(df, rownames.force = TRUE)
  return (df)
}

getFullRows <- function(df){
  return(df[rowSums(is.na(df) | df == "")  == 0,])
}

createDir <- function(dir){
  return(ifelse(!dir.exists(file.path(getwd(), dir)), dir.create(file.path(getwd(), dir)), TRUE))
  
}