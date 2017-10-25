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

// replaced by HTML hardcode
//var legend = L.control({position: 'topleft'});
//
//legend.onAdd = function (map) {
//
//    var div = L.DomUtil.create('div', 'info legend');
//
//    // loop through our density intervals and generate a label with a colored square for each interval
//    div.innerHTML +=
//        '<span style="background:#FB998E"></span><label>↑20%</label>' +
//        '<span style="background:#FBA3BB"></span><label>↑20%&ndash;15%</label>' +
//        '<span style="background:#E2B9E1"></span><label>↑15%&ndash;10%</label>' +
//        '<span style="background:#B7D1F4"></span><label>↑10%&ndash;0%</label>' +
//        '<span style="background:#8FE7EE"></span><label>↓0%&ndash;10%</label>' +
//        '<span style="background:#8EF6D2"></span><label>↓10%&ndash;15%</label>' +
//        '<span style="background:#B7FEAC"></span><label>↓15%&ndash;20%</label>' +
//        '<span style="background:#F2FE8E"></span><label>↓20%</label>';
//    return div;
//};
//
//legend.addTo(map);

// Used to override L.marker icon
var myIcon = L.divIcon({className: 'label'});
// To be displayed as labels
var labelData = [{coord:[43.65263, -79.40645], name:"Queen", dir:"left"},
                 {coord:[43.65195, -79.40645], name:"Richmond", dir:"left"},
                 {coord:[43.65053, -79.40645], name:"Adelaide", dir:"left"},
                 {coord:[43.64924, -79.40645], name:"King", dir:"left"},
                 {coord:[43.64777, -79.40645], name:"Wellington", dir:"left"},
                 {coord:[43.64596, -79.40645], name:"Front", dir:"left"},
                 {coord:[43.65325, -79.40602], name:"Bathurst", dir:"center"},
                 {coord:[43.65325, -79.39808], name:"Spadina", dir:"center"},
                 {coord:[43.65325, -79.38791], name:"University", dir:"center"},
                 {coord:[43.65325, -79.38022], name:"Yonge", dir:"center"},
                 {coord:[43.65325, -79.37394], name:"Jarvis", dir:"center"}];
// Adds labels to map
for(var i = 0; i < labelData.length; i++) {
    L.marker(labelData[i].coord, {icon: myIcon}).bindTooltip(labelData[i].name, {direction: labelData[i].dir, permanent: true, className: 'label'}).addTo(map);
}

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

var radio = document.getElementsByName('range');

for (var i = radio.length; i--;) {
    radio[i].onchange = function() {
        if (this.value == 1) {
            streetLayer.scene.config.global._range = "day";
            streetLayer.scene.updateConfig();
        } else if (this.value == 2) {
            streetLayer.scene.config.global._range = "month";
            streetLayer.scene.updateConfig();
        } else if (this.value == 3) {
            streetLayer.scene.config.global._range = "year";
            streetLayer.scene.updateConfig();
        }
    }
}