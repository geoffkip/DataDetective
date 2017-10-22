var charts = {}; // A list of charts on the page

$(document).ready(function() {
  // SETUP SELECTIONS
  $('#months-select').select2();
  $('#years-select').select2();
  $('#measures-select').select2();

  console.log("Getting measures")
  getMeasures(function(measures){
    console.log(measures)
    for(var i = 0; i < measures.length; i++) {
      let option = new Option(titleCaseMeasure(measures[i]), measures[i]);
      $("#measures-select").append(option);
    }
  })

  $("#measures-select")
    .on('change', function (e) {
      var measures = $('#measures-select').select2('data');
      var year = $('#years-select').select2('data')[0].id;
      var month = $('#months-select').select2('data')[0].id;

      drawCharts(measures, year, month)

      // Step 2: Update the recommendations
      measures = measures.map(function(m){return m.id})
      getRecommendations(measures, function(recommendations){
        $("#recommendations").empty();
        for(var i = 0; i < recommendations.length; i++) {
          $("#recommendations").append('<span onClick="updateMeasures(this.id)" id="' +
                                       recommendations[i] +
                                       '"class="badge badge-primary">' +
                                       titleCaseMeasure(recommendations[i]) +
                                       '</span>&nbsp;')
        }
      })

    })
});

var getMeasures = function(callback) {
  console.log("Getting measures")
  $.ajax({
      url: '/measures/list',
      type: 'GET',
      success: function(response) {
          return callback(response)
      },
      error: function(error) {
          console.log(error);
      }
  });
}

var updateMeasures = function(measure) {
  var selectedValues = $("#measures-select").val()
  selectedValues.push(measure)
  $("#measures-select").val(selectedValues).trigger("change")
}

var titleCaseMeasure = function(str) {
  str = str.toLowerCase().split('_');

  for(var i = 0; i < str.length; i++){
    str[i] = str[i].split('');
    str[i][0] = str[i][0].toUpperCase();
    str[i] = str[i].join('');
  }
  return str.join(' ');
}

var getSeries = function(measure, year, month, callback) {
  console.log("In getSeries", measure, year, month)
  $.ajax({
      url: '/measures/'+measure,
      data: {
        year: year,
        month: month
      },
      type: 'POST',
      success: function(response) {
          return callback(response)
      },
      error: function(error) {
          console.log(error);
      }
  });
}

var getGeoSeries = function(measure, year, month, callback) {
  console.log("In getSeries", measure, year, month)
  $.ajax({
      url: '/measures/'+measure+'/geo',
      data: {
        year: year,
        month: month
      },
      type: 'POST',
      success: function(response) {
          console.log("SERIES:", response)
          return callback(response)
      },
      error: function(error) {
          console.log(error);
      }
  });
}

var getTimeSeries = function(measure, year, month, callback) {
  console.log("In getSeries", measure, year, month)
  $.ajax({
      url: '/measures/'+measure+'/timeseries',
      data: {
        year: year,
        month: month
      },
      type: 'POST',
      success: function(response) {
          return callback(response)
      },
      error: function(error) {
          console.log(error);
      }
  });
}


var getRecommendations = function(measures, callback) {
  console.log("In getSeries", measures)
  if(measures.length > 0) {
    $.ajax({
        url: '/measures/recommend',
        data: {
          measures: JSON.stringify(measures.join(','))
        },
        type: 'POST',
        success: function(response) {
            return callback(response)
        },
        error: function(error) {
            console.log(error);
            callback([])
        }
    });
  } else {
    callback([])
  }
}

var newBarChart = function(id, title, series) {
  console.log("Make barchart", id, title, series)

  var barChart = Highcharts.chart(id, {
      chart: {
          type: 'column'
      },
      title: {
          text: title
      },
      xAxis: {
        type: "category"
      },
      yAxis: {
          min: 0,
          title: null
      },
      tooltip: {
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
              '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
          footerFormat: '</table>',
          shared: true,
          useHTML: true
      },
      plotOptions: {
          column: {
              pointPadding: 0.2,
              borderWidth: 0
          }
      },
      series: [series]
  });
}


// Create the chart
var newGeoChart = function(id, title, series) {
  var geochart = Highcharts.mapChart(id, {
      chart: {
          map: 'countries/us/us-pa-all'
      },
      title: {
          text: null
      },
      subtitle: {
          text: title
      },

      mapNavigation: {
          enabled: false,
          buttonOptions: {
              verticalAlign: 'bottom'
          }
      },

      colorAxis: {
          min: 0
      },

      series: [series]
  });
}
