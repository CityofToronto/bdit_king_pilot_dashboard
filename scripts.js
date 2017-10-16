// Setting map properties
var map = L.map("map");

//var bounds = new L.LatLngBounds(new L.LatLng(43.6473, -79.4044), new L.LatLng(43.64702, -79.40));

var streetLayer = Tangram.leafletLayer({
    scene: 'scene.yaml',
    events: {
        click: onMapClick,
    },
    selectionRadius: 25
});

//map.setMaxBounds(bounds);

streetLayer.addTo(map);

map.setView([43.6497, -79.3912], 15);

// select road feature
function onMapClick(selection) {
    if (selection.feature) {
        highlightSelect(selection.feature.properties.__roads_properties__.geo_id);
    } else {
        highlightSelect(false);
    }
}

// highlight selection
function highlightSelect(symbol) {
    streetLayer.scene.config.global._highlightSelect = symbol;
    streetLayer.scene.updateConfig();
}
