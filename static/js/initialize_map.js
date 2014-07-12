var map;
function initialize() {
  // Create the map.
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 12,
    center: {lat: 37.8, lng: -122.2}
  });

}

google.maps.event.addDomListener(window, 'load', initialize);