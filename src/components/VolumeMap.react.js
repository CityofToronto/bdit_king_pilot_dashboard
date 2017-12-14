import React, {Component} from 'react';
import {select, event} from 'd3-selection';
import {max, min} from 'd3-array';
import {scaleLinear} from 'd3-scale';
import {timeParse} from 'd3-time-format';
import {path} from 'd3-path';
import ReactFauxDOM from 'react-faux-dom';
import PropTypes from 'prop-types';

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
var parseDate = timeParse('%m/%d/%Y %I:%M');
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
var svgW = 1300;
var svgH = 550;

/* Scale SVGs
***********************************************************************/
var xArr, yArr, xMin, xMax, yMin, yMax, xScale, yScale;
function scaling(arr) {
	xArr = [(max(arr, function(obj) {return obj.x1;})),
			(max(arr, function(obj) {return obj.x2;})),
			(min(arr, function(obj) {return obj.x1;})),
			(min(arr, function(obj) {return obj.x2;}))];
			
	yArr = [(max(arr, function(obj) {return obj.y1;})),
			(max(arr, function(obj) {return obj.y2;})),
			(min(arr, function(obj) {return obj.y1;})),
			(min(arr, function(obj) {return obj.y2;}))];
	
	xMin = min(xArr);
	xMax = max(xArr);
	yMin = min(yArr);
	yMax = max(yArr);

	xScale = scaleLinear()
		.domain([xMin, xMax])
		.range([100, svgW-200]); // left 100px, right 200px whitespace
	yScale = scaleLinear()
		.domain([yMin, yMax])
		.range([150, svgH-100]); // top 150px, bottom 100px whitespace
}



/* Get min/max segment coordinates
***********************************************************************/
var minx1, minx2, miny1, miny2, maxx1, maxx2, maxy1, maxy2;
// takes array of objs and gets min of property across all objs
function getMin(arr, prop){
	return arr.reduce((min, obj) => Math.min(min, obj[prop]), arr[0][prop]);
}

// takes array of objs and gets max of property across all objs
function getMax(arr, prop){
	return arr.reduce((max, obj) => Math.max(max, obj[prop]), arr[0][prop]);
}


/* Colouring segments
***********************************************************************/
var cNeg4 = '#4d9221', cNeg3 = '#7fbc41', cNeg2 = '#b8e186', cNeg1 = '#e6f5d0';
var cPos1 = '#fde0ef', cPos2 = '#f1b6da', cPos3 = '#de77ae', cPos4 = '#c51b7d';
var cND = 'grey';

// colour path based on segment volume percent change
function pctColour(obj) {
	// given obj, returns a colour string
	var colour = '';
	if (obj.pct_change >= 0) { // zero or positive change is increase in volume compared to base; bad
		if (0 <= obj.pct_change && obj.pct_change < 5) {
			colour = cPos1;
			return colour;
		}
		else if (5 <= obj.pct_change && obj.pct_change < 10) {
			colour = cPos2;
			return colour;
		}
		else if (10 <= obj.pct_change && obj.pct_change < 20) {
			colour = cPos3;
			return colour;
		}
		else if (20 <= obj.pct_change) {
			colour = cPos4;
			return colour;
		}
	}
	else if (obj.pct_change < 0) { // negative change is decrease in volume compared to base; good
		if (-5 < obj.pct_change && obj.pct_change < 0) {
			colour = cNeg1;
			return colour;
		}
		else if (-10 < obj.pct_change && obj.pct_change <= -5) {
			colour = cNeg2;
			return colour;
		}
		else if (-20 < obj.pct_change && obj.pct_change <= -10) {
			colour = cNeg3;
			return colour;
		}
		else if (obj.pct_change <= -20) {
			colour = cNeg4;
			return colour;
		}
	}
	else {
		colour = cND // no data colour
		return colour;
	}
}



/* Functions to draw SVGs
***********************************************************************/
var slstrokeWidth = 3;
var sllinecap = 'round';

//var ssstroke = "black";
var ssstrokeWidth = 1;
var fillDefault = 'grey';

// Create line path generator (for sl)
var lpath;
function pathFunc(obj) {
	lpath = path();
	lpath.moveTo(xScale(obj.x1),yScale(obj.y1));
	lpath.lineTo(xScale(obj.x2),yScale(obj.y2));
	return lpath;
}

//// Variables and functions for polygon path generator (for ss)
var polywidth = 3;
var pathgen, seglist;

