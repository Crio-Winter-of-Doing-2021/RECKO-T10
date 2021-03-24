$(document).ready(function () {
   if(localStorage.getItem('adminPrivilege')=="true"){
     document.getElementById("admin").style.display="block";
   }

   /*
   $('#transactionsTable thead th').each( function () {
    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
} );

// DataTable
var table = $('#transactionsTable').DataTable({
  initComplete: function () {
      // Apply the search
      this.api().columns().every( function () {
          var that = this;

          $( 'input', this.header() ).on( 'keyup change clear', function () {
              if ( that.search() !== this.value ) {
                  that
                      .search( this.value )
                      .draw();
              }
          } );
      } );
  }
});
*/

});


function logout(){
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/logout/",
    success: function (data) {
      localStorage.removeItem('name');
      localStorage.removeItem('adminPrivilege');
      localStorage.removeItem('auth','');
      window.location.href="login.html";
 
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
}



function loadMemes() {
  var token="Token ";
  var token1=localStorage.getItem('auth');
  var authorization=token.concat(token1);
    $.ajax({
      type: "GET",
      url: "http://127.0.0.1:8000/transactions/",
      headers: {"Authorization": authorization},
      success: function (data) {
        
        $("#transactionsTable").dataTable().fnDestroy();
        $('#transactionsTable thead tr').clone(true).appendTo( '#transactionsTable thead' );
  $('#transactionsTable thead tr:eq(1) th').each( function (i) {
      var title = $(this).text();
      $(this).html( '<input type="text" placeholder="Search '+title+'" />' );

      $( 'input', this ).on( 'keyup change', function () {
          if ( table.column(i).search() !== this.value ) {
              table
                  .column(i)
                  .search( this.value )
                  .draw();
          }
      } );
  } );
 
  var table = $('#transactionsTable').DataTable({
          orderCellsTop: true,
          fixedHeader: false,
            data: data,  // Get the data object
            columns: [
                { data: 'accountId' },
                { data: 'accountName' },
                { data: 'amount' },
                { data: 'accountType' },
                { data: 'date' },
            ]});
   
      },
      error: function (response) {
        alert(response["statusText"]);
      },
    });

  }
  

  $(document).ready(function () {
    $("#filterByDateForm").submit(function (event) {
      /* stop form from submitting normally */
      event.preventDefault();
      var start = $("input[name=startdate]").val();
      var end = $("input[name=enddate]").val();
     console.log(start+" "+end);
      if (start > end) {
        alert("End date cannot be before start date");
        document.getElementsByName("filterByDateForm")[0].reset();
      } else {
        
        document.getElementsByName("filterByDateForm")[0].reset();
        fetch(
          "http://127.0.0.1:8000/filterByDate/",
          {
            method: "POST",
            body: JSON.stringify({
              startDate: start,
              endDate: end,
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8",
            },
          }
        )
          .then(function (response) {
            console.log(response);
            if (!response.ok) {
              alert(response.statusText);
              return {};
            }
            return response.json();
          })
          .then(function (responseData) {
            if (responseData.length == 0) {
              console.log("Bad response from server.");
            } else {
                $("#transactionsTable").dataTable().fnDestroy();
                $('#transactionsTable').DataTable({
                    data: responseData,  // Get the data object
                    columns: [
                        { data: 'accountId' },
                        { data: 'accountName' },
                        { data: 'amount' },
                        { data: 'accountType' },
                        { data: 'date' },
                    ]});
            }
          });
      }
    });
  });






  $(document).ready(function () {
    $("#filterByNameForm").submit(function (event) {
      /* stop form from submitting normally */
      event.preventDefault();
      var accname = $("input[name=namefilter]").val();
  
      console.log(accname);
  
      //document.getElementById("alltransactions").innerHTML = "";
      document.getElementsByName("filterByNameForm")[0].reset();
  
      var formData = $(this).serialize();
      fetch("http://127.0.0.1:8000/filterByAccName/", {
        method: "POST",
        body: JSON.stringify({
          accountName: accname,
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      })
        .then(function (response) {
          console.log(response);
          if (!response.ok) {
            alert("Account name not found!!");
            console.log(response.statusText);
            return {};
          }
          return response.json();
        })
        .then(function (responseData) {
          if (responseData.length == 0) {
            console.log("Bad response from server.");
          } else {
            $("#transactionsTable").dataTable().fnDestroy();
            $('#transactionsTable').DataTable({
                data: responseData,  // Get the data object
                columns: [
                    { data: 'accountId' },
                    { data: 'accountName' },
                    { data: 'amount' },
                    { data: 'accountType' },
                    { data: 'date' },
                ]});
    
            }
        });
    });
  });




  $(document).ready(function () {
    $("#filterByTypeForm").submit(function (event) {
      /* stop form from submitting normally */
      event.preventDefault();
      const rbs=document.querySelectorAll('input[name="type"]');
      let transactiontype;
      for (const rb of rbs) {
          if (rb.checked) {
              transactiontype = rb.value;
              break;
          }
      }
      console.log(transactiontype);
  
      //document.getElementById("alltransactions").innerHTML = "";
      document.getElementsByName("filterByNameForm")[0].reset();
  
      var formData = $(this).serialize();
      fetch("http://127.0.0.1:8000/filterByType/", {
        method: "POST",
        body: JSON.stringify({
          type: transactiontype,
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      })
        .then(function (response) {
          console.log(response);
          if (!response.ok) {
            alert("Transaction type not found!!");
            console.log(response.statusText);
            return {};
          }
          return response.json();
        })
        .then(function (responseData) {
          if (responseData.length == 0) {
            console.log("Bad response from server.");
          } else {
            $("#transactionsTable").dataTable().fnDestroy();
            $('#transactionsTable thead tr:eq(1) th').each( function (i) {
              var title = $(this).text();
              $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
        
              $( 'input', this ).on( 'keyup change', function () {
                  if ( table.column(i).search() !== this.value ) {
                      table
                          .column(i)
                          .search( this.value )
                          .draw();
                  }
              } );
          } );
            $('#transactionsTable').DataTable({
                data: responseData,  // Get the data object
                columns: [
                    { data: 'accountId' },
                    { data: 'accountName' },
                    { data: 'amount' },
                    { data: 'accountType' },
                    { data: 'date' },
                ]});

              
            
            
            }
        });
    });
  });


/*   CHART FUNCTIONS  

Highcharts.getJSON('https://demo-live-data.highcharts.com/aapl-c.json', function (data) {
    // Create the chart
    Highcharts.chart('container', {
      chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          type: 'pie'
      },
      title: {
          text: 'Browser market shares in January, 2018'
      },
      tooltip: {
          pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      accessibility: {
          point: {
              valueSuffix: '%'
          }
      },
      plotOptions: {
          pie: {
              allowPointSelect: true,
              cursor: 'pointer',
              dataLabels: {
                  enabled: true,
                  format: '<b>{point.name}</b>: {point.percentage:.1f} %'
              }
          }
      },
      series: [{
          name: 'Brands',
          colorByPoint: true,
          data: [{
              name: 'Chrome',
              y: 61.41,
              sliced: true,
              selected: true
          }, {
              name: 'Internet Explorer',
              y: 11.84
          }, {
              name: 'Firefox',
              y: 10.85
          }, {
              name: 'Edge',
              y: 4.67
          }, {
              name: 'Safari',
              y: 4.18
          }, {
              name: 'Sogou Explorer',
              y: 1.64
          }, {
              name: 'Opera',
              y: 1.6
          }, {
              name: 'QQ',
              y: 1.2
          }, {
              name: 'Other',
              y: 2.61
          }]
      }]
  });
});
*/

/*
$(document).ready(function () {
  // Create DataTable
  var table = $('#transactionsTable').DataTable({
      dom: 'Pfrtip',
  });

  // Create the chart with initial data
  var container = $('<div/>').insertBefore(table.table().container());

  var chart = Highcharts.chart(container[0], {
      chart: {
          type: 'pie',
      },
      title: {
          text: 'Transactions Per Account Name',
      },
      series: [
          {
              data: chartData(table),
          },
      ],
  });

  // On each draw, update the data in the chart
  table.on('draw', function () {
      chart.series[0].setData(chartData(table));
  });
});

function chartData(table) {
  var counts = {};

  // Count the number of entries for each position
  table
      .column(1, { search: 'applied' })
      .data()
      .each(function (val) {
          if (counts[val]) {
              counts[val] += 1;
          } else {
              counts[val] = 1;
          }
      });

  // And map it to the format highcharts uses
  return $.map(counts, function (val, key) {
      return {
          name: key,
          y: val,
      };
  });
}
*/