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
        labels: ['CasesGlobal', 'CasesGreece'],
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
        labels: ['CasesGlobal', 'CasesGR'],
        postUnits: ['%'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#d32f2f', '#3498dB']
      });


    var casesPerCapita = getResultFromEndpoint('/casesPerCapita');
    var casesPerCapitaData = [];
    for (let[key,value] of Object.entries(casesPerCapita)){
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        casesPerCapitaData.push({'Gdp':keyVal,'Cases':value});
    }

    Morris.Bar({
        element: 'cases-per-capita',
        data: casesPerCapitaData,
        xkey: 'Gdp',
        ykeys: ['Cases'],
        labels: ['Cases'],
        // parseTime: false,
        xLabelAngle: 90,
        barColors: ['#d32f2f']
      });

    var casesPerLife = getResultFromEndpoint('/casesPerLifeExpectancy');
    var casesPerLifeData = [];
    for (let[key,value] of Object.entries(casesPerLife)){
        var keyVal = parseFloat(key);
        keyVal = keyVal.toFixed(2);
        casesPerLifeData.push({'Life':keyVal,'Cases':value});
    }

    Morris.Bar({
        element: 'cases-per-life-expectancy',
        data: casesPerLifeData,
        xkey: 'Life',
        ykeys: ['Cases'],
        labels: ['Cases'],
        // parseTime: false,
        xLabelAngle: 90,
        barColors: ['#d32f2f']
      });

    $('.code-example').each(function (index, el) {
      eval($(el).text());
    });

}();
