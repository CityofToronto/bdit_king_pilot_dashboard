library(RPostgreSQL)
library(tidyr)
library(dplyr)
library(plyr)
library(ggplot2)
library(ggthemes)
library(xts)
library(lubridate)

################################
# IMPORT FROM POSTGRESQL
################################
drv <- dbDriver("PostgreSQL")
source("connect/connect.R")

strSQL <-
  paste0("SELECT * FROM king_pilot.bt_ttc_tt WHERE end_dt::date NOT IN ('2017-10-09')")
data <- dbGetQuery(con, strSQL)
data$end_dt = data$end_dt - hours(5)

bt_id <- 64

data_wkday <- data[(data$bt_id == bt_id) & (format(data$end_dt,"%w") %in% c(1,2,3,4,5)), ]
data_wkday$time_only <- as.POSIXct(as.numeric(as.POSIXct(data_wkday$end_dt)) %% 86400, origin = "2000-01-01", tz = "GMT")
data_wkday$time_bin <- as.POSIXct(floor(as.numeric(data_wkday$time_only) / (30 * 60)) * (30 * 60), origin='1970-01-01', tz = "GMT")

data_wkday_agg <- aggregate(tt_sec ~ time_bin, data_wkday, mean)
data_wkday_agg$time_only <- data_wkday_agg$time_bin

plot1 <- ggplot(data_wkday, aes(x = time_only, y = tt_sec/60.0)) +
  geom_point(color = "#8da0cb", size = 2.5, alpha = 0.5) + 
  geom_line(size = 2, alpha = 1, data = data_wkday_agg, color = "#0e57ce") +
  scale_x_datetime(date_breaks = "1 hours", date_labels = "%H", limits = c(as.POSIXct("2000-01-01") - hours(5),as.POSIXct("2000-01-02") - hours(5))) +
  theme_hc() +
  theme(text = element_text(size = 16)) +
  labs(y = "Travel Time (mins)", x= "Hour of Day")
plot1
