Exploratory Analysis - Miovision Counts
================
Aakash Harpalani
Thursday, December 14, 2017

### Setup

Loading libraries:

``` r
library(RPostgreSQL)
library(ggplot2)
library(lubridate)
library(dplyr)
```

Establishing connections and credentials:

``` r
drv <- dbDriver("PostgreSQL")
source("connect/connect.R")
```

### Analysis

Set intersection(s) of interest:

``` r
intersection_ids = seq(1,31,1)
```

Retrieve 15-min count data:

``` r
strSQL <-
  paste0("SELECT datetime_bin, intersection_name, classification, leg, dir, volume ",
         "FROM miovision.volumes_15min ",
         "INNER JOIN miovision.classifications USING (classification_uid) ",
         "INNER JOIN miovision.intersections USING (intersection_uid) ",
         "ORDER BY datetime_bin, intersection_name, classification_uid, leg, dir ")
data <- dbGetQuery(con, strSQL)
```

Overall volumes, by date/tod

``` r
all_vehicles <- data %>%
  group_by(datetime_bin, intersection_name, leg, dir) %>%
  filter(classification %in% c('Lights','Single-Unit Trucks','Articulated Trucks','Buses')) %>%
  summarize(total_volume = sum(volume))
head(all_vehicles)
```

    ## Source: local data frame [6 x 5]
    ## Groups: datetime_bin, intersection_name, leg [3]
    ## 
    ##          datetime_bin intersection_name   leg   dir total_volume
    ##                <dttm>             <chr> <chr> <chr>        <int>
    ## 1 2017-10-03 13:15:00   King / Bathurst     E    EB           81
    ## 2 2017-10-03 13:15:00   King / Bathurst     E    WB           74
    ## 3 2017-10-03 13:15:00   King / Bathurst     N    NB          142
    ## 4 2017-10-03 13:15:00   King / Bathurst     N    SB          118
    ## 5 2017-10-03 13:15:00   King / Bathurst     S    NB          133
    ## 6 2017-10-03 13:15:00   King / Bathurst     S    SB          106

``` r
all_vehicles$dt <- floor_date(all_vehicles$datetime_bin,'1 day')
all_vehicles$time_bin <- as.POSIXct(paste(sprintf("%02d",hour(all_vehicles$datetime_bin)),sprintf("%02d",minute(all_vehicles$datetime_bin)),sep=":"), format = "%H:%M")
all_vehicles$wk <- strftime(all_vehicles$dt,format='%W')
all_vehicles$dow <- strftime(all_vehicles$dt, format = '%u')
```

Plot all direction/leg combinations (Adelaide and Bathurst):

