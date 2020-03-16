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


    var totalCasesDay = getResultFromEndpoint('/totalCasesDay');
    var totalCasesDayGR = getResultFromEndpoint('/casesPerSpecificCountry/Greece');

    var datas=[];
    for (let[key,value] of Object.entries(totalCasesDay)){
      datas.push({'Day':key,'CasesGlobal':value, 'CasesGreece':totalCasesDayGR[key]});
    }

    Morris.Line({
        element: 'cases-per-day',
        data: datas,
        xkey: 'Day',
        ykeys: ['CasesGlobal', 'CasesGreece'],
        labels: ['Κρούσματα Παγκοσμίως', 'Κρούσματα στην Ελλάδα'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#d32f2f', '#3498dB']
      });

    var totalDeathsDay = getResultFromEndpoint('/totalDeathsDay');
    var totalDeathsDayGR = getResultFromEndpoint('/deathsPerSpecificCountry/Greece');

    var deathsPerDay=[];
    var casesUpToNow = 0;
    var casesUpToNowGR = 0;
    var deathsUpToNow = 0;
    var deathsUpToNowGR = 0;
    for (let[key,value] of Object.entries(totalDeathsDay)){
        if (key in totalCasesDay){
            casesUpToNow += totalCasesDay[key];
        }
        if (key in totalCasesDayGR){
            casesUpToNowGR += totalCasesDayGR[key];
        }
        deathsUpToNow += value;
        if (key in totalDeathsDayGR){
            deathsUpToNowGR += totalDeathsDayGR[key];
        }

        if (casesUpToNow === 0){
            if (casesUpToNowGR === 0){
                 deathsPerDay.push({'Day':key,'CasesGlobal':0, 'CasesGR':0});
            }
            else {
                deathsPerDay.push({'Day':key,'CasesGlobal':0, 'CasesGR':(deathsUpToNowGR/casesUpToNowGR * 100).toFixed(2)});
            }
        }
        else {
            if (casesUpToNowGR === 0){
                deathsPerDay.push({'Day':key,'CasesGlobal':(deathsUpToNow/casesUpToNow * 100).toFixed(2), 'CasesGR':0});
            }
            else {
                deathsPerDay.push({'Day':key,'CasesGlobal':(deathsUpToNow/casesUpToNow * 100).toFixed(2), 'CasesGR':(deathsUpToNowGR/casesUpToNowGR * 100).toFixed(2)});
            }

        }
    }

    Morris.Line({
        element: 'death-percent-daily-global',
        data: deathsPerDay,
        xkey: 'Day',
        ykeys: ['CasesGlobal', 'CasesGR'],
        labels: ['Ποσοστό Θανάτων Παγκοσμίως', 'Ποσοστό Θανάτων στην Ελλάδα'],
        postUnits: ['%'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#d32f2f', '#3498dB']
      });

    var cdfglobal = getResultFromEndpoint('/casesCDF');
    var cdfglobaldata = [];
    for (let[key,value] of Object.entries(cdfglobal)){
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        cdfglobaldata.push({'Cases':keyVal,'CDF':value});
    }

    var cdfGR = getResultFromEndpoint('/casesCountryCDF/GREECE');
    var cdfGRdata = [];
    for (let[key,value] of Object.entries(cdfGR)){
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        cdfGRdata.push({'Cases':keyVal,'CDF':value});
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
    for (let[key,value] of Object.entries(oddsglobal)){
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        oddsglobaldata.push({'Cases':keyVal,'ODDS':Math.log10(value)});
    }

    var oddsGR = getResultFromEndpoint('/casesCountryODDS/GREECE');

    var oddsGRdata = [];
    for (let[key,value] of Object.entries(oddsGR)){
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        oddsGRdata.push({'Cases':keyVal,'ODDS':Math.log10(value)});
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
    for (let[key,value] of Object.entries(casesPerCapita)){
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        casesPerCapitaData.push({'Gdp':keyVal,'Cases':Math.log10(value+1),'LinearCases':value});
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
    for (let[key,value] of Object.entries(capitaCountry)){
        capitaCountryData.push({'Country':key,'Capita':value});
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
        for (let[key,value] of Object.entries(humanfree)){
            freedom.push({'Cases':Math.log10(value+1),'human_freedom':key});
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
        for (let[key,value] of Object.entries(humanfreeCountry)){
            freedomCountry.push({'Cases':value[0],'Country':value[1],'human_freedom':key});
        }

        Morris.Bar({
        element: 'humanfreedomCountry',
        data: freedomCountry,
        xkey: 'human_freedom',
        ykeys: ['Cases','Country'],
        labels: ['Cases','Country'],
        // parseTime: false,
        xLabelAngle: 45,
        barColors: ['#9575cd','#00838f']
      });


}();
