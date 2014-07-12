var map;
function initialize() {
  // Create the map.
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 12,
    center: {lat: 37.8, lng: -122.2}
  });

  // Load the GeoJSON monster stomp.
  map.data.loadGeoJson('js/geoJSON_single_route.json');
  
    // Set the styling.
  var featureStyle = {
    fillColor: 'green',
    strokeWeight: 2
  }
  map.data.setStyle(featureStyle);
}


google.maps.event.addDomListener(window, 'load', initialize);