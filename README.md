# GEStatProj

## How to "Install"
1. Download all files above
2. Place the csv file containing students' response into the same directory of inputCSV.R
3. Open inputCSV.R by RStudio
4. In line 4:
```
rawdata <- read.csv("1415T2 Data (0924 version_ for student trial).csv", header = TRUE, sep = ",", na.strings = c("N/A"), check.names = FALSE, stringsAsFactors = FALSE)
```
substitute "1415T2 Data (0924 version_ for student trial).csv" by your own csv file name.
5. Run the script