// function for inner polygons of the map graphic
function inside(obj, arr) {
	// cases based on directions
	if (obj.direction == 'S') {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == 'W')) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == 'E'));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 - polywidth));
			pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 + polywidth));
			pathgen.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == 'W')) {
				pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 - polywidth));
				pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1));
				pathgen.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "E"))
				pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2));
				pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 + polywidth));
				pathgen.closePath();
			}
		}
		else { // if (seglist.length == 0)
			pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2));
			pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1));
			pathgen.closePath();
		}
	}
	else if (obj.direction == 'E') {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == 'S')) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == 'N'));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 + polywidth));
			pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 + polywidth));
			pathgen.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == 'S')) {
				pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 + polywidth));
				pathgen.lineTo(xScale(obj.x1), yScale(obj.y1 + polywidth));
				pathgen.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "N"))
				pathgen.lineTo(xScale(obj.x2), yScale(obj.y2 + polywidth));
				pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 + polywidth));
				pathgen.closePath();
			}
		}
		else { // if (seglist.length == 0)
			pathgen.lineTo(xScale(obj.x2), yScale(obj.y2 + polywidth));
			pathgen.lineTo(xScale(obj.x1), yScale(obj.y1 + polywidth));
			pathgen.closePath();
		}
	}
	else if (obj.direction == 'N') {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == 'E')) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == 'W'));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 + polywidth));
			pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 - polywidth));
			pathgen.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == 'E')) {
				pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 + polywidth));
				pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1));
				pathgen.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "W"))
				pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2));
				pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 - polywidth));
				pathgen.closePath();
			}
		}
		else { // if (seglist.length == 0)
			pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2));
			pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1));
			pathgen.closePath();
		}
	}
	else if (obj.direction == 'W') {
		// populate seglist
		seglist = arr.filter(function(seg) {
			return ((obj.x2 == seg.x1) && (obj.y2 == seg.y1) && (seg.direction == 'N')) || 
				((obj.x1 == seg.x2) && (obj.y1 == seg.y2) && (seg.direction == 'S'));
		})
		
		// draw polygon path, assuming last position at obj x2 and y2
		if (seglist.length == 2) {
			pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 - polywidth));
			pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 - polywidth));
			pathgen.closePath();
		}
		else if (seglist.length == 1) {
			if ((obj.x2 == seglist[0].x1) && (obj.y2 == seglist[0].y1) && (seglist[0].direction == 'N')) {
				pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 - polywidth));
				pathgen.lineTo(xScale(obj.x1), yScale(obj.y1 - polywidth));
				pathgen.closePath();
			}
			else { 
			// if ((obj.x1 == seglist[0].x2) && (obj.y1 == seglist[0].y2) && (seglist[0].direction == "S"))
				pathgen.lineTo(xScale(obj.x2), yScale(obj.y2 - polywidth));
				pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 - polywidth));
				pathgen.closePath();
			}
		}
		else { // if (seglist.length == 0)
			pathgen.lineTo(xScale(obj.x2), yScale(obj.y2 - polywidth));
			pathgen.lineTo(xScale(obj.x1), yScale(obj.y1 - polywidth));
			pathgen.closePath();
		}
	}
}


