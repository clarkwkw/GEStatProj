#----write a function to attach the correlation coefficients and the correlation and the hypothesis test results in the graph


# parameters x and y refer to x and y-axes respectively, "digits" refer to the digitals of the values, 
# "method" refers type of correlation used, where the ellipsis means graphical parameters as arguments to plot function
upperpanel.cor <- function(x, y, digits = 4, method = "pearson", ...) {
  
  # set the frame and a fixed coordinates for the plots from the matrix of scatterplots
  # "usr" means the extremes of the plots
  # "on.exit" makes sure the "usr" would not change no matter how the plotting parameters are automatically adjusted in a function
  usr <- par("usr"); on.exit(par(usr))
  # set the extremes of the plot
  par(usr = c(0, 1, 0, 1))
  
  # correlation coefficient
  r <- cor(x, y, method = method, use="na.or.complete")
  txt <- format(c(r), digits = digits)[1]
  txt <- paste("r= ", txt, sep = "")
  text(0.5, 0.6, txt)
  
  # p-value calculation
  p <- cor.test(x, y, method = method, use="na.or.complete")$p.value
  txt2 <- format(c(p), digits = digits)[1]
  txt2 <- paste("p= ", txt2, sep = "")
  if(p<0.01) txt2 <- paste("p= ", "<0.01", sep = "")
  text(0.5, 0.4, txt2)
}

lowerpanel.cor <- function(x, y, ...) {
  df <- data.frame(x, y)
  
  ## Use densCols() output to get density at each point
  x <- densCols(x, y, colramp=colorRampPalette(c("black", "white")))
  df$dens <- col2rgb(x)[1,] + 1L
  
  ## Map densities to colors
  cols <-  colorRampPalette(c("#000099", "#00FEFF", "#45FE4F", 
                              "#FCFF00", "#FF9400", "#FF3100"))(256)
  df$col <- cols[df$dens]
  points(x~y, data=df[order(df$dens),], pch=20, col=col, cex=2)
}

MyGray <- rgb(t(col2rgb("black")), alpha=25, maxColorValue=255)
#pairs(rawdata[4:10], xlim= c(-4,6), ylim=c(-4,6), upper.panel = upperpanel.cor, lower.panel= lowerpanel.cor)
corrplot(cor(rawdata[4:54], use="na.or.complete"), type="upper", tl.col="black", tl.srt=45)

