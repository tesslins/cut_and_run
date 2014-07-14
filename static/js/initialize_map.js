//declare namespace
var runAround = {};

// Declare the map & geocoder and always console log.
var map;
var geocoder;

function trace(message) 
{
    if (typeof console != 'undefined') 
    {
        console.log(message);
    }
}

// Create the map.
runAround.initialize = function() {
  var latlng = new google.maps.LatLng(37.8,-122.2);
  var mapOptions = {
    zoom: 12,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.TERRAIN 
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

// Geocode search box for zip code.
geocoder = new google.maps.Geocoder();
runAround.geocode = function() 
{
  var address = $('#address').val();
  geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) 
      {
          map.setCenter(results[0].geometry.location);
          // This places a marker in the center, don't want it.
          //var marker = new google.maps.Marker({
          //    map: map, 
          //    position: results[0].geometry.location
          //});
      } 
      else 
      {
          alert("Geocode was not successful for the following reason: " + status);
      }
  });
}
