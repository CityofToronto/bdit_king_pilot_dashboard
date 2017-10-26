var testarr = [{line: 1, x1: 100, y1: 100, x2: 100, y2: 200},{line: 2, x1: 100, y1: 100, x2: 200, y2: 100}];

/* Prepare CSV Data
***********************************************************************/
// CSV column types for streets_lines.csv
var slConverter = function(d) {
	return {
		id: +d.line,
		streetname: d.streetname,
		directions: d.directions,
		x1: +d.x1,
		y1: +d.y1,
		x2: +d.x2,
		y2: +d.y2
	};
};

/*
// Row conversion for streets_lines
var streets_lines = [];
d3.csv("streets_lines.csv", function(d) {
	streets_lines = d.map(slConverter);
	console.log(streets_lines);
});
*/


/* Setup SVGs
***********************************************************************/
var svgW = 1200;
var svgH = 500;

// Create SVG container
var svgContainer = d3.select("body").append("svg")
	.attr("width", svgW)
	.attr("height", svgH);

// Create Label Group
var labelGroup = svgContainer.append("g")
	.attr("id", "labelgroup");

// Create streets_segments Group
var ssGroup = svgContainer.append("g")
	.attr("id", "ssgroup");

// Create streets_lines Group
var slGroup = svgContainer.append("g")
	.attr("id", "slgroup");



/* Scale SVGs
***********************************************************************/
// Create arrays of streets_lines X and Y values
var xArr = [];
function xAccess(arr) {
	xArr = [];
	arr.forEach(function(obj) {
		xArr.push(obj.x1);
		xArr.push(obj.x2);
	});
	return xArr;
}

var yArr = [];
function yAccess(arr) {
	yArr = [];
	arr.forEach(function(obj) {
		yArr.push(obj.y1);
		yArr.push(obj.y2);
	});
	return yArr;
}

var xMin, xMax, yMin, yMax, xScale, yScale;
function scaling() {
	// Find x and y max/min of streets_lines
	xMin = d3.min(xArr)
	xMax = d3.max(xArr)
	yMin = d3.min(yArr)
	yMax = d3.max(yArr)
	
	// Create x and y Scales
	xScale = d3.scaleLinear()
		.domain([xMin, xMax])
		.range([100, svgW-100]) // 100px SVG whitespace buffer
	yScale = d3.scaleLinear()
		.domain([yMin, yMax])
		.range([100, svgH-100]) // 100px SVG whitespace buffer
}



/* Functions to draw SVGs
***********************************************************************/
var slstroke = "black";
var slstrokeWidth = 2;
var slpathfill = "none";

// Create path generator
var path;
function pathFunc(obj) {
	path = d3.path();
	path.moveTo(xScale(obj.x1),yScale(obj.y1));
	path.lineTo(xScale(obj.x2),yScale(obj.y2));
	return path;
}

// draw path to slGroup
function sldrawPath(obj) {
	slGroup.append("path")
		.attr("id", obj.streetname)
		.attr("d", pathFunc(obj))
		.attr("stroke", slstroke)
		.attr("stroke-width", slstrokeWidth)
		.attr("stroke-linecap", "round")
		.attr("fill", slpathfill);
}

// draw all street objects in an array
function slpathGen(arr) {
	arr.forEach(function(obj) {
	sldrawPath(obj)
	});
}



/* Functions to label SVGs
***********************************************************************/
var fontfam = "san-serif";
var fontsize = "12px";
var fontfill = "black";

var anchEW = "end";
var anchNS = "start";
var dxEW = -20;
var dxNS = 20;
var dyEW = ".35em"; // add half the text's height to its y attribute
var dyNS = ".35em"; // add half the text's height to its y attribute

// label a street object
var text;
function labelStreet(obj) {
	text = d3.select("#labelgroup")
		.append("text")
		.text(obj.streetname)
		.attr("x", xScale(obj.x1))
		.attr("y", yScale(obj.y1))
		.attr("font-family", fontfam)
		.attr("font_size", fontsize)
		.attr("fill", fontfill);
}

// label all street objects in an array
function labelMany(arr) {
	arr.forEach(function(obj) {
		if (obj.streetname == "Front1") { // treating Front1 exactly like other EW streets
		obj.streetname = "Front"; // reassigning streetname
		labelStreet(obj);
		text.attr("text-anchor", anchEW)
			.attr("dx", dxEW)
			.attr("dy", dyEW);
		}
		else if (obj.streetname == "Front2") { // don't want to label Front2
		return;
		}
		else if (obj.directions == "NS") {
		var rotNS = "rotate(270 " + xScale(obj.x1) + "," + yScale(obj.y1) + ")"; // local rotate variable
		labelStreet(obj);
		text.attr("text-anchor", anchNS)
			.attr("transform", rotNS) // Coordinate system is also rotated, affecting dx and dy
			.attr("dx", dxNS)
			.attr("dy", dyNS);
		}
		else if (obj.directions == "EW" || obj.directions == "E" || obj.directions == "W") {
		labelStreet(obj);
		text.attr("text-anchor", anchEW)
			.attr("dx", dxEW)
			.attr("dy", dyEW);
		}
		else {
		labelStreet(obj);
		};
	});
}



/* Draw SVGs
***********************************************************************/
// Load data and execute functions requiring immediate access to data
var streets_lines = [];
d3.csv("streets_lines.csv", function(sl) {
	streets_lines = sl.map(slConverter);
	xAccess(streets_lines);
	yAccess(streets_lines);
	scaling()
	labelMany(streets_lines);
	slpathGen(streets_lines);
});



