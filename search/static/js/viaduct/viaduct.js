var mapbox_key_elem = document.querySelector("#mapbox-key");
var mapbox_key = mapbox_key_elem.getAttribute('data-value');
var points_elem = document.querySelector("#map-data");
var points = points_elem.querySelectorAll('span');

var map = L.map('map').setView([25, 35], 2);
L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/{z}/{x}/{y}?access_token=' + mapbox_key, {maxZoom: 19}).addTo(map);
for(var i = 0; i < points.length; i++)
{
    var lat = points[i].getAttribute('data-lat');
    var lon = points[i].getAttribute('data-lon');
    var text = points[i].innerHTML;
    
    var point = L.circle([lat, lon], {fillColor: '#7F7FFF', radius: 100}).addTo(map);
    point.bindPopup(text);
}
