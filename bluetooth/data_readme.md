# Data Aggregation
To aggregate the Bluetooth data, the travel time of individual observations was aggregated into five minute bins using the median travel time. 

From this table, the data was further aggregated using an average weighted by the number of observations per five minute bin. The data was aggregated into 30 and 15 minute bins, then a 24 hour baseline was created for each interval. These baselines were compared and it was determined that 30 minute aggregation yielded more valuable data.

With the level of aggregation decided, scatter plots were created of all the 30 minute aggregated data. These plots were created per segment and divided into weekly subplots. The plots were all quality checked.

Meanwhile, in the baseline lookover notebook, each segment's 24 hour baseline was plotted over the 40-60, 20-80, and 0-100 percentile bands for the segment's 30 minute aggregated data. These plots were used to identify outliers that had an impact on the baselines. Most outliers that pulled the baseline out of the 20-80 percentile band were noted for futher investigation.

A third type of plot was put together to analyse the impact of removing a date from a given baseline. This plot showed the new baseline overlaid on the old baseline and it was determined that removing dates with outliers from the baseline could have an impact on the quality of the basline.

Finally, for each baseline with notable outliers, a scatter plot was produced for the week the outlier was found, the baseline percentile band plots were shown for reference, now with the 100th percentile shown as x's, and the last percentile band showing up to the 90th percentile. Lastly, the basline comparison graphs were plotted with the outlying dates removed from the new baseline. This process was completed for each segment with a noted outlier, and each of these sets of figures were analysed to see if the outlier's impact on the baseline was great enough to warrant it's removal.

If the outlier didn't have a large impact on the baseline, if it's impact was far from peak hours, or if removing the date had unpredictable effects on the baseline outside of the outlier's time the date wasn't listed for exclusion, and the window in the Jupyter notebook showing the segment's charts was closed to avoid clutter. 

The dates that were listed for exclusion were excluded from the baseline dates table, which was used as a reference for the formal generation of baselines. 

The 30 minute aggregated table was then aggregated again into time periods using an average. Finally, the segments were summed by corridor to produce the final table.
