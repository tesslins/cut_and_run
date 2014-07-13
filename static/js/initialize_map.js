var map;
function initialize() {
  // Create the map.
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 8,
    center: new google.maps.LatLng(39.7392,-104.9847)
  });

}

google.maps.event.addDomListener(window, 'load', initialize);