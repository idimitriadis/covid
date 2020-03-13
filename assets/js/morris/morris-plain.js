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
                console.log(data);
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
    var datas=[];
    for (let[key,value] of Object.entries(totalCasesDay)){
      datas.push({'Day':key,'Cases':value});}

    $(function () {

      Morris.Line({
        element: 'hero-graph',
        data: datas,
        xkey: 'Day',
        ykeys: ['Cases'],
        labels: ['Cases'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#d32f2f']
      });

      
    });

    var totalCasesDayGR = getResultFromEndpoint('/casesPerSpecificCountry/Greece');
    var dataGR=[];
    for (let[key,value] of Object.entries(totalCasesDayGR)){
      dataGR.push({'Day':key,'Cases':value});}

    Morris.Line({
        element: 'sentiment-graph',
        data: dataGR,
        xkey: 'Day',
        ykeys: ['Cases'],
        labels: ['Cases'],
        parseTime: false,
        xLabelAngle: 90,
        lineColors: ['#d32f2f']
      });

    $('.code-example').each(function (index, el) {
      eval($(el).text());
    });

}();
