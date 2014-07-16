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
function initialize () {
  var oakland = new google.maps.LatLng(37.8,-122.2);
  var mapOptions = {
    zoom: 12,
    center: oakland,
    mapTypeId: google.maps.MapTypeId.TERRAIN 
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

// Geocode centering on zip code.
// Need to add a check to ensure that this is a real address - 94616 sent me to eastern Europe?
geocoder = new google.maps.Geocoder();

function geocode () {
  var address = $('#address').val();
  geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[0]) {
          var googleLatLng = results[0].geometry.location;
          var lat = results[0].geometry.location.lat();
          var lng = results[0].geometry.location.lng();
          // var latlng = [lat,lng];
          map.setCenter(googleLatLng);
          submitdata(lat,lng);
        }
        else {
          console.log("Geocode function not working!")
        }
          // This places a marker in the center, which I do not want.
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

  // Rendering route.
  function submitdata (lat,lng) {
    console.log(lat)
    console.log(lng)
    $.getJSON('/route', {
      lat: lat.toString(),
      lng: lng.toString(),
      minDistance: $('input[name="min_distance"]').val(),
      maxDistance: $('input[name="max_distance"]').val(),
  }, function(routeJson) {
    // Load the GeoJSON monster stomp.
    var geoJson = routeJson
    console.log(geoJson);
    map.data.loadGeoJson(geoJson);
    // Set the styling.
     var featureStyle = {
     fillColor: 'green',
     strokeWeight: 10
     }
    map.data.setStyle(featureStyle);
  });
  return false;
};
  
  $(document).ready(function() {
    initialize();
    
    $('input#render').bind('click', function () {
      geocode();
    });
  });

