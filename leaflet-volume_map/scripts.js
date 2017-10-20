// Setting map properties
var map = L.map("map", { zoomControl:false });

var streetLayer = Tangram.leafletLayer({
    scene: 'scene.yaml',
    events: {
        click: onMapClick,
        hover: onMapHover,
    },
    selectionRadius: 25
});

var legend = L.control({position: 'topleft'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend');

    // loop through our density intervals and generate a label with a colored square for each interval
    div.innerHTML +=
        '<span style="background:#FB998E"></span><label>↑20%</label>' +
        '<span style="background:#FBA3BB"></span><label>↑20%&ndash;15%</label>' +
        '<span style="background:#E2B9E1"></span><label>↑15%&ndash;10%</label>' +
        '<span style="background:#B7D1F4"></span><label>↑10%&ndash;0%</label>' +
        '<span style="background:#8FE7EE"></span><label>↓0%&ndash;10%</label>' +
        '<span style="background:#8EF6D2"></span><label>↓10%&ndash;15%</label>' +
        '<span style="background:#B7FEAC"></span><label>↓15%&ndash;20%</label>' +
        '<span style="background:#F2FE8E"></span><label>↓20%</label>';
    return div;
};

legend.addTo(map);

var myIcon = L.divIcon({className: 'label'});


L.marker([43.65263, -79.40645], {icon: myIcon}).bindTooltip("Queen", {direction: "center", permanent: true, direction: "left", className: 'label'}).addTo(map);
L.marker([43.65195, -79.40645], {icon: myIcon}).bindTooltip("Richmond", {direction: "center", permanent: true, direction: "left", className: 'label'}).addTo(map);
L.marker([43.65053, -79.40645], {icon: myIcon}).bindTooltip("Adelaide", {direction: "center", permanent: true, direction: "left", className: 'label'}).addTo(map);
L.marker([43.64924, -79.40645], {icon: myIcon}).bindTooltip("King", {direction: "center", permanent: true, direction: "left", className: 'label'}).addTo(map);
L.marker([43.64777, -79.40645], {icon: myIcon}).bindTooltip("Wellington", {direction: "center", permanent: true, direction: "left", className: 'label'}).addTo(map);
L.marker([43.64596, -79.40645], {icon: myIcon}).bindTooltip("Front", {direction: "center", permanent: true, direction: "left", className: 'label'}).addTo(map);

L.marker([43.65300, -79.40602], {icon: myIcon}).bindTooltip("Bathurst", {direction: "center", permanent: true, className: 'label'}).addTo(map);
L.marker([43.65300, -79.39808], {icon: myIcon}).bindTooltip("Spadina", {direction: "center", permanent: true, className: 'label'}).addTo(map);
L.marker([43.65300, -79.38791], {icon: myIcon}).bindTooltip("University", {direction: "center", permanent: true, className: 'label'}).addTo(map);
L.marker([43.65300, -79.38022], {icon: myIcon}).bindTooltip("Yonge", {direction: "center", permanent: true, className: 'label'}).addTo(map);
L.marker([43.65300, -79.37394], {icon: myIcon}).bindTooltip("Jarvis", {direction: "center", permanent: true, className: 'label'}).addTo(map);

// Disable dragging when user's cursor enters the element
//map.dragging.disable();
//map.touchZoom.disable();
//map.doubleClickZoom.disable();
//map.scrollWheelZoom.disable();
//map.boxZoom.disable();
//map.keyboard.disable();


streetLayer.addTo(map);

map.setView([43.6495, -79.3910], 15);

// select road feature
function onMapClick(selection) {
    if (selection.feature) {
        highlightSelect(selection.feature.properties.geo_id);
    } else {
        highlightSelect(false);
    }
}


function onMapHover(selection) {
    document.getElementById('map').style.cursor = selection.feature ? 'pointer' : '';
}

// highlight selection
function highlightSelect(symbol) {
    streetLayer.scene.config.global._highlightSelect = symbol;
    streetLayer.scene.updateConfig();
}

function onRangeChange(value) {
    if (value == 1) {
        streetLayer.scene.config.sources.local.url = "http://localhost:8000/street_volumes.json";
        streetLayer.scene.updateConfig();
    } else if (value == 2) {
        streetLayer.scene.config.sources.local.url = "http://localhost:8000/street_volumes2.json";
        streetLayer.scene.updateConfig();
    } else if (value == 3) {
        streetLayer.scene.config.sources.local.url = "http://localhost:8000/street_volumes3.json";
        streetLayer.scene.updateConfig();
    } else {
        streetLayer.scene.config.sources.local.url = "http://localhost:8000/street_volumes.json";
        streetLayer.scene.updateConfig();
    }
}