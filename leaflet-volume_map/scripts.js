// Setting map properties
var map = L.map("map", { zoomControl:false });

var streetLayer = Tangram.leafletLayer({
    scene: 'scene.yaml',
//    events: {
//        click: onMapClick,
//        hover: onMapHover,
//    },
    selectionRadius: 25
});

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
    L.marker(labelData[i].coord, {icon: myIcon})
        .bindTooltip(labelData[i].name, {direction: labelData[i].dir,
                                         permanent: true,
                                         className: 'label'})
        .addTo(map);
}

// Disable dragging when user's cursor enters the element
map.dragging.disable();
map.touchZoom.disable();
map.doubleClickZoom.disable();
map.scrollWheelZoom.disable();
map.boxZoom.disable();
map.keyboard.disable();

streetLayer.addTo(map);

map.setView([43.6495, -79.3910], 15);

// Changes layer when user changes radio button selection
var radio = document.getElementsByName('range');
for (var i = radio.length; i--;) {
    radio[i].onchange = function() {
        if (this.value == 1) {
            streetLayer.scene.config.global._range = "day";
        } else if (this.value == 2) {
            streetLayer.scene.config.global._range = "month";
        } else if (this.value == 3) {
            streetLayer.scene.config.global._range = "year";
        }
        streetLayer.scene.updateConfig();
    }
}

// for use in future
// select road feature
//function onMapClick(selection) {
//    if (selection.feature) {
//        highlightSelect(selection.feature.properties.geo_id);
//    } else {
//        highlightSelect(false);
//    }
//}
//
//function onMapHover(selection) {
//    document.getElementById('map').style.cursor = selection.feature ? 'pointer' : '';
//}
//
//// highlight selection
//function highlightSelect(symbol) {
//    streetLayer.scene.config.global._highlightSelect = symbol;
//    streetLayer.scene.updateConfig();
//}


