var testarr = [
// {direction: "S", x1: 50, y1: 30, x2: 50, y2: 50},
{direction: "E", x1: 30, y1: 50, x2: 50, y2: 50},
// {direction: "N", x1: 50, y1: 70, x2: 50, y2: 50},
// {direction: "W", x1: 70, y1: 50, x2: 50, y2: 50},

{direction: "N", x1: 50, y1: 50, x2: 50, y2: 30},
// {direction: "W", x1: 50, y1: 50, x2: 30, y2: 50},
// {direction: "S", x1: 50, y1: 50, x2: 50, y2: 70},
// {direction: "E", x1: 50, y1: 50, x2: 70, y2: 50},

// {direction: "S", x1: 70, y1: 30, x2: 70, y2: 50},
// {direction: "E", x1: 50, y1: 30, x2: 70, y2: 30},

{direction: "W", x1: 50, y1: 30, x2: 30, y2: 30},
{direction: "S", x1: 30, y1: 30, x2: 30, y2: 50},
];

var testGroup = svgContainer.append("g")
	.attr("id", "testgroup");



var polywidth = 2.5;
var path, seglist;

function dirPath(obj, arr) {
	if (obj.direction == "S") {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == "W")) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == "E"));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 - polywidth));
			path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 + polywidth));
			path.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == "W")) {
				path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 - polywidth));
				path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1));
				path.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "E"))
				path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2));
				path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 + polywidth));
				path.closePath();
			}
		}
		else { // if (seglist.length == 0)
			path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2));
			path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1));
			path.closePath();
		}
	}
	else if (obj.direction == "E") {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == "S")) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == "N"));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 + polywidth));
			path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 + polywidth));
			path.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == "S")) {
				path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 + polywidth));
				path.lineTo(xScale(obj.x1), yScale(obj.y1 + polywidth));
				path.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "N"))
				path.lineTo(xScale(obj.x2), yScale(obj.y2 + polywidth));
				path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 + polywidth));
				path.closePath();
			}
		}
		else { // if (seglist.length == 0)
			path.lineTo(xScale(obj.x2), yScale(obj.y2 + polywidth));
			path.lineTo(xScale(obj.x1), yScale(obj.y1 + polywidth));
			path.closePath();
		}
	}
	else if (obj.direction == "N") {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == "E")) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == "W"));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 + polywidth));
			path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 - polywidth));
			path.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == "E")) {
				path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 + polywidth));
				path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1));
				path.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "W"))
				path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2));
				path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 - polywidth));
				path.closePath();
			}
		}
		else { // if (seglist.length == 0)
			path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2));
			path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1));
			path.closePath();
		}
	}
	else if (obj.direction == "W") {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == "N")) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == "S"));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 - polywidth));
			path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 - polywidth));
			path.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == "N")) {
				path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 - polywidth));
				path.lineTo(xScale(obj.x1), yScale(obj.y1 - polywidth));
				path.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "S"))
				path.lineTo(xScale(obj.x2), yScale(obj.y2 - polywidth));
				path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 - polywidth));
				path.closePath();
			}
		}
		else { // if (seglist.length == 0)
			path.lineTo(xScale(obj.x2), yScale(obj.y2 - polywidth));
			path.lineTo(xScale(obj.x1), yScale(obj.y1 - polywidth));
			path.closePath();
		}
	}
	else {
		console.log(obj);
	}	
}



function fancy(obj, arr) {
	path = d3.path();
	path.moveTo(xScale(obj.x1),yScale(obj.y1));
	path.lineTo(xScale(obj.x2),yScale(obj.y2));
	
	dirPath(obj, arr);
	
	return path;
}



function generate(arr) {
	d3.select("#testgroup") // create the ss path elements
		.selectAll("path")
		.data(arr)
		.enter()
		.append("path")
		.attr("d", function(obj) {return fancy(obj, arr);})
		.attr("stroke", "black")
		.attr("stroke-width", 1)
		.attr("fill", "red");
}









function getMin(arr, prop){
	return arr.reduce((min, obj) => Math.min(min, obj[prop]), arr[0][prop]);
}

function getMax(arr, prop){
	return arr.reduce((max, obj) => Math.max(max, obj[prop]), arr[0][prop]);
}



// in csv call
var minx1 = getMin(testarr, "x1");
var minx2 = getMin(testarr, "x2");
var miny1 = getMin(testarr, "y1");
var miny2 = getMin(testarr, "y2");

var maxx1 = getMax(testarr, "x1");
var maxx2 = getMax(testarr, "x2");
var maxy1 = getMax(testarr, "y1");
var maxy2 = getMax(testarr, "y2");



function outside(obj) {
	// NW corner
	if (obj.x2 == minx2 && obj.y2 == miny2 && obj.direction == "W") {
		path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 - polywidth));
		path.lineTo(xScale(obj.x1), yScale(obj.y1 - polywidth));
		path.closePath();
	}
	else if (obj.x1 == minx1 && obj.y1 == miny1 && obj.direction == "S") {
		path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2));
		path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 - polywidth));
		path.closePath();
	}
	// SW corner
	else if (obj.x2 == minx2 && obj.y2 == maxy2 && obj.direction == "S") {
		path.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 + polywidth));
		path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1));
		path.closePath();
	}
	else if (obj.x1 == minx1 && obj.y1 == maxy1 && obj.direction == "E") {
		path.lineTo(xScale(obj.x2), yScale(obj.y2 + polywidth));
		path.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 + polywidth));
		path.closePath();
	}
	// NE corner
	else if (obj.x1 == maxx1 && obj.y1 == miny1 && obj.direction == "W") {
		path.lineTo(xScale(obj.x2), yScale(obj.y2 - polywidth));
		path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 - polywidth));
		path.closePath();
	}
	else if (obj.x2 == maxx2 && obj.y2 == miny2 && obj.direction == "N") {
		path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 - polywidth));
		path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1));
		path.closePath();
	}
	// SE corner
	else if (obj.x1 == maxx1 && obj.y1 == maxy1 && obj.direction == "N") {
		path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2));
		path.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 + polywidth));
		path.closePath();
	}
	else if (obj.x2 == maxx2 && obj.y2 == maxy2 && obj.direction == "E") {
		path.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 + polywidth));
		path.lineTo(xScale(obj.x1), yScale(obj.y1 + polywidth));
		path.closePath();
	}
	else {
		console.log(obj);
	}
}


/*
for seg in array
if seg1 = obj2 and corresponding direction
or
if seg2 = obj1 and corresponding direction
then append seg to seglist

if length seglist = 0
then path for rectangle
if length seglist = 1
then path for right trapezoid
if length seglist = 2
then path for full trapezoid
*/