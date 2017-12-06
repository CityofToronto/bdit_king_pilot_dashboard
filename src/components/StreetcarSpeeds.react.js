import React, {Component} from 'react';
import {select, selectAll} from 'd3-selection';
import {interpolateRound} from 'd3-interpolate';
import {} from 'd3-transition';
import ReactFauxDOM from 'react-faux-dom';
import PropTypes from 'prop-types';

// styling variables
var margin = {top: 20, right: 10, bottom: 20, left: 10};
var width = 750 - margin.left - margin.right;
var height = 200 - margin.top - margin.bottom;
		
var buffer = 10;
var boxHeight = 80;

var textBuffer = 7;
var leftBuffer = 20;
var segmentBuffer = 10;

var fontSpeedSize = 18;
//var fontSegmentSize = 12;
var fontTTSize = 40;

var tileWidth = (width - margin.left - margin.right - leftBuffer)/5;
var tileHeight = 15;

// global data variables
var segmentLengths = [0.65,0.85,0.60,0.50]
var tt = [0,0];
var dataset = [];

var segments = ['Bathurst - Spadina','Spadina - University','University - Yonge','Yonge - Jarvis']

var tt_data = [];

// Determines the colour of the speed tiles based on speed
var speedColor = function(speed) {
	if (speed < 5){ return '#670912';}
	else if (speed < 10) { return '#FF5468';}
	else if (speed < 15) {return '#FABE4D';}
	else {return '#4DFA90';}
}

// all the transitions
function updateGraphics() {
	// Update speed colour tiles
	selectAll('rect.tiles')
		.data(dataset)
		.transition()
		.duration(1000)
		.attr('fill',function(d) {return speedColor(d);});
	// Update speed text
	selectAll('text.text_speeds')
		.data(dataset)
		.transition()
		.duration(1000)
		.tween('text', function(d) {
			var that = select(this);
			var currentValue = that.text().match(/\d+/);
			var i =  interpolateRound(currentValue, d);
			return function(t) { that.text(i(t) + ' KM/H');};
		});
	// Update travel time text
	selectAll('text.text_tt')
		.data(tt)
		.transition()
		.duration(500)
		.delay(1000)
		.tween('text', function(d) {
			var that = select(this);
			var currentValue = that.text();
			var i = interpolateRound(currentValue, d[0]);
			return function(t) { that.text(i(t));};					
		});
}

function dotProduct(array1, array2) {
	var sum = 0;
	for (var i=0; i < array1.length; i++) {
		sum += 60.0/array1[i] * array2[i];
	}
	return sum;
}

function updateDatasets(data) {
	var tt_subset = data;
	// Sort tt_subset by segment id
	tt_subset = 
		tt_subset.sort(function(a,b) {
			return a.segment_id > b.segment_id;
		});
	// Sort tt_subset by direction (EB/WB)
	tt_subset = 
		tt_subset.sort(function(a,b) {
			return a.dir < b.dir;
		});
	// Update travel time dataset
	dataset = [];
	for (var j =0; j < tt_subset.length; j++) {
		dataset.push(segmentLengths[j%4] / tt_subset[j].travel_time * 60.0);
	}
	
	var wb_tt = Math.round(dotProduct(dataset.slice(0,4),segmentLengths));
	var eb_tt = Math.round(dotProduct(dataset.slice(4,8),segmentLengths));
	// Update travel time display data
	tt = [[wb_tt,'Westbound'],[eb_tt,'Eastbound']];
}

