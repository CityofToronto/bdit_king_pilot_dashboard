# Data Aggregation

To aggregate the Bluetooth data, the travel times of individual observations were grouped into five-minute bins using the median travel time. 

From this table, the data was further aggregated using an average weighted by the number of observations per five minute bin. The data were aggregated into 30 and 15-minute bins, then a 24-hour baseline was created for both intervals for an arbitrary segment. These baselines were compared and it was determined that 30-minute aggregation yielded more valuable data.

With the level of aggregation decided, scatter plots of all the 30-minute data were created. These plots were created for each segment and divided into weekly subplots. The plots were all quality checked to ensure the data was contiguous and made sense.

Meanwhile, in the baseline lookover notebook, each segment's 24-hour baseline was plotted with it's 40-60, 20-80, and 0-100 percentile bands for the segment's 30 minute aggregated data over 24 hours. These plots were used to identify outliers that had an impact on the baselines. Most outliers that shifted the baseline beyond the 20-80 percentile band were noted for further investigation.

The third type of plot was put together to analyze the impact of removing a date from a given baseline. This plot showed the new baseline overlaid on the old baseline to demonstrate the effect of removing the outlier. It was determined that removing dates with outliers from the baseline could have an impact on the quality of the data.

Finally, for each baseline with notable outliers, a scatter plot was produced for the weeks the outliers were found. The percentile band plots were shown for reference, now with the 100th percentile shown as x's, and the last band showing up to the 90th percentile. Lastly, the baseline comparison graphs were plotted with the outlying dates removed from the new baseline. Each of these sets of figures was analyzed to see if the outlier's impact on the baseline was great enough to warrant it's removal.

If the outlier didn't have a large impact on the baseline, if it's impact was far from peak hours, or if removing the date had unpredictable effects on the baseline outside of the outlier's time the date wasn't listed for exclusion. 

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
