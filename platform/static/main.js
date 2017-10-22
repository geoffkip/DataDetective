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
          title: {
              text: 'Rainfall (mm)'
          }
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
var newGeoChart = function(id, title) {
  var data = [
      ['us-pa-015', 0],
      ['us-pa-117', 1],
      ['us-pa-027', 2],
      ['us-pa-035', 3],
      ['us-pa-061', 4],
      ['us-pa-009', 5],
      ['us-pa-075', 6],
      ['us-pa-029', 7],
      ['us-pa-011', 8],
      ['us-pa-083', 9],
      ['us-pa-047', 10],
      ['us-pa-005', 11],
      ['us-pa-019', 12],
      ['us-pa-007', 13],
      ['us-pa-067', 14],
      ['us-pa-099', 15],
      ['us-pa-053', 16],
      ['us-pa-123', 17],
      ['us-pa-121', 18],
      ['us-pa-033', 19],
      ['us-pa-063', 20],
      ['us-pa-107', 21],
      ['us-pa-079', 22],
      ['us-pa-055', 23],
      ['us-pa-001', 24],
      ['us-pa-089', 25],
      ['us-pa-069', 26],
      ['us-pa-093', 27],
      ['us-pa-081', 28],
      ['us-pa-095', 29],
      ['us-pa-025', 30],
      ['us-pa-065', 31],
      ['us-pa-003', 32],
      ['us-pa-129', 33],
      ['us-pa-021', 34],
      ['us-pa-013', 35],
      ['us-pa-039', 36],
      ['us-pa-023', 37],
      ['us-pa-097', 38],
      ['us-pa-043', 39],
      ['us-pa-077', 40],
      ['us-pa-091', 41],
      ['us-pa-131', 42],
      ['us-pa-113', 43],
      ['us-pa-037', 44],
      ['us-pa-045', 45],
      ['us-pa-119', 46],
      ['us-pa-087', 47],
      ['us-pa-031', 48],
      ['us-pa-085', 49],
      ['us-pa-071', 50],
      ['us-pa-049', 51],
      ['us-pa-041', 52],
      ['us-pa-127', 53],
      ['us-pa-017', 54],
      ['us-pa-059', 55],
      ['us-pa-051', 56],
      ['us-pa-101', 57],
      ['us-pa-103', 58],
      ['us-pa-115', 59],
      ['us-pa-125', 60],
      ['us-pa-105', 61],
      ['us-pa-109', 62],
      ['us-pa-111', 63],
      ['us-pa-057', 64],
      ['us-pa-073', 65],
      ['us-pa-133', 66]
  ];
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

      series: [{
          data: data,
          name: 'Random data',
          states: {
              hover: {
                  color: '#BADA55'
              }
          },
          dataLabels: {
              enabled: true,
              format: '{point.name}'
          }
      }]
  });
}
