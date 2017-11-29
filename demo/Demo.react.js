import React, {Component} from 'react';
import {StreetcarSpeeds} from '../src';

var data = [{'segment_id':1,'segment':'Bathurst-Spadina','dir':'EB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':8.5},{'segment_id':1,'segment':'Bathurst-Spadina','dir':'WB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':7.6},{'segment_id':2,'segment':'Spadina-University','dir':'EB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':2.8},{'segment_id':2,'segment':'Spadina-University','dir':'WB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':8.1},{'segment_id':3,'segment':'University-Yonge','dir':'EB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':6.6},{'segment_id':3,'segment':'University-Yonge','dir':'WB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':2.7},{'segment_id':4,'segment':'Yonge-Jarvis','dir':'EB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':2.0},{'segment_id':4,'segment':'Yonge-Jarvis','dir':'WB','mon':'2017-09-01 00:00:00','time_period':'AM','travel_time':3.8}]


class Demo extends Component {
    constructor() {
        super();
        this.state = {
            value: ''
        }
    }

    render() {
        return (
            <div>
                <hr/>
                <h2>ExampleComponent</h2>
				<StreetcarSpeeds id='test' data={data}></StreetcarSpeeds>
                <hr/>
            </div>
        );
    }
}

export default Demo;