class StreetcarSpeeds extends Component {
	// Initialize component
	constructor(props) {
		super(props)
		this.createSCSTable = this.createSCSTable.bind(this)
	}
	// Calls the function if React.Component mounted
	componentDidMount() {
		this.createSCSTable()
	}
	// Calls the functions whenever a prop changes
	componentDidUpdate() {
		updateDatasets(this.props.data);
		updateGraphics();
	}
	// Creates the StreetcarSpeeds table
	createSCSTable() {
		// Load prop data
		tt_data = this.props.data;
		// Loads the default data
		updateDatasets(tt_data);
		// Set the dimensions of the svg element
		var svg_width = width + margin.left + margin.right;
		var svg_height = height + margin.top + margin.bottom;
		var svg = select(this.node)
			.classed("svg-container", true)
			.append('svg')
			.attr('id', this.props.id)
//			.attr('width', width + margin.left + margin.right)
//			.attr('height', height + margin.top + margin.bottom)
			.attr('preserveAspectRatio','xMinYMin')
			.attr('viewBox', '0 0 '+svg_width+' '+svg_height)
			.attr('class', 'svg-content-responsive');
		// bars
		svg.selectAll('tiles')
			.data(dataset)
			.enter()
			.append('rect')
			.attr('class','tiles')
			.attr('x', function(d,i) { return margin.left + leftBuffer + (i%4) * tileWidth; })
			.attr('y', function(d,i) { if (i<=3){ return margin.top + boxHeight - buffer/2 - tileHeight;} else {return margin.top + boxHeight + buffer/2;} })
			.attr('width',tileWidth)
			.attr('height',tileHeight)
			.attr('fill',function(d) {return speedColor(d);})
			.attr('stroke','black')
			.attr('stroke-width',1)
		
		// km/h text
		svg.selectAll('text_speeds')
			.data(dataset)
			.enter()
			.append('text')
			.text(function(d) { return Math.round(d) + ' KM/H';})
			.attr('class','text_speeds')
			.attr('x', function(d,i) { return margin.left + leftBuffer + (i%4) * tileWidth + tileWidth/2; })
			.attr('y', function(d,i) { 	if (i<=3){ return margin.top + boxHeight - buffer/2 - tileHeight - textBuffer;} 
										else {return margin.top + boxHeight + buffer/2 + tileHeight + textBuffer + fontSpeedSize*7/10;} 
										})
			.attr('fill', 'black')
			.attr('text-anchor', 'middle')
			
		// segment name and line seperators
		svg.selectAll('text_segments')
			.data(segments)
			.enter()
			.append('text')
			.text(function(d) { return d.toUpperCase();})
			.attr('class','text_segments')
			.attr('x', function(d,i) { return margin.left + leftBuffer + i * tileWidth + tileWidth/2; })
			.attr('y', margin.top + boxHeight - buffer/2 - tileHeight - textBuffer - fontSpeedSize - segmentBuffer)
			.attr('fill', 'black')
			.attr('text-anchor', 'middle')
		
		svg.selectAll('line_segments')
			.data(segments)
			.enter()
			.append('line')
			.attr('class','line_segments')
			.attr('x1',function(d,i) { return margin.left+leftBuffer+(i+1)*tileWidth;})
			.attr('x2',function(d,i) { return margin.left+leftBuffer+(i+1)*tileWidth;})
			.attr('y1',margin.top)
			.attr('y2',margin.top + boxHeight*2)
			.attr('stroke','black')
			.attr('stroke-width',0.5)
		
		// lines
		svg.append('rect')
			.attr('width',width - margin.left - margin.right - leftBuffer)
			.attr('height', boxHeight * 2)
			.attr('x', margin.left + leftBuffer)
			.attr('y', margin.top)
			.attr('fill-opacity',0)
			.attr('stroke','black')
			.attr('stroke-width',1)
		
		svg.append('line')
			.attr('x1',margin.left + leftBuffer)
			.attr('x2',margin.left + leftBuffer + tileWidth * 5)
			.attr('y1',margin.top + boxHeight)
			.attr('y2',margin.top + boxHeight)
			.attr('stroke','black')
			.attr('stroke-width',0.5)	
		
		// travel time summaries
		var tt_texts = svg.selectAll('text.tt')
				.data(tt)
				.enter()
		
		tt_texts.append('text')
			.text(function(d) {return d[0];})
				.attr('class','text_tt')
				.attr('x', function() {return margin.left + leftBuffer + tileWidth * 4.475;})
				.attr('y', function(d,i) {return margin.top + boxHeight/2 + i * (boxHeight);})
				.attr('fill', 'black')
				.attr('text-anchor', 'end')
				
		tt_texts.append('text')
			.text('MIN')
				.attr('class','text_min')
				.attr('x', function() {return margin.left + leftBuffer + tileWidth * 4.525;})
				.attr('y', function(d,i) {return margin.top + boxHeight/2 + i * (boxHeight);})
				.attr('fill', 'black')
				.attr('font-size', (fontTTSize-14) + 'px')
		
		tt_texts.append('text')
			.text(function(d) {return d[1].toUpperCase();})
				.attr('class','text_dir')
				.attr('x', function() {return margin.left + leftBuffer + tileWidth * 4.525;})
				.attr('y', function(d,i) {return margin.top + boxHeight/2 + i * (boxHeight) + boxHeight*1/3;})
				.attr('fill', 'black')
				.attr('text-anchor', 'middle')
	}
	// What is displayed from the class
    render() {
		return (
			<div className={this.props.div_class} ref={node => this.node = node}>
			</div>
		)
	}
}
// StreetcarSpeeds props
StreetcarSpeeds.propTypes = {
	/**
     * The ID used to identify this component in Dash callbacks
     */
    div_class: PropTypes.string,
	
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,
	
	/**
	 * The data used to fill the component. Must be in JSON format.
	 */
	data: PropTypes.object
};

export default ReactFauxDOM.withFauxDOM(StreetcarSpeeds)