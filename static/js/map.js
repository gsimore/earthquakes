"use strict";


var map;
var geocoder;

function initMap() {
    // var uluru = {lat: -25.363, lng: 131.044};
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-34.397, 150.644);
    var mapOptions = {
        zoom: 4,
        center: latlng
    };
    var marker = new google.maps.Marker({
        position: latlng,
        map: map
    });
    map = new google.maps.Map(document.getElementById('eq-map'), mapOptions);
}


// Client Side Geocoding Below
// function codeAddress() {
//     var address = document.getElementById('station_address').value;
//     geocoder.geocode({'address': address}, function (results, status) {
//         if (status === 'OK') {
//             map.setCenter(results[0].geometry.location);
//             var marker = new google.maps.Marker({
//                 map: map,
//                 position: results[0].geometry.location
//             });
//         } else {
//             alert('Geocode was not successful for the following reason: ' + status);
//         }
//     });
// }
