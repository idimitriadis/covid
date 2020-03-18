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

var totalCases = parseInt(getResultFromEndpoint('/totalCases'));
var totalDeaths = parseInt(getResultFromEndpoint('/totalDeaths'));
var totalCasesPerCountry = getResultFromEndpoint('/totalCasesCountry');
var totalCasesGr = totalCasesPerCountry['GREECE'];
var totalDeathsPerCountry = getResultFromEndpoint('/totalDeathsCountry');
var totalDeathsGr = totalDeathsPerCountry['GREECE'];
var totalDays = getResultFromEndpoint('/totalDays');

var casesEU = getResultFromEndpoint('/casesEU');
var casesNonEU = getResultFromEndpoint('/casesnonEU');
var deathsEU = getResultFromEndpoint('/deathsEU');
var deathsNonEU = getResultFromEndpoint('/deathsnonEU');
var casesTodayEU = getResultFromEndpoint('/cases_todayEU');
var casesTodayNonEU = getResultFromEndpoint('/cases_today_nonEU');
var casesTodayGlobal = getResultFromEndpoint('/cases_today_global');
var deathsTodayEU = getResultFromEndpoint('/deaths_today_EU');
var deathsTodayNonEU = getResultFromEndpoint('/deaths_today_nonEU');
var deaths_today_global = getResultFromEndpoint('/deaths_today_global');
var recovered_greece = getResultFromEndpoint('/recovered_greece');

$('#recovered_greece').text(recovered_greece);
$('#cases-EU').text(casesEU);
$('#cases-Non-EU').text(casesNonEU);
$('#deaths-EU').text(deathsEU);
$('#deaths-Non-EU').text(deathsNonEU);
$('#casesTodayEU').text(casesTodayEU);
$('#casesTodayNonEU').text(casesTodayNonEU);
$('#casesTodayGlobal').text(casesTodayGlobal);
$('#deathsTodayEU').text(deathsTodayEU);
$('#deathsTodayNonEU').text(deathsTodayNonEU);
$('#deathsTodayGlobal').text(deaths_today_global);
$('#total-cases').text(totalCases);
$('#total-deaths').text(totalDeaths);
$('#total-cases-gr').text(totalCasesGr);
$('#total-deaths-gr').text(totalDeathsGr);
$('#time-frame').text('Από: ' + totalDays['first'] + '  Μέχρι: ' + totalDays['last']);

var countryData = getResultFromEndpoint('/getCountries');

var select1 = document.getElementById("selectField1");
var select2 = document.getElementById("selectField2");

// create option for all countries together
var el = document.createElement("option");
el.textContent = 'WORLD';
el.value = 'WORLD';
el.setAttribute('selected','selected');
var el2 = el.cloneNode(true);
select1.appendChild(el);
select2.appendChild(el2);

// for the second graph of death ratios
var select3 = document.getElementById("selectFieldDeath1");
var select4 = document.getElementById("selectFieldDeath2");
var el3 = el.cloneNode(true);
var el4 = el.cloneNode(true);
select3.appendChild(el3);
select4.appendChild(el4);

// append other options from country list
for (var i = 0; i < countryData.length; i++) {
    var opt = countryData[i];
    el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    el2 = el.cloneNode(true);
    select1.appendChild(el);
    select2.appendChild(el2);

    // for the second graph of death ratios
    el3 = el.cloneNode(true);
    el4 = el.cloneNode(true);
    select3.appendChild(el3);
    select4.appendChild(el4);
}



