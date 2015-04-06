// Declare variables
var map, // map object
    geocoder, // geocoded user-entered zipcode
    lat, // latitude from user-entered zipcode
    lng, // longitude from user-entered zipcode
    routeIds, // route list returned from API call
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
    routeMarker; // custom route marker

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
    geocoder = L.mapbox.geocoder('mapbox.places');
    geocoder.query(address, showCenterMap);
}
// To do: Add an error check to ensure that zipcode is actually real.

function showCenterMap(err, data) {
    // centers by bounds from zipcode
    if (data.lbounds) {
        map.fitBounds(data.lbounds);
    } else if (data.latlng) {
        map.setView([data.latlng[0], data.latlng[1]], 13);
    }
    submitData(lat, lng);
}

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
        routeId = routeIds[index]; // routeId is a number
        checkRoute();
        index++;
    }
}

// Ensure route is a loop or out and back - check that starting lat/lng and 
// ending lat/lng are within ~110 meters of each other.
function checkRoute() {
    $('body').addClass('loading');
    $.getJSON('/markers', {
        route_id: routeId.toString()
    }, function (routeData) {
        routePoints = routeData['points'];
        startLat = routePoints[0]['lat'];
        rstartLat = roundNumber(startLat, 3);
        startLng = routePoints[0]['lng'];
        rstartLng = roundNumber(startLng, 3);
        endLat = routePoints[routePoints.length -1]['lat'];
        rendLat = roundNumber(endLat, 3);
        endLng = routePoints[routePoints.length -1]['lng'];
        rendLng = roundNumber(endLng, 3);
        if (rstartLat == rendLat && rstartLng == rstartLng) {
            renderRoute(routeData);
        } else {
            showNextRoute();
        }
    });
}

// Render the route monster stomp!
function renderRoute(routeData) {
    $('body').removeClass('loading');
    // map.setZoom(14); // need to replace this to mapbox-friendly zoom
    var polylinePoints = []; // for polyline
    for (var i = 0; i < routePoints.length; i++) {
        var tempLat = routePoints[i]['lat'];
        var tempLng = routePoints[i]['lng'];
        // add as list to create polyline
        polylinePoints.push([tempLat, tempLng]);
    }
    // Set polyline options & create  polyline
    var polylineOptions = {
        color: '#00A651'
    };
    var polyline = L.polyline(polylinePoints, polylineOptions).addTo(map);

    // Hide existing banner/logo and pull up next banner/logo.
    $('#step1').hide();
    $('#logo1').hide();
    $('#step2').css("display", "block");
    $('#logo2').css("display", "block");

    addMarker();
}

// Drop maker at route start/finish after route polyline is plotted.
function addMarker() {
    L.mapbox.featureLayer({
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: [
          routePoints[0]['lng'],
          routePoints[0]['lat']
        ]
    },
    properties: {
        title: 'route start & end',
        'marker-size': 'large',
        'marker-color': '#00A651',
        'marker-symbol': 'pitch'
    }
}).addTo(map);
}

// Map zoom and center on routeMarker. Runs on click of yes button.
function zoomMarker() {
    $('#step2').hide();
    $('#logo2').hide();
    $('#logo3').css("display", "block");
    map.setView([routePoints[0]['lat'], routePoints[0]['lng']], 15);
}

// Helper to round latitude and longitude values for location comparison.
function roundNumber(rnum, rlength) {
    var newnumber = Math.round(rnum * Math.pow(10, rlength)) / Math.pow(10, rlength);
    return newnumber;
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
        zoomMarker();
    });
    $('#new-route-link').bind('click',  function () {
        initialize();
    });
});



