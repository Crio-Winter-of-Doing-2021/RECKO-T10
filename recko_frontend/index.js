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
      "<br><span class='btn btn-outline-danger'> <i class='fas fa-cloud'></i>Oops!! You are offline!</span>";
      offLine = !offLine;
  }
}

$(document).ready(function () {
  // Create DataTable
  var table = $("#transactionsTable").DataTable({});

  // Create the chart with initial data
  var container = $("<div/>").insertBefore(table.table().container());

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
        data: [-1, 2, 4, -6, 0, 7], //chartData(table),
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
  if (localStorage.getItem("adminPrivilege") == "true") {
    document.getElementById("admin").style.display = "block";
  }
});

function logout() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/logout/",
    success: function (data) {
      localStorage.removeItem("name");
      localStorage.removeItem("adminPrivilege");
      localStorage.removeItem("auth", "");
      window.location.href = "login.html";
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
}

function loadMemes() {
  var token = "Token ";
  var token1 = localStorage.getItem("auth");
  var authorization = token.concat(token1);
  if (localStorage.getItem("auth") === null) {
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
        data: data, // Get the data object
        columns: [
          { data: "accountId" },
          { data: "accountName" },
          { data: "amount" },
          { data: "accountType" },
          { data: "date" },
        ],
        dom: "<BfPl<t>ip>",
        buttons: [
          $.extend(true, {}, buttonCommon, {
            extend: "copyHtml5",
          }),
          $.extend(true, {}, buttonCommon, {
            extend: "excelHtml5",
          }),
          $.extend(true, {}, buttonCommon, {
            extend: "pdfHtml5",
          }),
          $.extend(true, {}, buttonCommon, {
            extend: "csvHtml5",
          }),
        ],
      });
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
}
