// Setting map properties
var map = L.map("map", { zoomControl:false });

//var bounds = new L.LatLngBounds(new L.LatLng(43.6473, -79.4044), new L.LatLng(43.64702, -79.3702));

//var street_volumes;

//$.getJSON("/street_volumes.geojson", function(json) {
//    L.geoJSON(json).addTo(map); // this will show the info it in firebug console
//    //console.log(street_volumes);
//    console.log(json);
//});

//L.geoJSON(street_volumes).addTo(map);

var streetLayer = Tangram.leafletLayer({
    scene: 'scene.yaml',
    events: {
        click: onMapClick,
    },
    selectionRadius: 25
});

//map.setMaxBounds(bounds);

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
