library(RPostgreSQL)
library(ggplot2)
library(lubridate)
library(dplyr)
library(ggthemes)

drv <- dbDriver("PostgreSQL")
source("connect/connect.R")

intersection_id = 1

strSQL <-
  paste0("SELECT intersection_name FROM miovision.intersections WHERE intersection_uid = ",intersection_id)
intersection_name <- dbGetQuery(con, strSQL)

strSQL <-
  paste0("SELECT datetime_bin, classification, leg, dir, volume ",
         "FROM miovision.volumes_15min ",
         "INNER JOIN miovision.classifications USING (classification_uid) ",
         "WHERE intersection_uid = ",intersection_id," ",
         "ORDER BY datetime_bin, classification_uid, leg, dir ")
data <- dbGetQuery(con, strSQL)


all_vehicles <- data %>%
  group_by(datetime_bin, leg, dir) %>%
  filter(classification %in% c('Lights','Single-Unit Trucks','Articulated Trucks','Buses')) %>%
  summarize(total_volume = sum(volume))
head(all_vehicles)

all_vehicles$dt <- floor_date(all_vehicles$datetime_bin,'1 day')
all_vehicles$time_bin <- as.POSIXct(paste(sprintf("%02d",hour(all_vehicles$datetime_bin)),sprintf("%02d",minute(all_vehicles$datetime_bin)),sep=":"), format = "%H:%M")
all_vehicles$wk <- strftime(all_vehicles$dt,format='%W')
all_vehicles$dow <- strftime(all_vehicles$dt, format = '%u')

for (leg in c('N','S','W','E')){
  for (dir in c('NB','SB','EB','WB')){
    if (((leg %in% c('N','S')) && (dir %in% c('NB','SB'))) | ((leg %in% c('E','W')) && (dir %in% c('EB','WB')))){
      subset <- all_vehicles[all_vehicles$dir == dir & all_vehicles$leg == leg,]
      dates <- data.frame(label = unique(all_vehicles$dt))
      dates$dow <- strftime(dates$lab, format = '%u')
      dates$wk <- strftime(dates$lab, format = '%W')
      dates$x = as.POSIXct('06:00', format = '%H:%M')
      dates$y = 0.975 * max(subset$total_volume)
      
      ggplot(data = subset, aes(x=time_bin, y=total_volume)) +
        geom_line(aes(color = ifelse(dow < 6, "weekday", "weekend")), size = 1) +
        scale_colour_brewer(type = 'qua', palette = "Set1", direction = -1) +
        scale_x_datetime(date_labels = "%H", date_breaks = "2 hours") +
        facet_grid(wk ~ dow) +
        geom_text(data = dates, aes(x,y-0.5,label=label)) +
        theme_light() + 
        guides(color = F) +
        labs(title = paste0(intersection_name,": ", leg, " leg, ", dir, " direction"))
    }
  }
}