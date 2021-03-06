var Script = function () {

    function getResultFromEndpoint(endpoint) {
        const host = 'http://127.0.0.1:5000';

        var tmp = null;
        $.ajax(
            {
                type: 'GET',
                async: false,
                url: host + endpoint,
                dataType: 'json',
                success: data => {
                    tmp = data;
                },
                error: function (x, e) {
                    alert('server error occoured');
                    if (x.status == 0) {
                        alert('0 error');
                    } else if (x.status == 404) {
                        alert('404 error');
                    } else if (x.status == 500) {
                        alert('500 error');
                    } else if (e == 'parsererror') {
                        alert('Error.nParsing JSON Request failed.');
                    } else if (e == 'timeout') {
                        alert('Time out.');
                    } else {
                        alert(x.responseText);
                    }
                }
            }
        );
        return tmp;
    }

    var cdfglobal = getResultFromEndpoint('/casesCDF');
    var cdfglobaldata = [];
    for (let [key, value] of Object.entries(cdfglobal)) {
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        cdfglobaldata.push({'Cases': keyVal, 'CDF': value});
    }

    var cdfGR = getResultFromEndpoint('/casesCountryCDF/Greece');
    var cdfGRdata = [];
    for (let [key, value] of Object.entries(cdfGR)) {
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        cdfGRdata.push({'Cases': keyVal, 'CDF': value});
    }

    Morris.Line({
        element: 'cdf-global',
        data: cdfglobaldata,
        xkey: 'Cases',
        ykeys: ['CDF'],
        labels: ['CDF'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#ffeb3b']
    });

    Morris.Line({
        element: 'cdf-greece',
        data: cdfGRdata,
        xkey: 'Cases',
        ykeys: ['CDF'],
        labels: ['CDF'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#f57f17']
    });


    var oddsglobal = getResultFromEndpoint('/casesODDS');
    var oddsglobaldata = [];
    for (let [key, value] of Object.entries(oddsglobal)) {
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        oddsglobaldata.push({'Cases': keyVal, 'ODDS': Math.log10(value+1)});
    }

    var oddsGR = getResultFromEndpoint('/casesCountryODDS/Greece');

    var oddsGRdata = [];
    for (let [key, value] of Object.entries(oddsGR)) {
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        oddsGRdata.push({'Cases': keyVal, 'ODDS': Math.log10(value+1)});
    }

    Morris.Line({
        element: 'pdf-global',
        data: oddsglobaldata,
        xkey: 'Cases',
        ykeys: ['ODDS'],
        labels: ['ODDS'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#81c784']
    });

    Morris.Line({
        element: 'pdf-greece',
        data: oddsGRdata,
        xkey: 'Cases',
        ykeys: ['ODDS'],
        labels: ['ODDS'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#2e7d32']
    });

    var capitacases = getResultFromEndpoint('/capita_and_cases_per_country');
    // console.log(humanfreeCountry);
    var capitacasesData = [];
    for (let [key, value] of Object.entries(capitacases)) {
        capitacasesData.push({'Country': key, 'Cases':Math.log(value[0]+1), 'Corruption': Math.log(value[1]+1.1)});
    }

    Morris.Bar({
        element: 'cases-per-capita',
        data: capitacasesData,
        xkey: 'Country',
        ykeys: ['Cases', 'Corruption'],
        labels: ['Cases', 'Corruption'],
        // parseTime: false,
        xLabelAngle: 90,
        gridTextSize: 8,
        barColors: ['#33FF64','#FF336E' ]
    });

    var chinaeu = getResultFromEndpoint('/china_vs_EU');
    // console.log(humanfreeCountry);
    var chinaeudata = [];
    for (let [key, value] of Object.entries(chinaeu)) {
        chinaeudata.push({'Date': key, 'EU Cases':value[0], 'CN Cases': value[1]});
    }

    Morris.Bar({
        element: 'china-eu',
        data: chinaeudata,
        xkey: 'Date',
        ykeys: ['EU Cases', 'CN Cases'],
        labels: ['EU Cases', 'CN Cases'],
        // parseTime: false,
        xLabelAngle: 90,
        gridTextSize: 8,
        barColors: ['#4733FF','#FF3352' ]
    });

    var humanfreeCountry = getResultFromEndpoint('/human_freedom_per_country');
    // console.log(humanfreeCountry);
    var freedomCountry = [];
    for (let [key, value] of Object.entries(humanfreeCountry)) {
        freedomCountry.push({'Country': key, 'Cases':Math.log(value[0]+1), 'human_freedom': value[1]});
    }

    Morris.Bar({
        element: 'humanfreedomCountry',
        data: freedomCountry,
        xkey: 'Country',
        ykeys: ['Cases', 'human_freedom'],
        labels: ['Cases', 'human_freedom'],
        // parseTime: false,
        xLabelAngle: 90,
        gridTextSize: 8,
        barColors: ['#03a9f4', '#ffc107']
    });

    // GLOBAL MAP
    var mapped = getResultFromEndpoint('/mapped_results');
    var markers = [];
    for (let [key, value] of Object.entries(mapped)) {
        markers.push({'Country': key, 'lat':value[0], 'lng':value[1],'Deaths':value[2],'Cases':value[3]});
    }

    var map = L.map( 'map', {
    center: [42.295999 , 23.225999],
    minZoom: 1,
    zoom: 3
    });

    L.tileLayer( 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
      subdomains: ['a', 'b', 'c']
    }).addTo( map );

    var myURL = jQuery( 'script[src$="morris-plain.js"]' ).attr( 'src' ).replace( 'morris-plain.js', '' );

    var myIcon = L.icon({
      iconUrl: myURL + '/covid.png',
      iconRetinaUrl: myURL + '/covid.png',
      iconSize: [29, 24],
      iconAnchor: [9, 21],
      popupAnchor: [0, -14]
    });

    for ( var i=0; i < markers.length; ++i )
    {L.marker( [markers[i].lat, markers[i].lng], {icon: myIcon} )
      .bindPopup( "<strong> Country:</strong>"+markers[i].Country+"<br>"+"<strong>Deaths:</strong>"+
        markers[i].Deaths+"<br>"+"<strong>Cases:</strong>"+markers[i].Cases)
      .addTo( map );}

      // GREEK MAP
    // var mappedGR = getResultFromEndpoint('/greek_data');
    // var markersGR = [];
    // for (let [key, value] of Object.entries(mappedGR)) {
    //     markersGR.push({'City': key, 'Cases':value[0], 'Deaths':value[1],'lat':value[2],'lon':value[3]});
    // }
    // var mapGR = L.map( 'mapGR', {
    // center: [38.995368 , 21.987713],
    // minZoom: 2,
    // zoom: 7
    // });

    // L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //   attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    //   subdomains: ['a', 'b', 'c']
    // }).addTo( mapGR );

    // var myURL = jQuery( 'script[src$="morris-plain.js"]' ).attr( 'src' ).replace( 'morris-plain.js', '' );

    // var myIcon = L.icon({
    //   iconUrl: myURL + '/covid.png',
    //   iconRetinaUrl: myURL + '/covid.png',
    //   iconSize: [29, 24],
    //   iconAnchor: [9, 21],
    //   popupAnchor: [0, -14]
    // });

    // for ( var i=0; i < markersGR.length; ++i )
    // {
    //  L.marker( [markersGR[i].lat, markersGR[i].lon], {icon: myIcon} )
    //   .bindPopup( "<strong> City:</strong>"+markersGR[i].City+"<br>"+"<strong>Deaths:</strong>"+markersGR[i].Deaths+"<br>"+"<strong>Cases:</strong>"+markersGR[i].Cases)
    //   .addTo( mapGR );}



}();

function compareCases() {
    document.getElementById('cases-per-day').innerHTML = "";
    const country1 = document.getElementById("selectField1").value;
    const country2 = document.getElementById("selectField2").value;

    var totalCasesDay1 = null;
    if (country1 === 'WORLD'){
        totalCasesDay1 = getResultFromEndpoint('/totalCasesDay');
    }
    else {
        totalCasesDay1 = getResultFromEndpoint('/casesPerSpecificCountry/' + country1);
    }

    var totalCasesDay2 = null;
    if (country2 === 'WORLD'){
        totalCasesDay2 = getResultFromEndpoint('/totalCasesDay');
    }
    else {
        totalCasesDay2 = getResultFromEndpoint('/casesPerSpecificCountry/' + country2);
    }

    var datas = [];
    for (let [key, value] of Object.entries(totalCasesDay1)) {
        if (key in totalCasesDay2){
            datas.push({'Day': key, 'Cases1': Math.log(value+1), 'Cases2': Math.log(totalCasesDay2[key]+1)});
        }
        else {
            datas.push({'Day': key, 'Cases1': Math.log(value+1), 'Cases2': Math.log(1)});
        }

    }

    Morris.Line({
        element: 'cases-per-day',
        data: datas,
        xkey: 'Day',
        ykeys: ['Cases1', 'Cases2'],
        labels: ['Κρούσματα (' + country1 + ')', 'Κρούσματα (' + country2 + ')'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#d32f2f', '#3498dB']
    });

}

function compareDeaths() {
    document.getElementById('death-ratio').innerHTML = "";
    const country1 = document.getElementById("selectFieldDeath1").value;
    const country2 = document.getElementById("selectFieldDeath2").value;

    var totalCasesDay1 = null;
    var totalDeathsDay1 = null;
    if (country1 === 'WORLD'){
        totalCasesDay1 = getResultFromEndpoint('/totalCasesDay');
        totalDeathsDay1 = getResultFromEndpoint('/totalDeathsDay');
    }
    else {
        totalCasesDay1 = getResultFromEndpoint('/casesPerSpecificCountry/' + country1);
        totalDeathsDay1 = getResultFromEndpoint('/deathsPerSpecificCountry/' + country1);
    }

    var totalCasesDay2 = null;
    var totalDeathsDay2 = null;
    if (country2 === 'WORLD'){
        totalCasesDay2 = getResultFromEndpoint('/totalCasesDay');
        totalDeathsDay2 = getResultFromEndpoint('/totalDeathsDay');
    }
    else {
        totalCasesDay2 = getResultFromEndpoint('/casesPerSpecificCountry/' + country2);
        totalDeathsDay2 = getResultFromEndpoint('/deathsPerSpecificCountry/' + country2);
    }

    var deathsPerDay = [];
    var casesUpToNow1 = 0;
    var casesUpToNow2 = 0;
    var deathsUpToNow1 = 0;
    var deathsUpToNow2 = 0;
    for (let [key, value] of Object.entries(totalDeathsDay1)) {
        if (key in totalCasesDay1) {
            casesUpToNow1 += totalCasesDay1[key];
        }
        if (key in totalCasesDay2) {
            casesUpToNow2 += totalCasesDay2[key];
        }
        deathsUpToNow1 += value;
        if (key in totalDeathsDay2) {
            deathsUpToNow2 += totalDeathsDay2[key];
        }

        if (casesUpToNow1 === 0) {
            if (casesUpToNow2 === 0) {
                deathsPerDay.push({'Day': key, 'Cases1': 0, 'Cases2': 0});
            } else {
                deathsPerDay.push({
                    'Day': key,
                    'Cases1': 0,
                    'Cases2': (deathsUpToNow2 / casesUpToNow2 * 100).toFixed(2)
                });
            }
        } else {
            if (casesUpToNow2 === 0) {
                deathsPerDay.push({
                    'Day': key,
                    'Cases1': (deathsUpToNow1 / casesUpToNow1 * 100).toFixed(2),
                    'Cases2': 0
                });
            } else {
                deathsPerDay.push({
                    'Day': key,
                    'Cases1': (deathsUpToNow1 / casesUpToNow1 * 100).toFixed(2),
                    'Cases2': (deathsUpToNow2 / casesUpToNow2 * 100).toFixed(2)
                });
            }

        }
    }

    Morris.Line({
        element: 'death-ratio',
        data: deathsPerDay,
        xkey: 'Day',
        ykeys: ['Cases1', 'Cases2'],
        labels: ['Ποσοστό Θανάτων (' + country1 + ')', 'Ποσοστό Θανάτων (' + country2 + ')'],
        postUnits: ['%'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#d32f2f', '#3498dB']
    });

}