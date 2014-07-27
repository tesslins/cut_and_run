// Declare the map & geocoder & feature.
var map;
var geocoder;
var i;
var lat;
var lng;

// Console log.
function trace(message) {
    if (typeof console !== 'undefined') {
        console.log(message);
    }
}

// Create the map.
function initialize() {
    var oakland = new google.maps.LatLng(37.8, -122.2);
    var mapOptions = {
        zoom: 14,
        center: oakland,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);
}

// Set map to null to clear data layer containing previous route.
function clearLayer() {
    map.data.setMap(null);
    reinitialize();
    console.log("data layer cleared");
}

// Recreate map between routes.
function reinitialize() {
    var center = new google.maps.LatLng(lat, lng);
    var mapOptions = {
        zoom: 14,
        center: center,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);
    showNextRoute();
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

// Passes index to Python to get next route, increments index after call.
// Runs on click of no button
var value = 1; // Must be 1, first time is default to 0 (in Python).
function showNextRoute() {
    $.getJSON('/create_route', {
        index: value.toString()
    }, function (js_file) {
        renderRoute(js_file);
        console.log('Index passed and value incremented.');
    });
    value++;
    console.log(value);
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



$(document).ready(function () {
    initialize();
    $('input#render').bind('click', function () {
        centerMap();
    });
    $('input#no').bind('click', function () {
        clearLayer();

    });
    $('input#yes').bind('click', function () {
    });
});

