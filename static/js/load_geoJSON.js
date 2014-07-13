// Load the GeoJSON (monster stomp).
runAround.loadGeoJSON = function() {
  var geoJSON = 'js/geoJSON_route_348949363.json'
  map.data.loadGeoJson(geoJSON);
  
  // Set the styling.
  var featureStyle = {
    fillColor: 'green',
    strokeWeight: 10
  }
  map.data.setStyle(featureStyle);
}