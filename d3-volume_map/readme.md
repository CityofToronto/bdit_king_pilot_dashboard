# D3 Volume Map
## 1. Overview
The D3 Volume Map was created for the public dashboard of the King Street Pilot, to present actual and percent change in volumes in major streets in the study area for which is there is data. The study area is bounded by Bathurst in the west, Jarvis in the east, Queen in the north, and Front in the south. 

## 2. Data
The D3 Volume Map takes in 3 different datasets:
1. `streets_lines3.csv` - full-length streets, point-to-point line, version 3
2. `streets_segments31.csv` - streets segmented by intersections with other streets, point-to-point line, version 3.1
3. `street_volumes.csv`, or other source - volume data tied to segment number and segment direction; street_volumes.csv is fake data


###streets_lines example

line|streetname|directions|x1|y1|x2|y2
----|----------|----------|--|--|--|--
1|Queen|EW|10|10|250|10
2|Richmond|W|10|20|250|20

###streets_segments example

segment|streetname|direction|segdesc|x1|y1|x2|y2
-------|----------|---------|-------|--|--|--|--
1|Queen|E|Bathurst to Portland|10|10|30|10
2|Queen|E|Portland to Spadina|30|10|60|10

###street_volumes example

segment|direction|mon|time_period|volume|pct_change
-------|---------|---|-----------|------|----------
1|E|11/01/2017 0:00|AM|2380|13.42
2|E|11/01/2017 0:00|AM|2725|12.34

## 3. Major Components
The code for the D3 Volume Map is broken up into several different sections dedicated to different purposes, and groups functions for those purposes. The following describes the different sections and some functions of interest:

* Prepare CSV Data
* Setup SVGs
* Scale SVGs
* Get min/max segments coordinates
* Create tooltip - in react.js, this section appears in the createVolumeMap function
* Data filter functions - in react.js, this section does not exist as data filtering is handled on the Python side
* Colouring segments
* Functions to draw SVGs
* Functions to label SVGs
* Create a legend
* Draw SVGs - in react.js, this section appears in the createVolumeMap function

## 4. Key Takeaways
The development of the D3 Volume Map had many challenges, but there were several lessons learned in regards to developing in Javascript and with D3.js.

### Asynchronous Javascript / Working with external files with D3
### Global Variables
### Built-In Array Functions
### Using Anonymous Functions as Accessors of Data