``` r
for (intersection_id in intersection_ids){
  
  strSQL <-
    paste0("SELECT intersection_name FROM miovision.intersections WHERE intersection_uid = ",intersection_id)
  intersection_name <- as.character(dbGetQuery(con, strSQL))

  print(paste0(intersection_id,': ', intersection_name))
  
  for (leg in c('N','S','W','E')){
    for (dir in c('NB','SB','EB','WB')){
      if (((leg %in% c('N','S')) && (dir %in% c('NB','SB'))) | ((leg %in% c('E','W')) && (dir %in% c('EB','WB')))){
        subset <- all_vehicles[all_vehicles$dir == dir 
                               & all_vehicles$leg == leg 
                               & all_vehicles$intersection_name == intersection_name,]
        dates <- data.frame(label = unique(all_vehicles$dt))
        dates$dow <- strftime(dates$lab, format = '%u')
        dates$wk <- strftime(dates$lab, format = '%W')
        dates$x = as.POSIXct('04:00', format = '%H:%M')
        dates$y = max(0.96 * max(subset$total_volume), 0.95)
        
        print(ggplot(data = subset, aes(x=time_bin, y=total_volume)) +
          geom_line(aes(color = ifelse(dow < 6, "weekday", "weekend")), size = 1) +
          scale_colour_brewer(type = 'qua', palette = "Set1", direction = -1) +
          scale_x_datetime(date_labels = "%H", date_breaks = "2 hours") +
          facet_grid(dow ~ wk) +
          geom_text(data = dates, aes(x,y-0.5,label=label)) +
          theme_light() + 
          guides(color = F) +
          theme(aspect.ratio = 1/2) +
          labs(title = paste0(intersection_name,": ", leg, " leg, ", dir, " direction")),
          width = 700, height = 1400)
      }
    }
  }
}
```

    ## [1] "1: Adelaide / Bathurst"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-1.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-2.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-3.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-4.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-5.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-6.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-7.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-8.png)

    ## [1] "2: Adelaide / Spadina"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-9.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-10.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-11.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-12.png)

    ## Warning in max(subset$total_volume): no non-missing arguments to max;
    ## returning -Inf

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-13.png)

    ## Warning: Unknown or uninitialised column: 'PANEL'.

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-14.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-15.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-16.png)

    ## [1] "3: Adelaide / Bay"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-17.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-18.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-19.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-20.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-21.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-22.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-23.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-24.png)

    ## [1] "4: Adelaide / Jarvis"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-25.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-26.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-27.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-28.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-29.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-30.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-31.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-32.png)

    ## [1] "5: Front / Bathurst"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-33.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-34.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-35.png)

    ## Warning in max(subset$total_volume): no non-missing arguments to max;
    ## returning -Inf

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-36.png)

    ## Warning: Unknown or uninitialised column: 'PANEL'.

    ## Warning: no non-missing arguments to max; returning -Inf

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-37.png)

    ## Warning: Unknown or uninitialised column: 'PANEL'.

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-38.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-39.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-40.png)

    ## [1] "6: Front / Spadina"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-41.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-42.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-43.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-44.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-45.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-46.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-47.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-48.png)

    ## [1] "7: Front / Bay"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-49.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-50.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-51.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-52.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-53.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-54.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-55.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-56.png)

    ## [1] "8: Front / Jarvis"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-57.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-58.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-59.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-60.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-61.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-62.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-63.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-64.png)

    ## [1] "9: King / Strachan"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-65.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-66.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-67.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-68.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-69.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-70.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-71.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-72.png)

    ## [1] "10: King / Bathurst"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-73.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-74.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-75.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-76.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-77.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-78.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-79.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-80.png)

    ## [1] "11: King / Portland"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-81.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-82.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-83.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-84.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-85.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-86.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-87.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-88.png)

    ## [1] "12: King / Spadina"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-89.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-90.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-91.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-92.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-93.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-94.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-95.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-96.png)

    ## [1] "13: King / Peter"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-97.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-98.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-99.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-100.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-101.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-102.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-103.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-104.png)

    ## [1] "14: King / Simcoe"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-105.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-106.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-107.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-108.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-109.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-110.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-111.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-112.png)

    ## [1] "15: King / University"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-113.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-114.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-115.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-116.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-117.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-118.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-119.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-120.png)

    ## [1] "16: King / York"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-121.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-122.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-123.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-124.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-125.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-126.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-127.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-128.png)

    ## [1] "17: King / Bay"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-129.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-130.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-131.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-132.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-133.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-134.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-135.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-136.png)

    ## [1] "18: King / Yong"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-137.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-138.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-139.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-140.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-141.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-142.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-143.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-144.png)

    ## [1] "19: King / Church"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-145.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-146.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-147.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-148.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-149.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-150.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-151.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-152.png)

    ## [1] "20: King / Jarvis"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-153.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-154.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-155.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-156.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-157.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-158.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-159.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-160.png)

    ## [1] "21: King / Sherbourne"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-161.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-162.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-163.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-164.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-165.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-166.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-167.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-168.png)

    ## [1] "22: Queen / Bathurst"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-169.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-170.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-171.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-172.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-173.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-174.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-175.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-176.png)

    ## [1] "23: Queen / Spadina"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-177.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-178.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-179.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-180.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-181.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-182.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-183.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-184.png)

    ## [1] "24: Queen / Bay"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-185.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-186.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-187.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-188.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-189.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-190.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-191.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-192.png)

    ## [1] "25: Queen / Jarvis"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-193.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-194.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-195.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-196.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-197.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-198.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-199.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-200.png)

    ## [1] "26: Richmond / Bathurst"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-201.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-202.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-203.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-204.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-205.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-206.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-207.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-208.png)

    ## [1] "27: Richmond / Spadina"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-209.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-210.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-211.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-212.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-213.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-214.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-215.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-216.png)

    ## [1] "28: Richmond / Bay"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-217.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-218.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-219.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-220.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-221.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-222.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-223.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-224.png)

    ## [1] "29: Richmond / Jarvis"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-225.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-226.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-227.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-228.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-229.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-230.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-231.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-232.png)

    ## [1] "30: Wellington / Blue Jays"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-233.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-234.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-235.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-236.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-237.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-238.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-239.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-240.png)

    ## [1] "31: Wellington / Bay"

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-241.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-242.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-243.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-244.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-245.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-246.png)

    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?
    ## geom_path: Each group consists of only one observation. Do you need to
    ## adjust the group aesthetic?

![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-247.png)![](exploratory_analysis_files/figure-markdown_github/unnamed-chunk-6-248.png)
