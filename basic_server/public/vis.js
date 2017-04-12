window.onload = function () {

   var rawData;
   var chart = new CanvasJS.Chart("chartContainer");
   chart.options.title = { text: "Chart Title" };

   var xhttp = new XMLHttpRequest();
   xhttp.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200) {
         rawData = xhttp.responseText;
         //Need a bit more to fill in the dataPoints
         dpoints = [];
         rawData.forEach(function(val, i) {
            dpoints.push( { label: i, y: val} );
         });

         chart.options.data = [];
         chart.options.data[0] = { type: "line", name: "values" };
         chart.options.data[0].dataPoints = dpoints;
         chart.render();
      } else {
         console.log("Error in async call");
      }
   };
   xhttp.open("GET", "localhost:8080/api/data", true);
   xhttp.send();

   dpoints = {
      type: "line",
      name: "plotted points",
      dataPoints: [
         { label: "a", y: 7},
         { label: "b", y: 21},
         { label: "c", y: 3},
         { label: "d", y: 2},
         { label: "e", y: 10},
         { label: "f", y: 5},
         { label: "g", y: 2}
      ]
   };

   }
