# King St. Pilot Dashboard Dash Components

## Usage

### Requirements
You must have `Node`, `NPM`, and `Python 3.x` in order to use these components as they are built with `React.js`.
You should also have the following `Node` modules installed using `NPM`:
- [`builder-init`](https://github.com/FormidableLabs/builder-init)
- [`builder`](https://www.npmjs.com/package/builder)
- [`d3`](https://www.npmjs.com/package/d3) Version 4
- [`react-faux-dom`](https://www.npmjs.com/package/react-faux-dom)

Also the following `Python` libraries installed using `pip`:
- All the Dash libraries mentioned in their [installation](https://plot.ly/dash/installation)
- [`pandas`](https://pandas.pydata.org/)

### Making Dash Components
Follow the [Writing Your Own Components](https://plot.ly/dash/plugins) guide provided by Plotly on how to set up your Dash ecosystem used to write your Dash components. You should also read [Plotly's tutorial](https://academy.plot.ly/react/1-introduction/) on React.js which will teach you everything you need to know on making Dash components with the Dash library.

### Installing these Components
Create your own Dash Environment from the [Writing Your Own Components](https://plot.ly/dash/plugins) guide and call it `dash-components`. Then you'll need re-install the mentioned `Node` modules above in your Dash Environment so that the components can use them. Then copy these files into the folder to replace the ones you recently created.

Once you copied the folders into your Dash environment, run the following command:

`$ npm run prepublish`

Then in your `Python 3.x` virtual environment run:

`$ python setup.py install`

Finally if you wish to see the components run:

`$ python usage.py` and go to `http://127.0.0.1:8050/` in your browser.

## Reactifying D3 Components for use in Dash
D3 is a major JavaScript data visualization library that allows for the creation of custom graphs, charts, and other visualizations. For this reason, we wanted to combine it with the power data manipulation libraries of Python such as `pandas`. To do so, JavaScript and Python are combined using Dash which can process `React.js` and convert it to be usable in a Python file which outputs the `React.js` as `HTML`. However, you can not simply process `D3` in `React.js` with `Dash` as you would with a normal React component. Below is a guide on Reactifying D3 Components for use in Dash explained with what needs to be done to each file in you Dash Enviornment.

### `<Your Component Name>.react.js`
Found in `<Your Dash Enviroment>/src/components/`. 

#### What You Should Import
At a minimum, you should have these modules imported.
```
import React, {Component} from 'react';
import ReactFauxDOM from 'react-faux-dom';
import PropTypes from 'prop-types';
```

#### Importing D3 modules
Normally you would import the D3 library using `import * as d3 from 'd3'` when working with JavaScript. However, you must import the individual functions of the D3 library from it's sub-libraries using `import {<Function you want>} from 'd3-<sub-library>'`. This is largely due to a ESLint rule as demonstrated [here](https://github.com/benmosher/eslint-plugin-import/blob/HEAD/docs/rules/no-namespace.md). As a result of this, you'll have to also add the sub-library to your list of dependencies in `package.json` in your Dash Environment. To do this simply run `$ npm i -S d3-<sub-library>` to add it.  

#### Modifying Your Component Class
Your component class is what is called when you access it in your `usage.py`, it also controls what will be rendered for your component. The following layout is used to explain what is recommend for your component using D3:
```
class <Component Name> extends Component {
  constructor(props) {
    super(props)
    this.create<Component Name> = this.create<Component Name>.bind(this)
    ...
  }
  componentDidMount() {
    this.create<Component Name>()
    ...
  }
  componentDidUpdate() {
    ...
  }
  create<Component Name>() {
    var x = select(this.node);
    ...
    (Your D3 stuff)
    ...
  }
  ...
  render() {
    return (
      // Does not need to be a svg, it can be an div, header, etc.
      // It depends on what your component will do.
      <svg ref={node => this.node = node}
        id={this.props.id}
        ...(other properties of your component)...
      >
      ...(you can have other elements within your class element)...
      </svg>
    )
  }
}
```

**Explanation**

`contructor(props)` is used to initalize your component whenever it is called. This is primarly used to set your `props` (explained later) to your component and to bind your component as the context to any new internal functions if you want access to `this.props` or `this.state` in that function. In this case, it is binding to the `create<Component Name>()` function.

`componentDidMount()` is used to fire your function(s) whenever your class is called.

`componentDidUpdate()` is used to fire your function(s) whenever your component is updated (i.e. when you change the value of your props)

`create<Component Name>()` is a function which in this case is used to create the contents/functionality of the component. Other functions can be created similar to this one. You just need to bind it to the component as mentions so you can use `this.props` or `this.state`. Inside is `var x = select(this.node)` which is the `d3-select` `select` function selecting a node produced in `render()`. Modifying `x` will modify that node such that doing `x.attr('width': 10)` using `d3` will set the `svg` node to have a width of 10.

`render()` is what is produced from your class. It should return a [`JSX`](https://jsx.github.io/) formatted value. `this.node` is set in the `ref` property of the `svg` element and acts as a reference to the actual DOM node generated by React, so you can hand that DOM node over to your D3 functionality. 

There are other methods of `React.Component` class which may be useful to your component. For a full list of these methods, see the [React Documentation](https://reactjs.org/docs/react-component.html).

#### `propTypes`
`props` are values that are passed to your component from your main app.
```
<Component Name>.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks
   */
  id: PropTypes.string,
  /**
   * Data that is passed to the class
   */
  data: PropTypes.object,
  ...
};
```
You can have any number of `props` of many types such as the ones mentioned [here](https://reactjs.org/docs/typechecking-with-proptypes.html). These `props` are values provided by your app. An important feature of `propTypes` is that there must be a comment above your `prop` as it is rendered in `metadata.json` whenenver you prepublish.

#### `export default`
For normal `React.Component`'s you would normally use `export default <Your Component Name>` to export your component, but since we are using `d3` you will need to use [`ReactFauxDOM`](https://github.com/Olical/react-faux-dom) which can render `d3`. This is done using:

```
export default ReactFauxDOM.withFauxDOM(<Your Component Class>)
```
Doing so will allow your class to be callable.

### index.js
Found in `<Your Dash Environment>/src/`. 

This file is used to group all of your components into one file. For this file, all you need to to do is import your component you created above and export it's class. For example:
```
/* eslint-disable import/prefer-default-export */
import <Your Component> from './components/<Your Component>.react';
// You can import your other components too

export {
  <Your component>
};
```

### usage.py
Found in `<Your Dash Environment>`.

This file is where your `Dash` is laid out and it's data manipulated. For this I'll be using this `usage.py` to explain.
```
import dash_components
import dash
import dash_html_components as html
import dash_core_components as dcc
# You can add other libraries too

... <some external functions> ...

app = dash.Dash('')

app.scripts.config.serve_locally = True

#layout
app.layout = html.Div([
	dash_components.<Your Component>( id='test', data=<some default data>),
  dcc.RadioItems(
		id='my_radio',
		options = [...],
		value=...,
		labelStyle={'display': 'inline-block'}
	),
	...
])

@app.callback(
	dash.dependencies.Output('<Your Component>', 'data'),
	[dash.dependencies.Input('my_radio', 'value'),
	 ...])
def update_component(a, b):
	# Some data maniputation
  ...
	return <somedata> ...

if __name__ == '__main__':
    app.run_server(debug=True)
```
Most of this is explained by the [Dash User Guide](https://plot.ly/dash/getting-started-part-2). 

#### Importing Our Component
For our component we created using `d3`, we import it using `import <Dash Environment Name>` or for this case `import dash_components`. This refers to the `dash_components` file in the `<Dash Enviornment>` directory. This folder will contain are bundled version of our components once we prepublish it.

#### Adding Our Component to the Layout
`app.layout` is used to control what is displayed on the dash. Simply add our component using `dash_components.<Your Component>( id='test', data=<some default data>)` to the `html.Div([...])` and fill any default properties of your function to satify it. These properties refer to the `props` mentioned in your component file and assigning a value here will get passed to them. Make sure you have `<your prop>=<somevalue>` when assigning properties so that the compiler knows which `prop` your referring to. You can also add [other](https://plot.ly/dash/dash-core-components) [components](https://plot.ly/dash/dash-html-components) by Plotly to your layout and can be set to interact with your component such as with `my-radio`.

#### Modify Our Component's `props`
The `@app.callback(...)` is used to update a `prop` of a component. The component is defined as the first field with it being the output as `dash.dependencies.Output('<Your Component>', '<prop>')` which is followed by the input `[dash.dependencies.Input('my_radio', 'value'), ...]`. Immediately following `@app.callback(...)` is a function that is used to update the `prop` mentioned in the output. This function takes in the values of the input in order so that the first input's value goes into the first field, and the second input's value goes into the second field of the function. The value returned by the function automatically updates the `prop`. Whenever an input is updated or changed, it triggers the function to update the output. This pattern is also known as the [Model-View-Controller Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller).

### Republishing Your Component
Once you made your desired changes to your component simply run:

```
$ npm run prepublish
$ python setup.py install
$ python usage.py
```
To prepublish your component and to display it in your browser at `http://127.0.0.1:8050/`. Optionally you can run `$ npm run prepublish` to display your component in pure JavaScript, but you'll need to update `demo/Demo.react.js` to include it.

### Enable Global Styling
It is possible to style all components using one stylesheet. All you need to do it modify your `usage.py` file and create classes if you are using `d3`.

Add the following to your `usage.py`:

```
...
from flask import send_from_directory

...
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
...

app.layout = html.Div([
	html.Link(
        rel='stylesheet',
        href='/src/styles.css' # replace this with the location of your stylesheet
    ),
	... your other components ...
])

@app.server.route('/src/<path:path>') # replace this with the home folder of your stylesheet
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'src') # ditto
    return send_from_directory(static_folder, path)
...

```
Then in your `<Component>.react.js` where you create your `d3` elements add `.attr('class', 'test')` to your `d3` element.

For example:
```
tt_texts.append('text')
				.text(function(d) {return d[1].toUpperCase();})
				.attr('x', function() {return margin.left + leftBuffer + tileWidth * 4.525;})
				.attr('y', function(d,i) {return margin.top + boxHeight/2 + i * (boxHeight) + boxHeight*1/3;})
				.attr('fill', 'black')                     # you can still have your own styling in d3
				.attr('font-size', (fontTTSize-22) + 'px') # but your stylesheet will override it
				.attr('text-anchor', 'middle')             # if you alter the same property
				.attr('class','test')                      # add this
```

### Enable Dynamic Scaling on SVGs
The great thing about SVG's is that it allow us to scale our components based on the view window size. To do so, modify your code to follow this:
```
// Create SVG container
var svgContainer = select(this.node)				// this.node is your base Div which your component builds off of
	.classed('svg-container volumemap-padding', true)	// Set the class for your base Div, also added a seperate class
	.append('svg')						// Add your SVG
	...
	.attr('preserveAspectRatio','xMinYMin')			// Preserves the aspect ratio of your svg
	.attr('viewBox', '0 0 '+svgW+' '+svgH)			// svgW and svgH are your width and height, these are mandatory
	.attr('class', 'svg-content-responsive');		// class to make it responsive
```
Then add the following code to your stylesheet:
```
.svg-container {
    display: inline-block;
    position: relative;
    vertical-align: top;
    width:100%;
    height:100%;
    overflow: hidden;
}
.svg-content-responsive {
    display: block;
    position: absolute;
    top: 0;
    left: 0;
}
.volumemap-padding {
	padding-bottom: 40%; /* probably need to adjust this according to your aspect ratio */
}
```
This method of scaling your D3 SVGs is based off of [this solution](https://stackoverflow.com/questions/16265123/resize-svg-when-window-is-resized-in-d3-js).

### Useful Tips
Here are few tips on developing you D3 component in Dash:
- Remove all unused variables from you component, a lot of errors will appear if you don't.
- Make sure values such as for data are in the correct format.
- If you want to update your component when it's `props` changes. Make an external function that updates the elements of your component such as `updateGraphics()` in `StreetcarSpeeds.react.js` and is called whenever a prop changes by placing it in `componentDidMount()`. This way you don't have to recreate you component everytime a prop changes.
- Leave all of the data manipulation to your `usage.py` file.
- If you modify your style sheet and the browser does not apply the changes, try clearing your cookies. I would recommend working in incognito to avoid having to do this constantly.

## Resources
[React.js Documentation](https://reactjs.org/docs/react-api.html)

[Elijah Meek's Guide to Interactive Application with React & D3](https://medium.com/@Elijah_Meeks/interactive-applications-with-react-d3-f76f7b3ebc710)

[React-Faux-Dom Documentation](https://github.com/Olical/react-faux-dom)

[Dash User Guide](https://plot.ly/dash/)
