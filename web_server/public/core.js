window.onload = function () {

   var rawData;
   var chart = new CanvasJS.Chart("chartContainer");
   chart.options.title = { text: "CPU usage" };

   var xhttp = new XMLHttpRequest();
   xhttp.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200) {
         rawData = JSON.parse(xhttp.responseText);
         //Need a bit more to fill in the dataPoints
         dpoints = [];
         for( key in rawData ) {
            //console.log(rawData[key].time);
            dpoints.push( { label: rawData[key].time, y: rawData[key].cpu} );
         }
         //console.log(dpoints);

         chart.options.data = [];
         chart.options.data[0] = { type: "line", name: "values" };
         chart.options.data[0].dataPoints = dpoints;
         chart.render();
      } else {
         console.log("Error in async call");
      }
   };
   xhttp.open("GET", "http://localhost:8080/api/data", true);
   xhttp.send();

/*
   dpoints = [
         { label: "a", y: 7},
         { label: "b", y: 21},
         { label: "c", y: 3},
         { label: "d", y: 2},
         { label: "e", y: 10},
         { label: "f", y: 5},
         { label: "g", y: 2}
   ];

   chart.options.data = [];
   chart.options.data[0] = { type: "line", name: "values" };
   chart.options.data[0].dataPoints = dpoints;
   chart.render();
*/

}
