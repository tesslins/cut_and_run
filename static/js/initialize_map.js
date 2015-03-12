// Declare the map & geocoder & feature.
var map,
    geocoder,
    i,
    lat,
    lng,
    routeIds, // route list returned from API call/database query
    routeId,
    routePoints,
    startLat,
    rstartLat,
    startLng,
    rstartLng,
    endLat,
    rendLat,
    endLng,
    rendLng,
    startLatLng,
    routeMarker;

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
// To do: Need to add a check to ensure that this is a real location.

// Ajax call for close-to-location MapMyFitness API call, returns list of route ids
// Runs on completion of centerMap function.
function submitData(lat, lng) {
    $.getJSON('/api', {
        lat: lat.toString(),
        lng: lng.toString(),
        distance: $('input[name="distance"]').val()
    }, function (route_ids) {
        routeIds = route_ids; // routeIds is an object
        showNextRoute();
    });
    return false;
}

// Defines route id to use for renderRoute ajax call. Increments index.
// Runs on each click of no button.
var index = 0;
function showNextRoute() {
    if (index <= 20) {
        console.log(index);
        routeId = routeIds[index]; // routeId is a number
        index++;
        checkRoute();
    }
}

// Ensure route is a loop or out and back - check that starting lat/lng and 
// ending lat/lng are near each other (within ~110 m).
function checkRoute() {
    $.getJSON('/markers', {
        route_id: routeId.toString()
    }, function (retVal) {
        $('body').addClass('loading');
        routePoints = retVal['points'];
        startLat = routePoints[0]['lat'];
        rstartLat = roundNumber(startLat, 3);
        startLng = routePoints[0]['lng'];
        rstartLng = roundNumber(startLng, 3);
        endLat = routePoints[routePoints.length -1]['lat'];
        rendLat = roundNumber(endLat, 3);
        endLng = routePoints[routePoints.length -1]['lng'];
        rendLng = roundNumber(endLng, 3);
        if (rstartLat == rendLat && rstartLng == rstartLng) {
            renderRoute();
        } else {
            showNextRoute();
        }
    });
}

// Render the route monster stomp!
function renderRoute() {
    $('body').removeClass('loading');
    map.setZoom(14);
    var routeCoordinates = [];
    for (var x = 0; x < routePoints.length; x++) {
        var tempLat = routePoints[x]['lat'];
        var tempLng = routePoints[x]['lng'];
        tempCoordinates = new google.maps.LatLng(tempLat, tempLng);
        routeCoordinates.push(tempCoordinates);
    }
    var routePath = new google.maps.Polyline({
        path: routeCoordinates,
        geodesic: true,
        strokeColor: '#00A651',
        strokeWeight: 8,
        strokeOpacity: 0.5
    });
    routePath.setMap(map);

    // Hide existing banner/logo and pull up next banner/logo.
    $('#step1').hide();
    $('#logo1').hide();
    $('#step2').css("display", "block");
    $('#logo2').css("display", "block");

    addMarkers();
}

// Drop maker at route start/finish after route polyline is plotted.
function addMarkers() {
    startLatLng = new google.maps.LatLng(startLat, startLng);
    var routeMarkerimage = 'img/startfinishmarker.png'; // fancy custom image nbd
    // Place start marker.
    routeMarker = new google.maps.Marker({
        position: startLatLng,
        map: map,
        icon: routeMarkerimage,
        animation: google.maps.Animation.DROP
    });
}

// Map zoom and center on startMarker. Runs on click of yes button.
function zoomMarker() {
    $('#step2').hide();
    $('#logo2').hide();
    $('#logo3').css("display", "block");
    map.setZoom(25);
    map.panTo(startMarker.position);
}

// Helper to round latitude and longitude values for location comparison.
function roundNumber(rnum, rlength) {
    var newnumber = Math.round(rnum * Math.pow(10, rlength)) / Math.pow(10, rlength);
    return newnumber;
}

$(document).ready(function () {
    initialize();
    /// Disable AJAX timer because current code has many short calls.
        // $body = $("body");
        // Show loading screen if Ajax call is more than 3000 milliseconds (3 sec).
        // $(document).ajaxStart(function () {
        //     timer = setTimeout(function () {
        //         $body.addClass("loading");
        //         console.log('loading');
        //     }, 2000);
        // });
        // $(document).ajaxComplete(function () {
        //     $body.removeClass("loading");
        //     console.log('removing loading');
        //     clearTimeout(timer);
        // });

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



