var offLine=false;
window.addEventListener("online", connectionUpdate);
window.addEventListener("offline", connectionUpdate);

function connectionUpdate(event) {
  if (navigator.onLine) {
    if (offLine) {
     
      document.getElementById("connectionStatus").innerHTML =
        "<br><span class='btn btn-outline-success' id='statusOnline'>You are back online...</span>";
      setTimeout(function () {
        $("#statusOnline").fadeOut("slow");
      }, 2000);
      offLine = !offLine;
    }
  } else {
    
    document.getElementById("connectionStatus").innerHTML =
      "<br><span class='btn btn-outline-danger'> <i class='fas fa-cloud'></i>Oops!! You are offline!You cannot make any request to the server now!</span>";
      offLine = !offLine;
  }
}




$(document).ready(function () {
  // Create DataTable
  var table = $("#filterDate");//.DataTable({});

  // Create the chart with initial data
  var container = $("<div/>").insertBefore(table);//table.table().container());

  var chart = Highcharts.chart(container[0], {
    chart: {
      type: "bar",
    },
    title: {
      text: "Amount on a particular date",
    },
    xaxis:{
         title:'Date'
    },
    yaxis:{
      title:'Amount'
    },
    series: [
      {
        data: [-1, 2, 4, -6, 0, 7,-3], //chartData(table),
      },
      {
        data: [1, 2, 3, 4, 5, 6, 7],
      },
    ],
  });





  // On each draw, update the data in the chart
  table.on("draw", function () {
    chart.series[0].setData(chartData(table));
  });
});

