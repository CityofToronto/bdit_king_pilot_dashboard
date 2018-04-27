# How to Generate Monthly Bluetooth Summaries 

Every month, summary tables of travel times need to be populated for each day type and period combination. These summaries can be automatically generated through the functions in the `monthlysummary.ipynb` file. Follow these steps in order to generate monthly summaries when required.

1. Open the notebook, and locate the `month` object. It will be under the heading "Month Class".
<br>

2. In this section of the notebook, you will find a variable called `my_month`. It is an instance of the `month` object. Create an instance of this class with the appropriate start date, end date, and holidays attributes. 
<br>

3. Now run all cells in the notebook.
<br>

4. Proceed to the bottom of the notebook. you will see two dropdown menus, `Day Type` and `Period`, and a `Generate` button. For each combination of day time and period, click `Generate`. A table like the one below will be generated

![png](bluetooth/monthly_summaries/images/screenshot.png) 

<br>

5. For each table generated, copy the values and paste them into the King Pilot Dashboard email template. 
<br>

# How to Update the `Snowflags` dataframe

In addition to summaries being generated, a dataframe with flagged with snow/rain days is updated every month. For time periods with snow/rain a 1 is placed in an additional column, and 0 is placed otherwise. After snow/rain time periods and days are identified, follow these steps to update this dataframe:

1. Open the `snowflags.ipynb`. 
<br>

2. You will see a cell containing several lists of dictionaries assigned to month variables. The keys of these dictionaries are datetime objects of days with snow/rain, and the values correspond to a list of specific time periods where it snowed/rained on these days. 
<br>

3. Each month, create a new dictionary variable with the appropriate keys and values as described above.
<br>

4. Run the notebook. An updated dataframe will be at the bottom of the notebook. 
<br>

# December Snow Analysis 

December 2018 had quite a bit of snow. As a result, a statistical analysis was conducted for the month of December, in an effort to investigate the impact of snow on travel times. Here are some significant high level results of that analysis: 


* Dundas, Queen, Adelaide, and Jarvis had slower travel times.
    * No street had a statistically significant result, i.e. the impact of snow was not statistically significant at the alpha level 0.05.
    Queen was affected the greatest - this borderlined on statistical significance
    Dundas was affected the least 

* For time periods, PM Peak had a slower mean travel time
    * No statistical significance, but had a sizeable change in travel time

* The East-West Corridor has a slower overall travel time
    * Midday and PM Peak affected this. PM Peak had the biggest impact 
    * East-West corridor during PM Peak time contained borderline statistically significant results
  The North-South Corridor seemed unaffected overall
    * PM Peak was the only period with a slower travel time


