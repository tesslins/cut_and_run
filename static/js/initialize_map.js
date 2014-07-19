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
    zoom: 8,
    center: oakland,
    mapTypeId: google.maps.MapTypeId.TERRAIN 
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

// Centers map on zip code. Runs on click of "Find A Route" button.
geocoder = new google.maps.Geocoder();

function centerMap () {
  var address = $('#address').val();
  geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[0]) {
          var googleLatLng = results[0].geometry.location;
          var lat = results[0].geometry.location.lat();
          var lng = results[0].geometry.location.lng();
          map.setCenter(googleLatLng);
          submitdata(lat,lng);
        }
        else {
          console.log("centerMap function not working!")
        }
      } 
      else 
      {
        alert("centerMap function was not successful for the following reason: " + status);
      }
  });
}
// Need to add a check to ensure that this is a real address - 94616 sent me to eastern Europe?

// Call to Python for initial MapMyFitness API call. Runs on click of "Find A Route" button.
function submitdata (lat,lng) {
  $.getJSON('/api_call', {
    lat: lat.toString(),
    lng: lng.toString(),
    minDistance: $('input[name="min_distance"]').val(),
    maxDistance: $('input[name="max_distance"]').val(),
}, function(routeJson) {
    // Send routeJson to renderRoute.
    console.log("MapMyFitness API call was successful!")
    renderRoute(routeJson);
});
return false;
}

// Call to Python for additional route after initial API call. Runs on click of "Nope" button.
var index = 1; // starts at [1] because [0] is the initial route render
function showNextRoute() {
  $.getJSON('/pass_index', {
    index: index.toString(),
  }, function(routeJson) {
    // Send routeJson to renderRoute.
    renderRoute(routeJson);
    index = index + 1
    console.log(index)
  });
}

// Render route.
function renderRoute (routeJson) {
  // Load the GeoJSON ((monster stomp)).
  var pyGeoJson = JSON.stringify(routeJson);
  var staticGeoJson = 'js/geoJSON_route_Oakland.json';
  map.data.loadGeoJson(staticGeoJson);
  // Set the styling.
   var featureStyle = {
   fillColor: 'green',
   strokeWeight: 10
   }
  map.data.setStyle(featureStyle);
  console.log("Rendering route was successful!")
}

// Stores route in the session. Runs on the click of yes button.
function storeRoute() {
  
}

  
  $(document).ready(function() {
    initialize();
    
    $('input#render').bind('click', function() {
      centerMap();
    });
    
    $('input#no').bind('click', function() { 
      showNextRoute();
      console.log("Leaving main function");
    });
    
    $('input#yes').bind('click', function() {
      storeRoute();
      
    });
  });

