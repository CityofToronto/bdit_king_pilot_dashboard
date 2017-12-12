library(RPostgreSQL)
library(rjson)
library(dplyr)
library(lubridate)
library(ggplot2)
library(ggthemes)

########################################
# CONNECT TO POSTGRESQL
########################################
drv <- dbDriver("PostgreSQL")
source("connect/connect.R")

########################################
########################################

line_number <- 504

strSQL <- paste0("SELECT trip_start::date AS dt, EXTRACT(hour FROM trip_start) AS HOUR, COUNT(*) as trips, ceil(COUNT(*)/8.0) AS trips_cat ",
"FROM (SELECT date_key, trip_id, MIN(departure_datetime) AS trip_start FROM ttc.pointstop WHERE line_number = ", line_number," GROUP BY date_key, trip_id) AS X ",
"GROUP BY trip_start::date, EXTRACT(hour FROM trip_start) ",
"ORDER BY trip_start::date, EXTRACT(hour FROM trip_start)")
all_trips <- dbGetQuery(con, strSQL)
all_trips$hour <- all_trips$hour + 0.5
all_trips$trips_cat <- as.factor(all_trips$trips_cat)
all_trips$weekday <- ifelse(wday(all_trips$dt) %in% c(2,3,4,5,6), 1, 0)

ggplot(data = all_trips, aes(y = hour, x = dt)) +
  geom_tile(aes(fill = trips_cat, alpha = weekday), colour = "white") +
  scale_fill_brewer(palette = "YlGnBu", type = "seq") +
  geom_text(aes(label = trips), colour = "white") +
  theme_hc() +
  scale_x_date(date_minor_breaks = "1 day", date_labels = "%a %b %d") +
  scale_y_continuous(breaks = seq(0,24,2)) +
  theme(legend.position="none")