// function for outer/edge polygons of the map graphic
function outside(obj, arr) {
	// NW corner
	if (obj.x2 == minx2 && obj.y2 == miny2 && obj.direction == 'W') {
		pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 - polywidth));
		pathgen.lineTo(xScale(obj.x1), yScale(obj.y1 - polywidth));
		pathgen.closePath();
	}
	else if (obj.x1 == minx1 && obj.y1 == miny1 && obj.direction == 'S') {
		pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2));
		pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 - polywidth));
		pathgen.closePath();
	}
	// SW corner
	else if (obj.x2 == minx2 && obj.y2 == maxy2 && obj.direction == 'S') {
		pathgen.lineTo(xScale(obj.x2 - polywidth), yScale(obj.y2 + polywidth));
		pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1));
		pathgen.closePath();
	}
	else if (obj.x1 == minx1 && obj.y1 == maxy1 && obj.direction == 'E') {
		pathgen.lineTo(xScale(obj.x2), yScale(obj.y2 + polywidth));
		pathgen.lineTo(xScale(obj.x1 - polywidth), yScale(obj.y1 + polywidth));
		pathgen.closePath();
	}
	// NE corner
	else if (obj.x1 == maxx1 && obj.y1 == miny1 && obj.direction == 'W') {
		pathgen.lineTo(xScale(obj.x2), yScale(obj.y2 - polywidth));
		pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 - polywidth));
		pathgen.closePath();
	}
	else if (obj.x2 == maxx2 && obj.y2 == miny2 && obj.direction == 'N') {
		pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 - polywidth));
		pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1));
		pathgen.closePath();
	}
	// SE corner
	else if (obj.x1 == maxx1 && obj.y1 == maxy1 && obj.direction == 'N') {
		pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2));
		pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 + polywidth));
		pathgen.closePath();
	}
	else if (obj.x2 == maxx2 && obj.y2 == maxy2 && obj.direction == 'E') {
		pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 + polywidth));
		pathgen.lineTo(xScale(obj.x1), yScale(obj.y1 + polywidth));
		pathgen.closePath();
	}
	// E Wellington/Front St corner exceptions
	else if (obj.streetname == 'Front1' && obj.segdesc == 'Church to Jarvis') {
		pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2 + polywidth));
		pathgen.lineTo(xScale(obj.x1), yScale(obj.y1 + polywidth));
		pathgen.closePath();
	}
	else if (obj.streetname == 'Jarvis' && obj.segdesc == 'Wellington to King') {
		pathgen.lineTo(xScale(obj.x2 + polywidth), yScale(obj.y2));
		pathgen.lineTo(xScale(obj.x1 + polywidth), yScale(obj.y1 + polywidth));
		pathgen.closePath();
	}
	// otherwise, run function for inside segments
	else {
		inside(obj, arr);
	}
}


// Create polgyon path generator (for ss)
function fancy(obj, arr) {
	pathgen = path();
	pathgen.moveTo(xScale(obj.x1),yScale(obj.y1));
	pathgen.lineTo(xScale(obj.x2),yScale(obj.y2));
	
	outside(obj, arr);
	
	return pathgen;
}


// draw all objects in streets_lines
function slpathGen(arr, group) {
	if (group == '#slnodata') { // streets with no data are bottom layer and grey
		select(group)
			.selectAll('path')
			.data(arr.filter(function(obj) {return (obj.streetname == 'Portland' || obj.streetname == 'Wellington' || 
					obj.streetname == 'Peter/Blue Jays' || obj.streetname == 'John' || 
					obj.streetname == 'Simcoe' || obj.streetname == 'University' || obj.streetname == 'York' ||
					obj.streetname == 'Yonge' || obj.streetname == 'Church');}))
			.enter()
			.append('path')
			.attr('id', function(obj) {return obj.streetname;})
			.attr('d', function(obj) {return pathFunc(obj);})
			.attr('stroke', 'grey')
			.attr('stroke-dasharray', '5, 10')
			.attr('stroke-width', slstrokeWidth)
			.attr('stroke-linecap', sllinecap);
	}
	else { // streets with data are top layer and black
		select(group)
			.selectAll('path')
			.data(arr
					.filter(function(obj) {return !(obj.streetname == 'Portland' || obj.streetname == 'Wellington' || 
					obj.streetname == 'Peter/Blue Jays' || obj.streetname == 'John' || 
					obj.streetname == 'Simcoe' || obj.streetname == 'University' || obj.streetname == 'York' ||
					obj.streetname == 'Yonge' || obj.streetname == 'Church');}))
			.enter()
			.append('path')
			.attr('id', function(obj) {return obj.streetname;})
			.attr('d', function(obj) {return pathFunc(obj);})
			.attr('stroke', 'white')
			.attr('stroke-width', slstrokeWidth)
			.attr('stroke-linecap', sllinecap);
	}
}

// draw all objects in streets_segments
function sspathGen(ssarr) {
	select('#ssgroup') // create and draw the ss path elements
		.selectAll('path')
		.data(ssarr, function(obj) {return obj.direction + obj.id;}) // key for binding
		.enter()
		.append('path')
		.attr('id', function(obj) {return obj.direction + obj.id;})
		.attr('d', function(obj) {return fancy(obj, ssarr);})
		.attr('stroke', 'white')
		.attr('stroke-width', ssstrokeWidth)
		.attr('fill', fillDefault); // default colour, also no-data colour
}

