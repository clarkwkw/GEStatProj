# GEStatProj

## How to "Install"
1. Download all files above
2. Place the csv file containing students' response into the same directory of inputCSV.R
3. In RStudio, set the working directory by `setwd("%path%")`, where %path% is the path to inputCSV.R
3. Open inputCSV.R by RStudio
4. In line 4: 
`rawdata <- read.csv("xxxxx.csv"...`
, substitute "xxxxx.csv" by your own csv file name
5. Run the script.

## percentageTable.R
* Please install package `ggplot2` before calling the function.

For details, please refer to the [wiki page] (https://github.com/clarkwkw/GEStatProj/wiki/percentageTable.R).

## correlation-maxGroupByQuestion.R
Please refer to the [wiki page] (https://github.com/clarkwkw/GEStatProj/wiki/correlation-maxGroupByQuestion.R).

## correlation-bf.R
Please refer to the [wiki page] (https://github.com/clarkwkw/GEStatProj/wiki/Brute-Force-Search-Algorithm-for-Correlation).
