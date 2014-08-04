// Declare the map & geocoder & feature.
var map,
    geocoder,
    i,
    lat,
    lng,
    routeIds, // route list returned from API call
    routeId;
console.log(lat)
console.log(lng)

// Console log.
function trace(message) {
    if (typeof console !== 'undefined') {
        console.log(message);
    }
}

// Create the map.
function initialize() {
    if (lat && lng) {
        center = new google.maps.LatLng(lat, lng);
    } else {
        // Default to Oakland (of course).
        center = new google.maps.LatLng(37.8, -122.2);
    }
    var mapOptions = {
        zoom: 10,
        center: center,
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
    center = new google.maps.LatLng(lat, lng);
    mapOptions = {
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
        istance: $('input[name="distance"]').val()
    }, function (route_ids) {
        routeIds = route_ids; // routeIds is an object
        console.log('API call successful!');
        showNextRoute();
    });
    return false;
}

// Defines route id to use for renderRoute ajax call. Increments index.
// Runs on each click of no button.
var index = 0;
function showNextRoute() {
    routeId = routeIds[index]; // routeId is a number
    routeId = routeId.toString();
    index++;
    renderRoute();
}

// Confirm route is loop or out-and-back 
function checkRoute() {
  renderRoute();
  addMarkers();
}

// Call to get route from database and render route.
function renderRoute() {
    // Load the GeoJSON ((monster stomp)).
    map.setZoom(14);
    map.data.loadGeoJson("/route/" + routeId);
    // Set the styling.
    var featureStyle = {
        strokeColor: 'green',
        strokeWeight: 10,
        strokeOpacity: 0.5
    };
    map.data.setStyle(featureStyle);
    console.log("Rendering route was successful!");
    // Hide existing banner/logo and pull up next banner/logo.
    $('#step1').hide();
    $('#logo1').hide();
    $('#step2').css("display", "block");
    $('#logo2').css("display", "block");
}

// Add route markers - start, end, and loop.
var startLat,
    startLng,
    endLat,
    endLng,
    startLatLng,
    endLatLng,
    startMarker,
    endMarker,
    startMarkerimage = 'img/startmarker.png',
    endMarkerimage= 'img/endmarker.png'
function addMarkers() {
    console.log("in addMarkers");
    $.getJSON('/markers', {
        route_id: routeId.toString()
    }, function (points) {
        // Place end marker first so it is visually behind start marker.
        startLat = points.start_lng;
        startLng = points.start_lat;
        startLatLng = new google.maps.LatLng(startLat, startLng);
        endLat = points.end_lng;
        endLng = points.end_lat;
        endLatLng = new google.maps.LatLng(endLat, endLng);
        // Currently disabled.
        //endMarker = new google.maps.Marker({
        //    position: endLatLng,
        //    map: map,
        //    title: "end",
        //    icon: endMarkerimage
        //});
        // Place start marker.

        startMarker = new google.maps.Marker({
            position: startLatLng,
            map: map,
            title: "start",
            icon: startMarkerimage,
            animation: google.maps.Animation.DROP
        });
        console.log(endLatLng);
        console.log(startLatLng);
        console.log(typeof startLatLng);
    });
}

// Map zoom and center on startMarker. Runs on click of yes button.
function zoomMarker() {
    $('#step2').hide();
    $('#logo2').hide();
    //$('#step2').css("display", "block");
    $('#logo3').css("display", "block");
    map.setZoom(25);
    map.panTo(startMarker.position);
}

// Used to round latitude and longitude values for location comparison.
function roundNumber(rnum, rlength) { 
    var newnumber = Math.round(rnum * Math.pow(10, rlength)) / Math.pow(10, rlength);
    return newnumber;
}

$(document).ready(function () {
    initialize();
    $body = $("body");
    // Show loading screen if Ajax call is more than 3000 milliseconds (3 sec).
    $(document).ajaxStart(function () {
        timer = setTimeout(function () {
            $body.addClass("loading");
        }, 3000);
    });
    $(document).ajaxComplete(function () {
        $body.removeClass("loading");
        clearTimeout(timer);
    });

    $('input#render').bind('click', function () {
        centerMap();
    });
    $('input#no').bind('click', function () {
        clearLayer();
    });
    $('input#yes').bind('click', function () {
        zoomMarker();
    });
    $('#new-route-link').bind('click',  function () {
        initialize();
    });
});



