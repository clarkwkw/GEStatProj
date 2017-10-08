chisqtest=NULL
pval=NULL

#3,5,6,8 warning due to small proportion
for(i in 2:(ncol(demographic)))
{
  temp=chisq.test(table(demographic[,c(1,i)]))
  chisqtest=append(chisqtest,list(temp))
  pval=c(pval,temp$p.value)
}

names(chisqtest)=names(demographic)[-1]
names(pval)=names(demographic)[-1]
