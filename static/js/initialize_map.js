// Declare the map & geocoder & feature.
var map;
var geocoder;
var feature;

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
        zoom: 12,
        center: oakland,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
                              mapOptions);
}

// Centers map on zip code. Runs on click of "Find A Route" button.
geocoder = new google.maps.Geocoder();

function centerMap() {
    var address = $('#address').val();
    geocoder.geocode({ 'address': address}, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                var googleLatLng = results[0].geometry.location;
                var lat = results[0].geometry.location.lat();
                var lng = results[0].geometry.location.lng();
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
    feature = map.data.loadGeoJson(js_file);
    // Set the styling.
    var featureStyle = {
            fillColor: 'green',
            strokeWeight: 10
        };
    map.data.setStyle(featureStyle);
    console.log("Rendering route was successful!");
    console.log(feature)
}

// Reset map to null to clear previous route.
function clearMap() {
    map.data.setMap(null);
    passIndex();
}

$(document).ready(function () {
    initialize();
    $('input#render').bind('click', function () {
        centerMap();
    });
    $('input#no').bind('click', function () {
        //clearMap();
        //console.log("clearMap called");
        passIndex();
        console.log("passIndex called"); 
    });
    $('input#yes').bind('click', function () {
    });
});

