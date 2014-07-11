var map;
function initialize() {
  // Create a simple map.
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 8,
    center: {lat: 39.7392, lng: -104.9847}
  });

  // Load a GeoJSON from the same server as our demo.
  map.data.loadGeoJson('/geo_json_points.json');
}

google.maps.event.addDomListener(window, 'load', initialize);