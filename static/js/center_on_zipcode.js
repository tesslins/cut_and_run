var map;
var geocoder;
function initialize() {
  // Create the map.
  geocode = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(39.7392,-104.9847);
  var mapOptions = {
    zoom: 8,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.TERRAIN 
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

var zipCode = JSON.stringify(94606);
function codeAddress(zipCode) {
    geocoder.geocode( { 'address': zipCode}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        //Got result, center the map and put it out there
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
  }
  
  google.maps.event.addDomListener(window, 'load', initialize, codeAddress);