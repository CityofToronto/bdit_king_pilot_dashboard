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

// Disable dragging when user's cursor enters the element
//map.dragging.disable();
//map.touchZoom.disable();
//map.doubleClickZoom.disable();
//map.scrollWheelZoom.disable();
//map.boxZoom.disable();
//map.keyboard.disable();


streetLayer.addTo(map);

map.setView([43.6493, -79.3910], 15);

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