function heatmapper(region, routesJson) {

document.getElementById('routes_micro_container').innerHTML = "<div id='map' style='width: 1200px; height:800px;'></div>";
var map = L.map('map').setView([35.0, 25.0], 14);

var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 17,
    minZoom: 1,
    max:1.0,
    minOpacity:1,
    gradient:{0.15: 'blue', 0.25: 'lime',0.5:'orange', 1: 'red'},
    radius:25
}).addTo(map);


var heat = L.heatLayer(routesJson).addTo(map),
    draw = true;
}

