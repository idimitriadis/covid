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

    var cdfGR = getResultFromEndpoint('/casesCountryCDF/GREECE');
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
        oddsglobaldata.push({'Cases': keyVal, 'ODDS': Math.log10(value)});
    }

    var oddsGR = getResultFromEndpoint('/casesCountryODDS/GREECE');

    var oddsGRdata = [];
    for (let [key, value] of Object.entries(oddsGR)) {
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        oddsGRdata.push({'Cases': keyVal, 'ODDS': Math.log10(value)});
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


    var casesPerCapita = getResultFromEndpoint('/casesPerCapita');
    var casesPerCapitaData = [];
    for (let [key, value] of Object.entries(casesPerCapita)) {
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        casesPerCapitaData.push({'Gdp': keyVal, 'Cases': Math.log10(value + 1), 'LinearCases': value});
    }

    Morris.Bar({
        element: 'cases-per-capita',
        data: casesPerCapitaData,
        xkey: 'Gdp',
        ykeys: ['Cases'],
        labels: ['Κρούσματα'],
        // parseTime: false,
        xLabelAngle: 90,
        barColors: ['#0277bd']
    });

    var capitaCountry = getResultFromEndpoint('/capitaPerCountry');
    var capitaCountryData = [];
    for (let [key, value] of Object.entries(capitaCountry)) {
        capitaCountryData.push({'Country': key, 'Capita': value});
    }

    Morris.Bar({
        element: 'countries_per_capita',
        data: capitaCountryData,
        xkey: 'Country',
        ykeys: ['Capita'],
        labels: ['ΑΕΠ'],
        // parseTime: false,
        xLabelAngle: 90,
        barColors: ['#00838f']
    });

    var humanfree = getResultFromEndpoint('/human_freedom');
    var freedom = [];
    for (let [key, value] of Object.entries(humanfree)) {
        freedom.push({'Cases': Math.log10(value + 1), 'human_freedom': key});
    }

    Morris.Bar({
        element: 'totalCasesHumanFreedom',
        data: freedom,
        xkey: 'human_freedom',
        ykeys: ['Cases'],
        labels: ['Cases'],
        // parseTime: false,
        xLabelAngle: 45,
        barColors: ['#9575cd']
    });

    var humanfreeCountry = getResultFromEndpoint('/human_freedom_per_country');
    console.log(humanfreeCountry);
    var freedomCountry = [];
    for (let [key, value] of Object.entries(humanfreeCountry)) {
        freedomCountry.push({'Cases': value[0], 'Country': value[1], 'human_freedom': key});
    }

    Morris.Bar({
        element: 'humanfreedomCountry',
        data: freedomCountry,
        xkey: 'human_freedom',
        ykeys: ['Cases', 'Country'],
        labels: ['Cases', 'Country'],
        // parseTime: false,
        xLabelAngle: 45,
        barColors: ['#9575cd', '#00838f']
    });


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
        datas.push({'Day': key, 'Cases1': value, 'Cases2': totalCasesDay2[key]});
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