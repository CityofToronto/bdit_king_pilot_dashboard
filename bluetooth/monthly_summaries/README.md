# Monthly Bluetooth Summaries 

Every month, summary tables of travel times need to be populated for each day type and period combination. These summaries can be automatically generated through the functions in the `monthlysummary.ipynb` file. Follow these steps in order to generate monthly summaries when required.

1. Open the notebook, and locate the `month` object. It will be under the heading "Month Class".
<br>

2. In this section of the notebook, you will find a variable called `my_month`. It is an instance of the `month` object. Create an instance of this class with the appropriate start date, end date, and holidays attributes. 
<br>

3. Now run all cells in the notebook.
<br>

4. Proceed to the bottom of the notebook. you will see two dropdown menus, `Day Type` and `Period`, and a `Generate` button. For each combination of day time and period, click `Generate`. 
<br>

5. For each table generated, copy the values and paste them into the King Pilot Dashboard email template. 
<br>

### Snowflags 

In addition to summaries being generated, a dataframe with flagged with snow/rain days is updated everymonth. For time periods with snow/rain a 1 is placed, and 0 is placed otherwise. After snow/rain time periods and days are identified, follow these steps to update this dataframe:

1. Open the `snowflags.ipynb`. 
<br>

2. You will see a cell containing several lists of dictionaries assigned to month variables. The keys of these dictionaries are datetime objects of days with snow/rain, and the values correspond to a list of specific time periods where it snowed/rained on these days. 
<br>

3. Each month, create a new variable with the appropriate keys and values as described above.
<br>

4. Run the notebook. An updated dataframe will be at the bottom of the notebook. 
