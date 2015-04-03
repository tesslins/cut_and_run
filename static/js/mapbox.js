// Declare variables
var map, // map object for Google Map
    geocoder, // geocoded user-entered zipcode for Google Map
    lat, // latitude from user-entered zipcode
    lng, // longitude from user-entered zipcode
    routeIds, // route list returned from API call/database query
    routeId, // single route ID from routeIds array
    routePoints, // array of all points from single route
    startLat, // latitude of route start point
    rstartLat, // rounded latitude of route start point
    startLng, // longitude of route start point
    rstartLng, // rounded longitude of route start point
    endLat, // latitude of end route point
    rendLat, // rounded latitude of end route point
    endLng, // longitude of end route point
    rendLng, // rounded longitude of end route point
    startLatLng, // single point to drop the start & finish marker
    routeMarker; // custom route marker for Google Map

// Console log
function trace(message) {
    if (typeof console !== 'undefined') {
        console.log(message);
    }
}

// Create the map.
// ?? Why is map initializing twice with Mapbox?
function initialize() {
    if (!lat && !lng) {
        // Default to Oakland of course.
        lat = 37.8;
        lng = -122.2;
    }

    // L.mapbox.map(element, id|url|tilejson, options(optional))
    map = L.mapbox.map('map-canvas', 'examples.map-i86l3621')
        .setView([lat, lng], 10);
}

// Set map to null to clear data layer containing previous route.
function clearLayer() {
    map.remove();
    reinitialize();
}

// Recreate map between routes.
// ?? Must be a better way to do this, try to add & remove layers?
function reinitialize() {
    map = L.mapbox.map('map-canvas', 'examples.map-i86l3621')
        .setView([lat, lng], 10);
    showNextRoute();
}

// Centers map on zip code. Runs on click of "Find A Route" button.
// Mapbox Forward geocoding - place name (ie zipcode) to lat/lng
function centerMap() {
    // address is zipcode
    var address = $('#address').val();
    // url example http://api.tiles.mapbox.com/v4/geocode/{index}/{query}.json?access_token=<your access token>
    var geocodeUrl = 'http://api.tiles.mapbox.com/v4/geocode/mapbox.places/' + address + '.json?access_token=' + L.mapbox.accessToken;
     $.getJSON(geocodeUrl, function( data ) {
        // definitely returns backwards, why??!
        lat = data.features[0].center[1];
        lng = data.features[0].center[0];
        var centerLatLng = [lat, lng];
        map.setView(centerLatLng, 13);
        submitData(lat, lng);
     });
}
// To do: Add an error check to ensure that zipcode is actually real.

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

// Map zoom and center on routeMarker. Runs on click of yes button.
function zoomMarker() {
    $('#step2').hide();
    $('#logo2').hide();
    $('#logo3').css("display", "block");
    map.setZoom(25);
    map.panTo(routeMarker.position);
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



