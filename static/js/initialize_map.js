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
    // Return routesObject to Javascript, call showNextRoute to get Index variable. Do I need to pass variable to access it in a different function?
    renderRoute(routeJson);
    console.log("MapMyFitness API call was successful!");
});
return false;
}

// Passes index to Python, increments index after call. Runs on click of no button
function passIndex() {
  var value = parseInt(document.getElementById('no').value, 0);
  console.log("inside function")
  console.log(value)
  value = isNaN(value) ? 0 : value;
  document.getElementById('number').value = value;
  $.getJSON('/pass_index', {
    index: value.toString(),
  }, function(index) {
    // Increments each time index is passed, aka each time a new route object is created.
    console.log(index);
  });
value++;
}

// Get the next route. Runs on click of no button.
function showNextRoute() {
  $.getJSON('/create_route' , {
    getroute: 'yesplease'
  } , function(routeJson) {
    renderRoute(routeJson);
  });
}
                                
// Render route.
function renderRoute (routeJson) {
  // Load the GeoJSON ((monster stomp)).
  var pyGeoJson = routeJson;
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

  
  $(document).ready(function() {
    initialize();
    
    $('input#render').bind('click', function() {
      centerMap();
    });
    
    $('input#no').bind('click', function() { 
      passIndex();
      console.log("passIndex called");
      showNextRoute();
      console.log("showNextRoute called")
    });
    
    $('input#yes').bind('click', function() {
      
    });
  });