var divtip;
//update segment polygons by binding data
function sspathUpdate(dataset) {
	// update variables current_period and current_month
	//buttonChecker();
	
	// bind data to ss paths
	var segments = select('#ssgroup')
		.selectAll('path')
		.data(dataset)
		// Dash does all filtering
		// .data(dataset.filter(function(obj) // filter for current period and month
					// {return (obj.time_period == current_period) 
						// && ((obj.month.getMonth() + 1) == current_month);}), 
				// function(obj) {return obj.direction + obj.id;}) // key for binding
	
	// colour by data with transition
	segments.transition()
		.duration(1000)
		.attr('fill', function(obj) {return pctColour(obj);})
	
	// tooltip
	segments.on('mouseover', function() {
				divtip.style('display', 'inline');
			})
		.on('mousemove', function(obj) {
			divtip.transition()
				.duration(200)
				.style('opacity', .9);
			divtip.html('Volume Change: ' + obj.pct_change + '%' + '<br>' + 'Actual Volume: ' + obj.volume)
				.style('left', (event.pageX) + 'px')
				.style('top', (event.pageY) + 'px');})
		.on('mouseout', function() {
			divtip.transition()
				.duration(500)
				.style('opacity', 0);});
}



/* Functions to label SVGs
***********************************************************************/
var fontsize = '12px';
var fontfill = 'black'; // font colour

var anchEW = 'end';
var anchNS = 'start';
var dxEW = -20;
var dxNS = 20;
var dyEW = '.35em'; // add half the text's height to its y attribute
var dyNS = '.35em'; // add half the text's height to its y attribute

function labelStreets(arr) {
	select('#labelgroup')
		.selectAll('text')
		.data(arr)
		.enter()
		.append('text')
		.text(function(obj) {if (obj.streetname == 'Front1') {return 'Front';} // Front exceptions
							else if (obj.streetname == 'Front2') {return '';}
							else {return obj.streetname;}})
		.attr('class', 'labels-text')
		.attr('x', function(obj) {return xScale(obj.x1);})
		.attr('y', function(obj) {return yScale(obj.y1);})
		.attr('font_size', fontsize)
		.attr('fill', fontfill)
		.attr('text-anchor', function(obj) { // rotate NS street labels
			if (obj.directions == 'NS' || obj.directions == 'N' || obj.directions == 'S') 
				{return anchNS;}
			else {return anchEW;}})
		.attr('transform', function(obj) {
			if (obj.directions == 'NS' || obj.directions == 'N' || obj.directions == 'S')
				{return 'rotate(270 ' 
				+ xScale(obj.x1) + ',' + yScale(obj.y1) + ')';}
			else {return '';}})
		.attr('dx', function(obj) {if (obj.directions == 'NS' || obj.directions == 'N' || obj.directions == 'S') 
										{return dxNS;}
									else {return dxEW;}})
		.attr('dy', function(obj) {if (obj.directions == 'NS' || obj.directions == 'N' || obj.directions == 'S') 
										{return dyNS;}
									else {return dyEW;}});
}



/* Create a legend
***********************************************************************/
// data and variables for legend
var legendText = ['Volume Change (%)', 
	'&minus;20', '&minus;10', '&minus;10 to &minus;5', '&minus;5 to 0', 
	'0', '5 to 10', '+10', '+20', 'No Data']; // requires length of 10
var legendX = svgW - 120;
var legendY = [0, 40, 80, 120, 140, 160, 180, 200, 240, 280]; // requires length of 10
var legendColours = [cND, cNeg4, cNeg3, cNeg2, cNeg1, cPos1, cPos2, cPos3, cPos4, cND]; // requires length of 10
var legendData = []; // will be length of 10

