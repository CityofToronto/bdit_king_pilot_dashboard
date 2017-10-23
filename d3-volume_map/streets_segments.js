

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



/* Functions to draw SVGs
***********************************************************************/
var stroke = "black";
var strokeWidth = 5;
var pathfill = "none";

// Create path generator
var path;
function pathFunc(obj) {
	path = d3.path();
	path.moveTo(xScale(obj.x1),yScale(obj.y1));
	path.lineTo(xScale(obj.x2),yScale(obj.y2));
	return path;
}

// draw a path
function drawPath(obj) {
	svgContainer.append("path")
		.attr("id", obj.id)
		.attr("d", pathFunc(obj))
		.attr("stroke", stroke)
		.attr("stroke_width", strokeWidth)
		.attr("fill", pathfill);
}

// draw all street objects in an array
function pathGen(arr) {
	arr.forEach(function(obj) {
	drawPath(obj)
	});
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
	})
	pathGen(streets_segments);
});

