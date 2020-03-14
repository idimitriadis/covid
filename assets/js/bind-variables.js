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

var totalCases = getResultFromEndpoint('/totalCases');
var totalDeaths = getResultFromEndpoint('/totalDeaths');
var totalCasesPerCountry = getResultFromEndpoint('/totalCasesCountry');
var totalCasesGr = totalCasesPerCountry['Greece'];
var totalDeathsPerCountry = getResultFromEndpoint('/totalDeathsCountry');
var totalDeathsGr = totalDeathsPerCountry['Greece'];
var totalDays = getResultFromEndpoint('/totalDays');

$('#total-cases').text(totalCases);
$('#total-deaths').text(totalDeaths);
$('#total-cases-gr').text(totalCasesGr);
$('#total-deaths-gr').text(totalDeathsGr);
$('#time-frame').text('Από: ' + totalDays['first'] + '  Μέχρι: ' + totalDays['last']);
