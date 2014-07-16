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
  var latlng = new google.maps.LatLng(37.8,-122.2);
  var mapOptions = {
    zoom: 12,
    center: latlng,
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
      if (status == google.maps.GeocoderStatus.OK) 
      {
          var lat_lng = results[0].geometry.location
          map.setCenter(lat_lng);
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
      return lat_lng;
  });
  
}

  // Rendering route.
  function submitdata (lat_lng) {
      $.getJSON($SCRIPT_ROOT + '/_route', {
        lat_lng: lat_lng,
        min_distance: $('input[name="min_distance"]').val(),
        max_distance: $('input[name="max_distance"]').val()
    }, function(data) {   
      // Load the GeoJSON monster stomp.
      
      // TO TEST - Declaring static json file as variable and loading onto map.
      // var geoJSON = 'js/geoJSON_single_route.json'
      // map.data.loadGeoJson(geoJSON);
      //$("#route_points").text(data.route_points); // this line - how to declare geoJson as varible?
        var geoJSON = 'js/geoJSON_single_route.json'
        map.data.loadGeoJson(geoJSON);
      
      // Set the styling.
      var featureStyle = {
      // fillColor: 'green',
      strokeWeight: 10
      }
      map.data.setStyle(featureStyle);
    });
    return false;
  };
  
  $(document).ready(function() {
    initialize();
    
    $('input#render').bind('click', function () {
      var lat_lng = geocode();
      submitdata(lat_lng);
    });
  });

