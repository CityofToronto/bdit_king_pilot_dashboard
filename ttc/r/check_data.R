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
# HEATMAPS - Check for Coverage Gaps
########################################

line_number <- 504

strSQL <- paste0("SELECT trip_start::date AS dt, EXTRACT(hour FROM trip_start) AS HOUR, COUNT(*) as trips, ceil(COUNT(*)/10.0) AS trips_cat ",
"FROM (SELECT date_key, trip_id, MIN(departure_datetime) AS trip_start FROM ttc.pointstop WHERE line_number = ", line_number," GROUP BY date_key, trip_id) AS X ",
"GROUP BY trip_start::date, EXTRACT(hour FROM trip_start) ",
"ORDER BY trip_start::date, EXTRACT(hour FROM trip_start)")
all_trips <- dbGetQuery(con, strSQL)
all_trips$hour <- all_trips$hour + 0.5
all_trips$trips_cat <- as.factor(all_trips$trips_cat)
all_trips$weekday <- ifelse(wday(all_trips$dt) %in% c(2,3,4,5,6), 1, 0)
all_trips[all_trips$dt == '2017-10-09',]$weekday <- 0

weekdays <- ggplot(data = all_trips[all_trips$weekday == 1, ], aes(y = hour, x = dt)) +
  geom_tile(aes(fill = trips_cat), colour = "white") +
  scale_fill_brewer(palette = "Blues", type = "seq", direction = 1) +
  geom_text(aes(label = trips), colour = "lightgrey", size = 1.5) +
  theme_hc() +
  scale_x_date(date_minor_breaks = "1 day", date_labels = "%a %b %d") +
  scale_y_reverse(breaks = seq(0,24,4), limits = c(24,4)) +
  theme(legend.position="none",
        panel.grid.major = element_line(colour = "#708090",size = 0.3),
        axis.ticks = element_line(colour = "#708090", size = 0.3),
        axis.title.x = element_text(size = 9, colour = "black"),
        axis.text.x = element_text(size = 7, colour = "#708090"),
        axis.title.y = element_text(size = 9, colour = "black", hjust = 1),
        axis.text.y = element_text(size = 7, colour = "#708090"),
        plot.title = element_text(size = 12, colour = "black"),
        plot.subtitle = element_text(size = 8, colour = "#708090")) +
  labs(title = paste0(ifelse(line_number==501,"Queen","King")," Streetcar (",line_number,") - Weekday Temporal Coverage"), subtitle = "Number of Trips Started, by Hour",
       x = "Date", y = "Time of Day (Hour)")
ggsave(paste0(line_number,"_weekdays.png"), weekdays, width = 8, height = 4, units = "in", dpi = 300)

weekends <- ggplot(data = all_trips[all_trips$weekday == 0, ], aes(y = hour, x = dt)) +
  geom_tile(aes(fill = trips_cat), colour = "white") +
  scale_fill_brewer(palette = "Blues", type = "seq", direction = 1) +
  geom_text(aes(label = trips), colour = "lightgrey", size = 1.5) +
  theme_hc() +
  scale_x_date(date_minor_breaks = "1 day", date_labels = "%a %b %d") +
  scale_y_reverse(breaks = seq(0,24,4), limits = c(24,4)) +
  theme(legend.position="none",
        panel.grid.major = element_line(colour = "#708090",size = 0.3),
        axis.ticks = element_line(colour = "#708090", size = 0.3),
        axis.title.x = element_text(size = 9, colour = "black"),
        axis.text.x = element_text(size = 7, colour = "#708090"),
        axis.title.y = element_text(size = 9, colour = "black", hjust = 1),
        axis.text.y = element_text(size = 7, colour = "#708090"),
        plot.title = element_text(size = 12, colour = "black"),
        plot.subtitle = element_text(size = 8, colour = "#708090")) +
  labs(title = paste0(ifelse(line_number==501,"Queen","King")," Streetcar (",line_number,") - Weekend/Holiday Temporal Coverage"), subtitle = "Number of Trips Started, by Hour",
       x = "Date", y = "Time of Day (Hour)")
ggsave(paste0(line_number,"_weekends.png"), weekends, width = 8, height = 4, units = "in", dpi = 300)
