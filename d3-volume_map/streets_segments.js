

/* Prepare CSV Data
***********************************************************************/
// CSV column types for streets_segments.csv
var ssConverter = function(d) {
	return {
		id: +d.segment,
		streetname: d.streetname,
		direction: d.direction,
		segdesc: d.segdesc,
		x1: +d.x1,
		y1: +d.y1,
		x2: +d.x2,
		y2: +d.y2
	};
};

/*
// Row conversion for streets_segments
var streets_segments = [];
d3.csv("streets_segments.csv", function(d) {
	streets_segments = d.map(ssConverter);
	console.log(streets_segments);
});
*/

// CSV column types for volume data
var parseDate = d3.timeParse("%m/%d/%Y %I:%M");
var dataConverter = function(d) {
	return {
		id: +d.segment,
		direction: d.direction,
		month: parseDate(d.mon),
		time_period: d.time_period,
		volume: +d.volume,
		pct_change: +d.pct_change
	};
};



/* Setup SVGs
***********************************************************************/
// Create streets_segments Group
var ssGroup = svgContainer.append("g")
	.attr("id", "ssgroup");



/* Functions to draw SVGs
***********************************************************************/
var stroke = "grey";
var strokeWidth = 5;
var pathfill = "none";

// draw a path
function ssdrawPath(obj) {
	ssGroup.append("path")
		.attr("id", obj.direction + obj.id)
		.attr("d", pathFunc(obj))
		.attr("stroke", stroke)
		.attr("stroke_width", strokeWidth)
		.attr("fill", pathfill);
}

// draw all street objects in an array
function sspathGen(arr) {
	arr.forEach(function(obj) {
	ssdrawPath(obj)
	});
}



/* Data filter functions
***********************************************************************/
// loop through radio button values
var periodIDs = ["AM", "PM"];
var monthIDs = ["Sep","Oct","Nov","Dec"];
var current_period = document.getElementById("AM").value;
var current_month = document.getElementById("Sep").value;

// check which buttons are selected, update and return current period and month
function periodLoop(arr) {
	arr.forEach(function(buttonID) {
		if (document.getElementById(buttonID).checked == true) {
			current_period = document.getElementById(buttonID).value;
			//console.log(current_period);
		};
	});
	return current_period;
}

function monthLoop(arr) {
	arr.forEach(function(buttonID) {
		if (document.getElementById(buttonID).checked == true) {
			current_month = document.getElementById(buttonID).value;
			//console.log(current_month);
		};
	});
	return current_month;
}


// time period filter
var periodArr = [];
function periodFilter(arr, period) {
	periodArr = [];
	if (period == "AM") {
		periodArr = arr.filter(obj => obj.time_period == "AM");
		//console.log(periodArr);
		return periodArr;
	}
	else if (period == "PM") {
		periodArr = arr.filter(obj => obj.time_period == "PM");
		//console.log(periodArr);
		return periodArr;
	}
	else {
		return;
	}
}

// month filter
var monthArr = [];
function monthFilter(arr, month) {
	monthArr = [];
	if (month == 9) {
		monthArr = arr.filter(obj => (obj.month.getMonth() + 1) == 9);
		//console.log(monthArr);
		return monthArr;
	}
	else if (month == 10) {
		monthArr = arr.filter(obj => (obj.month.getMonth() + 1) == 10);
		//console.log(monthArr);
		return monthArr;
	}
	else if (month == 11) {
		monthArr = arr.filter(obj => (obj.month.getMonth() + 1) == 11);
		//console.log(monthArr);
		return monthArr;
	}
	else if (month == 12) {
		monthArr = arr.filter(obj => (obj.month.getMonth() + 1) == 12);
		//console.log(monthArr);
		return monthArr;
	}
	else {
		return;
	}
}

// filter array for given month and string time period; master filter
var filteredData = [];
function dataFilter(arr, month, period) {
	filteredData = [];
	filteredData = monthFilter(periodFilter(arr, period), month);
	console.log(filteredData);
	return filteredData;
}










/* Draw SVGs
***********************************************************************/
// Load data and execute functions requiring immediate access to data
var absURL = "https://cityoftoronto.github.io/bdit_king_pilot_dashboard/data/street_volumes.csv";
var vol_data;
var streets_segments = [];
d3.csv("streets_segments.csv", function(ss) {
	streets_segments = ss.map(ssConverter);
	xAccess(streets_segments);
	yAccess(streets_segments);
	scaling();
	d3.csv(absURL, function(file) {
		vol_data = file.map(dataConverter);
		console.log(vol_data);
		dataFilter(vol_data, monthLoop(monthIDs), periodLoop(periodIDs));
	})
	sspathGen(streets_segments);
});

