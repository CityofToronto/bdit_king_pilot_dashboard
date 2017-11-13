library(dplyr)
library(magrittr)

df <- 
  do.call(rbind,
          lapply(list.files(".",".csv"), header = T, sep = ";", stringsAsFactors = F, row.names = NULL, read.csv))

df$Timestamp <- as.POSIXct(df$Timestamp, format ="%b %d, %Y %I:%M:%S %p")
df$Timestamp <- df$Timestamp - 5*60

agg <- 
df %>%
  group_by(StartPointName, EndPointName, Timestamp = cut(Timestamp, breaks = "30 min")) %>%
  summarize(obs = sum(SampleCount), tt = sum(MedianMeasuredTime*SampleCount)/sum(SampleCount))

write.csv(agg, "agg.csv")
# intervals <- ISOdatetime(2017,11,12,0,0,0) + seq(0:95)*30*60