// create objects from text, x, y, and colour to put into legendData array
function createLegend() {
	legendText.forEach(function(t, i) {
		legendData.push({text: t, 
						x: legendX, 
						y: legendY[i]+130, // shift legend height
						colour: legendColours[i]});
	});

	// display text for legend
	select('#legendgroup')
		.selectAll('text')
		.data(legendData.filter(function(d) {return d.text == legendText[0] || d.text == legendText[1] ||
											d.text == legendText[2] || d.text == legendText[5] ||
											d.text == legendText[7] || d.text == legendText[8] ||
											d.text == legendText[9];}))
		.enter()
		.append('text')
		.html(function(d) {return d.text;})
		.attr('class', 'legend-text')
		.attr('x', function(d) {if (d.text == legendText[0]) {return d.x-40;}
								else {return d.x;}})
		.attr('y', function(d) {if (d.text == legendText[1]) {return d.y+20;}
								else if (d.text == legendText[2]) {return d.y+20;}
								else if (d.text == legendText[5]) {return d.y-20;}
								else if (d.text == legendText[7]) {return d.y-20;}
								else if (d.text == legendText[8]) {return d.y-20;}
								else {return d.y;}})
		.attr('font-size', function(d) {if (d.text == legendText[0]) {return 18;}
								else {return 14;}})
		.attr('fill', 'black')
		.attr('dy', '.35em');

	// display symbol for legend
	select('#legendgroup')
		.selectAll('line')
		.data(legendData.filter(function(d) {return d.text != legendText[0];}))
		.enter()
		.append('line')
		.attr('x1', function(d) {return d.x-40;})
		.attr('y1', function(d) {return d.y;})
		.attr('x2', function(d) {return d.x-9;})
		.attr('y2', function(d) {return d.y;})
		.attr('stroke', function(d) {return d.colour;})
		.attr('stroke-width', 40);
}

class VolumeMap extends Component {
	// Initialize component
	constructor(props) {
		super(props)
		this.createVolumeMap = this.createVolumeMap.bind(this)
	}
	// Calls the function if React.Component mounted
	componentDidMount() {
		this.createVolumeMap()
	}
	// // Calls the functions whenever a prop changes
	componentDidUpdate() {
		sspathUpdate((this.props.volume_data).map(dataConverter));
	}
	// Creates the VolumeMap
	createVolumeMap() {
		// Load prop data
		var sl = this.props.sl_data;
		var ss = this.props.ss_data;
		var file = this.props.volume_data;
		
		/* Create tooltip
		***********************************************************************/
		divtip = select(this.node.parentNode)
			.append('div')
			.attr('class', 'tooltip')
			.style('opacity', 0);
		
		// Create SVG container
		var svgContainer = select(this.node)
			.classed('svg-container volumemap-padding', true)
			.append('svg')
			.attr('id', this.props.id)
			// .attr('width', svgW)
			// .attr('height', svgH);
			.attr('preserveAspectRatio','xMinYMin')
			.attr('viewBox', '0 0 '+svgW+' '+svgH)
			.attr('class', 'svg-content-responsive');
		
		// Create Label Group
		svgContainer.append('g')
			.attr('id', 'labelgroup');
		// Create streets_lines no data group
		svgContainer.append('g')
			.attr('id', 'slnodata');
		// Create streets_lines Group
		svgContainer.append('g')
			.attr('id', 'slgroup');
			
		// Create streets_segments Group
		svgContainer.append('g')
			.attr('id', 'ssgroup');
		// Create legend Group
		svgContainer.append('g')
			.attr('id', 'legendgroup');
		
		// typify data
		var streets_lines = sl.map(slConverter);
		var streets_segments = ss.map(ssConverter);
		var vol_data = file.map(dataConverter);
		
		// get min/max segment coordinates
		minx1 = getMin(streets_segments, 'x1');
		minx2 = getMin(streets_segments, 'x2');
		miny1 = getMin(streets_segments, 'y1');
		miny2 = getMin(streets_segments, 'y2');

		maxx1 = getMax(streets_segments, 'x1');
		maxx2 = getMax(streets_segments, 'x2');
		maxy1 = getMax(streets_segments, 'y1');
		maxy2 = getMax(streets_segments, 'y2');
		
		// create scale and labels
		scaling(streets_lines);
		labelStreets(streets_lines);
		createLegend();
		
		// create and draw paths
		slpathGen(streets_lines, '#slnodata');
		slpathGen(streets_lines, '#slgroup');
		sspathGen(streets_segments);
		
		
		// initial data view
		//buttonChecker();
		sspathUpdate(vol_data);
	}
	// What is displayed from the class
    render() {
		return (
			<div ref={node => this.node = node}>
			</div>
		)
	}
}

// VolumeMap props
VolumeMap.propTypes = {
	
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,
	
	/**
	 * The data used to generate the street lines. Must be in JSON format
	 */
	sl_data: PropTypes.object,
	
	/**
	 * The data used to generate the street segments. Must be in JSON format.
	 */
	ss_data: PropTypes.object,
	
	/**
	 * The data that contains volume info for the street segments. Must be in JSON format.
	 */
	volume_data: PropTypes.object
};

export default ReactFauxDOM.withFauxDOM(VolumeMap)