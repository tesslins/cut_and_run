// Declare the map & geocoder & feature.
var map;
var geocoder;
var i;
var lat;
var lng;
// following two variables are for direction calculation
var directionsDisplay; 
var directionsService = new google.maps.DirectionsService();

// Console log.
function trace(message) {
    if (typeof console !== 'undefined') {
        console.log(message);
    }
}

// Create the map.
function initialize() {
    directionsDisplay = new google.maps.DirectionsRenderer();
    var oakland = new google.maps.LatLng(37.8, -122.2);
    var mapOptions = {
        zoom: 13,
        center: oakland,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);
    directionsDisplay.setMap(map);
}

// TEST - Calculating directions.
function calcRoute() {
    var start = '37.8044, -122.2708';
    var end = '37.8717, -122.2728';
    var request = {
  origin: start,
  destination: end,
  travelMode: google.maps.TravelMode.WALKING,
  unitSystem: google.maps.UnitSystem.IMPERIAL
};
    directionsService.route(request, function (response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });
    console.log("Directions calculated")
}

// Recreate map between routes.
function reinitialize() {
    var center = new google.maps.LatLng(lat, lng);
    var mapOptions = {
        zoom: 13,
        center: center,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);
    passIndex();
}

// Centers map on zip code. Runs on click of "Find A Route" button.
geocoder = new google.maps.Geocoder();
function centerMap() {
    var address = $('#address').val();
    geocoder.geocode({ 'address': address}, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                var googleLatLng = results[0].geometry.location;
                lat = results[0].geometry.location.lat();
                lng = results[0].geometry.location.lng();
                map.setCenter(googleLatLng);
                submitData(lat, lng);
            } else {
                console.log("centerMap function not working!");
            }
        } else {
            alert(
                "centerMap function was not successful because: "
                    + status
            );
        }
    });
}
// To fix: Need to add a check to ensure that this is a real US zip code.

// Call to Python for initial MapMyFitness API call.
// Runs on completion of centerMap function.
function submitData(lat, lng) {
    $.getJSON('/api_call', {
        lat: lat.toString(),
        lng: lng.toString(),
        minDistance: $('input[name="min_distance"]').val(),
        maxDistance: $('input[name="max_distance"]').val()
    }, function (js_file) {
        renderRoute(js_file);
        console.log("MapMyFitness API call was successful.");
    });
    return false;
}

// Passes index to Python, increments index after call.
// Runs on click of no button
var value = 1; // Must be 1, first time is default to 0 (in Python).
function passIndex() {
    $.getJSON('/pass_index', {
        index: value.toString()
    }, function (index) {
    // Increments value each time index is passed.
        showNextRoute(index);
        console.log(typeof index);
        value++;
        console.log('Index passed and value incremented.');
    });
}
// To fix: an increment without Python call, duh! Get rid of this function!

// Get the next route. Runs on click of no button.
function showNextRoute(index) {
    $.getJSON('/create_route', {
        index: index.toString()
    }, function (js_file) {
        renderRoute(js_file);
    });
}

// Render route.
function renderRoute(js_file) {
    // Load the GeoJSON ((monster stomp)).
    map.data.loadGeoJson(js_file);
    // Set the styling.
    var featureStyle = {
            strokeColor: 'green',
            strokeWeight: 10,
            strokeOpacity: 0.5
        };
    map.data.setStyle(featureStyle);
    console.log("Rendering route was successful!");
    $('#step1').hide();
    $('#step2').css("display", "block");
}

// Set map to null to clear data layer containing previous route.
function clearLayer() {
    map.data.setMap(null);
    reinitialize();
    console.log("data layer cleared")
    
}

$(document).ready(function () {
    initialize();
    $('input#render').bind('click', function () {
        centerMap();
    });
    $('input#no').bind('click', function () {
        clearLayer();

    });
    $('input#yes').bind('click', function () {
        calcRoute();
        console.log("Calculating route.")
    });
});

