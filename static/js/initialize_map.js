// Declare the map & geocoder & feature.
var map;
var geocoder;
var i;
var lat;
var lng;
var routeIds; // list from API call
var routeId;


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
            console.log(
                "centerMap function was not successful because: "
                    + status
            );
        }
    });
}
// To fix: Need to add a check to ensure that this is a real location.

// Ajax call for initial MapMyFitness API call, returns list of route ids
// Runs on completion of centerMap function.
function submitData(lat, lng) {
    $.getJSON('/api', {
        lat: lat.toString(),
        lng: lng.toString(),
        distance: $('input[name="distance"]').val()
    }, function (route_ids) {
        routeIds = route_ids; // routeIds is an object
        console.log('API call successful!');
        showNextRoute();
    });
    return false;
}

// Defines route id to use for renderRoute ajax call. Increments index.
// Runs on click of no button
var index = 0;
function showNextRoute() {
    routeId = routeIds[index]; // routeId is a number
    routeId = routeId.toString();
    index++;
    renderRoute();
}

// Call to get route from database and render route.
function renderRoute() {
    //routeId = routeId;
    // Load the GeoJSON ((monster stomp)).
    map.data.loadGeoJson("/route/" + routeId);
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
    addMarkers();
}

// Add route beginning and end markers.
var startLat;
var startLng;
var endLat;
var endLng;
var startLatLng;
var endLatLng;
var startMarker;
var endMarker;
var startMarkerimage = 'img/startmarker.png';
var endMarkerimage;
function addMarkers() {
    console.log("in addMarkers");
    $.getJSON('/markers', {
        route_id: routeId.toString()    
    }, function (points) {
        startLat = points.start_lng;
        startLng = points.start_lat;
        startLatLng = new google.maps.LatLng(startLat, startLng);
        endLatLng = new google.maps.LatLng(endLat, endLng);
        startMarker = new google.maps.Marker({
            position: startLatLng,
            map: map,
            title: "start",
            icon: startMarkerimage
        });
        //endMarker = new google.maps.Marker({
        //    position: endLatLng,
        //    map: map,
        //    title: "end",
        //    visible: true
        //});
    });
}

// Add route distance.

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

