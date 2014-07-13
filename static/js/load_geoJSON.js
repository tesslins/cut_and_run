var map;
function initialize() {
  // Create the map.
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 12,
    center: new google.maps.LatLng(39.7392,-104.9847)
  });

  // Load the GeoJSON monster stomp.
  var geoJSON = 'js/geoJSON_single_route.json'
  map.data.loadGeoJson(geoJSON);
  
  // Set the styling.
  var featureStyle = {
    fillColor: 'green',
    strokeWeight: 10
  }
  map.data.setStyle(featureStyle);
}


google.maps.event.addDomListener(window, 'load', initialize);