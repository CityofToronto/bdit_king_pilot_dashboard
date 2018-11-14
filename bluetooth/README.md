# Bluetooth Travel Time Data
BlipTrack sensors have been installed in a grid at major intersections in the Pilot area. They detect the unique IDs of Bluetooth devices as they pass by and measure the travel time between two sensors for each detected device.


## Data Aggregation

To aggregate the Bluetooth data, the travel times were aggregated with:
1. The median of 5-minute bins
2. The weighted average of 30-minute bins
3. The average of time periods
4. The sum over a given corridor, typically from Bathurst to Jarvis.

### Baseline Determination

The following plots were used to determine which dates and observations to use in determining the base line:
1. Dot graphs of 30-min travel times over a week
2. 24-hour line plot averaging 30-min bins, with quintile bands
3. 24-hour line plot averaging 30-min bins, with and without outliers removed
4. For weeks with significant outliers, a Weekly dot graph with percentile bands and outliers identified. 

With the level of aggregation decided, scatter plots of the 30-minute data were created for each segment and divided into weekly subplots. The plots were all checked to ensure the data was contiguous and sane.

Meanwhile, in the [baseline lookover notebook](baseline%20lookover.ipynb), each segment's 24-hour baseline was plotted with quintile bands for the segment's 30 minute aggregated data over 24 hours. These plots were used to identify outliers that had an impact on the baselines. Outliers that shifted the baseline beyond the 20-80 percentile band were noted for further investigation.

The third type of plot was put together to analyze the impact of removing a date from a given baseline. This plot showed the new baseline overlaid on the old baseline to demonstrate the effect of removing the outlier. It was determined that removing dates with outliers from the baseline could have an impact on the quality of the data. 

Finally, for each baseline with notable outliers, a scatter plot was produced for the weeks the outliers were found. The percentile band plots were shown for reference, now with the 100th percentile shown as x's, and the last band showing up to the 90th percentile. 

Lastly, the baseline comparison graphs were plotted with the outlying dates removed from the new baseline. Each of these sets of figures was analyzed to see if the outlier's impact on the baseline was great enough to warrant it's removal. 

Entire dates were removed as outliers if they had a large effect on the baseline unless the outlier:
 - didn't have a large impact on the baseline, 
 - had an impact outside peak hours,
 - had unpredictable effects on the baseline outside of the outlier's timeperiod

When looking at the travel time scatterplot for Queen Street University to Yonge, a major change in travel times was noticed at midnight on Saturday, September 30th. The baseline for Saturday was examined using the percentile band plot, and it looked like the event significantly impacted the baseline, pulling it beyond the 10-90 percentile band, and forming a slight upwards trend where no such trend is reflected in the bulk of the data. Because of this, the original baseline was compared to a new baseline with September 30th and October 1st removed, and the new weekend baseline was significantly lower during early morning and midnight. Finally, it was learned that the event occurred during Nuit Blanche, and the Bluetooth readers likely picked up pedestrian phones as there were no cars on the street. Even though this didn't affect the data during peak hours, its impact on the baseline was so large it was excluded from the baseline data. 

The dates excluded for specific road segments include: 
1. September 24th, on Queen University to Yonge, for a travel time during midday 2 - 3 times longer than any other during that day.
2. September 30th and October 1st on Queen, Universtiy to Yonge, Eastbound and Westbound, for Nuit Blanche.
3. September 19th on Queen Spadina to Bathurst for a travel time around 21:30 of over 2,500 seconds, more than five times longer than any other travel time on that segment.
4. October 30th, 31st, and November 1st on Adelaide, Jarvis to Parliament, for a series of very high PM peaks 2-3 times higher than any other PM peak.
5. September 16th on Front, Jarvis to Parliament, for a peak hour travel time more than 15 times longer than any other on the segment.
6. November 5th, on Dufferin Queen to King for a travel time three times higher than any weekend peak and twice as long as any weekday travel time. 
7. September 16th on Jarvis Front to King for a travel time at 23:30 4-5 times as long as any other weekend travel time.
8. September 17th on Jarvis King to Queen for a travel time at midday 4-5 times longer than any other weekend travel time. 
9. September 24th on Parliament Queen to Dundas due to an abnormally high morning travel time causing the baseline to trend upwards when the data generally trends downwards.

Many outliers are single points, which are likely due to pedestrian phones being picked up during low traffic during the nighttime hours. The exceptions to this rule are Nuit Blanche, the three large peaks on Adelaide, and the Sunday on Dufferin, which seemed to have an abnormal slowdown event ongoing at the time of the outlier. 

The dates that had serious outliers were excluded from the baseline dates table for their associated segment, which was used as a reference for the formal generation of baselines. The table contains a list of analysis_id's and dates so a given date can be left out for a specific segment.

The 30-minute table was then aggregated again into time periods using an average. Finally, the segments were summed by corridor to produce the final table.
