library(ggplot2)

#mirror hist
for(i in 2:ncol(demographic))
{
  data=as.data.frame(table(demographic[,c(1,i),drop=F]))
  data$Freq[which(data$Outside.Class.Activity=="OD")]=-1*data$Freq[which(data$Outside.Class.Activity=="OD")]
  png(paste(varname[i],"mirrored hist",".png"))
  print(
    ggplot(data,aes(x=data[,2],y=Freq,fill=Outside.Class.Activity))+geom_bar(stat="identity",position = "identity")+
      coord_flip()+
      labs(x=varname[i],y="Frequency",fill=varname[1]))
  dev.off()
}

elec_count=c(-apply(subset(elec,game=="OD"),2,function(x){length(which(!is.na(x)))}),apply(subset(elec,game=="Civ4"),2,function(x){length(which(!is.na(x)))}))
data=data.frame("Outside Class Activity"=factor(rep(c("OD","Civ4"),each=14),levels = c("OD","Civ4"),labels = c("OD","Civ4")),
                "Elective"=rep(c("Phy", "Chem", "Bio", "Com Sci", "Inter Sci", "Eng Lit", "Chin Lit", "Hist", "Chin Hist", "Ethics & RS", "Music", "Visual Art", "Econ", "Geog"),times=2),
                "Freq"=elec_count)
png("High School Electives mirrored hist.png")
ggplot(data,aes(x=data[,2],y=Freq,fill=Outside.Class.Activity))+geom_bar(stat="identity",position = "identity")+coord_flip()+labs(x="Elective",y="Frequency",fill="Outside Class Activity")
dev.off()


#grouped hist
for(i in 2:ncol(demographic))
{ 
  png(paste(varname[i],"grouped hist",".png"))
  print(
    ggplot(demographic, aes(x=demographic[,i], fill=Outside.Class.Activity))+
      geom_bar(stat="count",  position="dodge")+
      coord_flip()+
      labs(x=varname[i],y="Frequency",fill=varname[1]))
  dev.off()
}

elec_count=c(apply(subset(elec,game=="OD"),2,function(x){length(which(!is.na(x)))}),apply(subset(elec,game=="Civ4"),2,function(x){length(which(!is.na(x)))}))
data=data.frame("Outside Class Activity"=factor(rep(c("OD","Civ4"),each=14),levels = c("OD","Civ4"),labels = c("OD","Civ4")),
                "Elective"=rep(c("Phy", "Chem", "Bio", "Com Sci", "Inter Sci", "Eng Lit", "Chin Lit", "Hist", "Chin Hist", "Ethics & RS", "Music", "Visual Art", "Econ", "Geog"),times=2),
                "Freq"=elec_count)
png("High School Electives grouped hist.png")
ggplot(data, aes(x=Elective, y=Freq, fill=Outside.Class.Activity))+geom_bar(stat="identity",  position="dodge")+coord_flip()+labs(x="Elective",y="Frequency",fill="Outside Class Activity")
dev.off()