function chartData(table) {
  var counts = {};

  // Count the number of entries for each position
  table
    .column(2, { search: "applied" })
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

$(document).ready(function () {
  if (sessionStorage.getItem("adminPrivilege") == "true") {
    document.getElementById("admin").style.display = "block";
  }
});

function logout() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/logout/",
    success: function (data) {
      sessionStorage.removeItem("name");
      sessionStorage.removeItem("adminPrivilege");
      sessionStorage.removeItem("auth", "");
      window.location.href = "login.html";
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
}



$(document).ready(function () {
  var token = "Token ";
  var token1 = sessionStorage.getItem("auth");
  var authorization = token.concat(token1);
  if (sessionStorage.getItem("auth") === null) {
    window.location.href = "login.html";
  }




  
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/transactions/",
    headers: { Authorization: authorization },
    success: function (data) {
      $("#transactionsTable").dataTable().fnDestroy();
      

      var buttonCommon = {
        exportOptions: {
          format: {
            body: function (data, row, column, node) {
              // Strip $ from amount column to make it numeric
              return column === 5 ? data.replace(/[$,]/g, "") : data;
            },
          },
        },
      };

      var table = $("#transactionsTable").DataTable({
        orderCellsTop: true,
        fixedHeader: false,
        data:data,
        columns: [
          { data: "accountId"},
          { data: "accountName"},
          { data: "amount"},
          { data: "accountType"},
          { data: "date"},
        ],
        columnDefs: [
          { width: '60%', targets: 0 },
          { width: '100%', targets: 2 },
          { width: '100%', targets: 3 },
          { width: '100%', targets: 4 }
      ],
      dom: "<Bfrl<t>ip>",
      buttons: [
         'copy','pdf','excel','csv','print'
      ],
       initComplete: function () {
        var count = 0;
        this.api().columns().every( function () {
            var title = this.header();
            //replace spaces with dashes
            title = $(title).html().replace(/[\W]/g, '-');
            var column = this;
            var select = $('<select id="' + title + '" class="select2" ></select>')
                .appendTo( $(column.footer()).empty() )
                .on( 'change', function () {
                  //Get the "text" property from each selected data 
                  //regex escape the value and store in array
                  var data1 = $.map( $(this).select2('data'), function( value, key ) {
                    return value.text ? '^' + $.fn.dataTable.util.escapeRegex(value.text) + '$' : null;
                             });
                  
                  //if no data selected use ""
                  if (data1.length === 0) {
                    data1= [""];
                  }
                  
                  //join array into string with regex or (|)
                  var val = data1.join('|');
                  
                  //search for the option(s) selected
                  column
                        .search( val ? val : '', true, false )
                        .draw();
                } );

            column.data().unique().sort().each( function ( d, j ) {
                select.append( '<option value="'+d+'">'+d+'</option>' );
            } );
          
          //use column title as selector and placeholder
          $('#' + title).select2({
            multiple: true,
            closeOnSelect: false,
            placeholder: "Select " + title,
            width: '100%'
          });
          
          //initially clear select otherwise first option is selected
          $('.select2').val(null).trigger('change');
        } );
    },
    
    
    footerCallback: function ( row, data, start, end, display ) {
      var api = this.api(), data;

      // Remove the formatting to get integer data for summation
      var intVal = function ( i ) {
          return typeof i === 'string' ?
              i.replace(/[\$,]/g, '')*1 :
              typeof i === 'number' ?
                  i : 0;
      };

      // Total over all pages
      var total = api
          .cells( function ( index, data, node ) {
              return api.row( index ).data().accountType === 'Credit' ?
                  true : false;
          }, 0 )
          .data(2,{filter:'applied'})
          .reduce( function (a, b) {
              return parseFloat(a) + parseFloat(b);
          }, 0 );


          var dtotal = api
          .cells( function ( index, data, node ) {
              return api.row( index ).data().accountType === 'Debit' ?
                  true : false;
          }, 2,{filter:'applied'} )
          .data(2,{filter:'applied'})
          .reduce( function (a, b) {
              return parseFloat(a) + parseFloat(b);
          }, 0 );


          var cr = 0;
          var dr = 0;

          var data1=data;
      var data2 =api.rows( { search:'applied' } ).data().each(function(value, index) {
        //console.log(value, index);
        if(value['accountType']==='Credit'){
          cr+=parseFloat(value['amount']);
        }else{
          dr+=parseFloat(value['amount']);
        }
    });
    //console.log(dr);
       //console.log(cr);
      



      // Total over this page
      var pageTotal = api
          .column( 2,{filter:'applied'} )
          .data()
          .reduce( function (a, b) {
           
              return parseFloat(a) + parseFloat(b);
          }, 0 );


      // Update footer
      $( api.column( 2 ).footer() ).html(
          '$'+pageTotal.toFixed(2) +' ( $'+ cr.toFixed(2) +' Cr)'+' ( $'+ dr.toFixed(2) +' Dr)'
      );
  }
         
      });
    
     
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
});


$('.input-daterange input').each(function() {
  $(this).datepicker('clearDates');
});

// Extend dataTables search
$.fn.dataTable.ext.search.push(
  function(settings, data, dataIndex) {
    var min = $('#min').val();
    var max = $('#max').val();
    var createdAt = data[4] || 4; // Our date column in the table

    if((min == "" || max == "") ||(moment(createdAt).isSameOrAfter(min) && moment(createdAt).isSameOrBefore(max)))
     {
    return true;
}

    return false;
  }
);


$(document).ready(function () {
  $('.date-range-filter').change(function() {
    //console.log("True");
      var table = $('#transactionsTable').DataTable();
    table.draw();
  });

 
 

  document.getElementById("min").value="";
  document.getElementById("max").value="";
  
  $('#data-table_filter').hide();
  
  });



/* Custom filtering function which will search data in column four between two values */
$.fn.dataTable.ext.search.push(
	function( settings, data, dataIndex ) {
		var min = parseFloat( $('#mina').val(), 10 );
		var max = parseFloat( $('#maxa').val(), 10 );
		var amt = parseFloat( data[2] ) || 0; // use data for the amt column

		if ( ( isNaN( min ) && isNaN( max ) ) ||
			 ( isNaN( min ) && amt <= max ) ||
			 ( min <= amt   && isNaN( max ) ) ||
			 ( min <= amt   && amt <= max ) )
		{
			return true;
		}
		return false;
	}
);

//const log = document.getElementById('mina');

document.addEventListener('keyup', redraw);


function redraw(e){
  var table = $('#transactionsTable').DataTable();
      table.draw();

}


/*                  AMOUNT FILTERS AND CLEARING             */


  function clearAmount(){
    document.getElementById("mina").value="";
    document.getElementById("maxa").value="";
    var table = $('#transactionsTable').DataTable();
    table.draw();
  }


  function clearDates(){
    document.getElementById("min").value="";
    document.getElementById("max").value="";
    var table = $('#transactionsTable').DataTable();
    table.draw();
  }

