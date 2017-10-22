library(ggplot2)

#mirror hist
varname=names(demographic)
for(i in 2:ncol(demographic))
{
  data=as.data.frame(table(demographic[,c(1,i),drop=F]))
  data$Freq[which(data$Outside.Class.Activity=="OD")]=-1*data$Freq[which(data$Outside.Class.Activity=="OD")]
  png(paste(varname[i],"mirrored hist",".png"))
  print(
    ggplot(data,aes(x=data[,2],y=Freq,fill=Outside.Class.Activity))+geom_bar(stat="identity",position = "identity")+
      labs(x=varname[i],y="Frequency",fill=varname[1])+
      scale_y_continuous(labels=abs)+
      coord_flip()+
      ggtitle(varname[i])+
      theme(plot.title = element_text(face="bold",size=24)))
  dev.off()
}

elec_count=c(-apply(subset(elec,game=="OD"),2,function(x){length(which(!is.na(x)))}),apply(subset(elec,game=="Civ4"),2,function(x){length(which(!is.na(x)))}))
data=data.frame("Outside Class Activity"=factor(rep(c("OD","Civ4"),each=14),levels = c("OD","Civ4"),labels = c("OD","Civ4")),
                "Elective"=rep(c("Phy", "Chem", "Bio", "Com Sci", "Inter Sci", "Eng Lit", "Chin Lit", "Hist", "Chin Hist", "Ethics & RS", "Music", "Visual Art", "Econ", "Geog"),times=2),
                "Freq"=elec_count)
png("High School Electives mirrored hist.png")
ggplot(data,aes(x=data[,2],y=Freq,fill=Outside.Class.Activity))+geom_bar(stat="identity",position = "identity")+
  scale_y_continuous(labels=abs)+
  coord_flip()+
  labs(x="Elective",y="Frequency",fill="Outside Class Activity")+
  ggtitle("High School Electives")+
  theme(plot.title = element_text(face="bold",size=24))
dev.off()

varname=paste("Q",18:35,sep = "")
for(i in 1:ncol(part2to3))
{
  data=as.data.frame(table(cbind(demographic[,1,drop=F],part2to3[,i,drop=F])))
  data$Freq[which(data$Outside.Class.Activity=="OD")]=-1*data$Freq[which(data$Outside.Class.Activity=="OD")]
  png(paste(varname[i],"mirrored hist",".png"))
  print(
    ggplot(data,aes(x=data[,2],y=Freq,fill=Outside.Class.Activity))+geom_bar(stat="identity",position = "identity")+
      labs(x=varname[i],y="Frequency",fill="Outside Class Activity")+
      scale_y_continuous(labels=abs)+
      coord_flip()+
      ggtitle(varname[i])+
      theme(plot.title = element_text(face="bold",size=24)))
  dev.off()
}

varname=names(grade)
for(i in 1:ncol(grade))
{
  if(i==2)
  {
    data=as.data.frame(table(cbind(demographic[,1,drop=F],grade[,i,drop=F])))
    data$Freq[which(data$Outside.Class.Activity=="OD")]=-1*data$Freq[which(data$Outside.Class.Activity=="OD")]
  }
  else
  {
    data=as.data.frame(table(cbind(demographic[,1,drop=F],cut(grade[,i],1:12/12*4))))
    data$Freq[which(data$Outside.Class.Activity=="OD")]=-1*data$Freq[which(data$Outside.Class.Activity=="OD")]
  }
  png(paste(varname[i],"mirrored hist",".png"))
  print(
    ggplot(data,aes(x=data[,2],y=Freq,fill=Outside.Class.Activity))+geom_bar(stat="identity",position = "identity")+
      labs(x=varname[i],y="Frequency",fill="Outside Class Activity")+
      scale_y_continuous(labels=abs)+
      coord_flip()+
      ggtitle(varname[i])+
      theme(plot.title = element_text(face="bold",size=24)))
  dev.off()
}
