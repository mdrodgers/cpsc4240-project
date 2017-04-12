window.onload = function () {

   var rawData;
   var cpuChart = new CanvasJS.Chart("cpuChartContainer");
   var diskChart = new CanvasJS.Chart("diskChartContainer");
   var memoryChart = new CanvasJS.Chart("memoryChartContainer");
   cpuChart.options.title = { text: "CPU Usage" };
   diskChart.options.title = { text: "Disk Usage" };
   memoryChart.options.title = { text: "Memory Usage" };

   var xhttp = new XMLHttpRequest();
   xhttp.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200) {
         rawData = JSON.parse(xhttp.responseText);
         //Need a bit more to fill in the dataPoints
         cpupoints = [];
         diskpoints = [];
         memorypoints = [];
         for( key in rawData ) {
            //console.log(rawData[key].time);
            cpupoints.push( { label: rawData[key].time, y: rawData[key].cpu} );
            diskpoints.push( { label: rawData[key].time, y: rawData[key].disk} );
            memorypoints.push( { label: rawData[key].time, y: rawData[key].memory} );
         }
         //console.log(cpupoints);

         cpuChart.options.data = [];
         cpuChart.options.data[0] = { type: "line", name: "values" };
         cpuChart.options.data[0].dataPoints = cpupoints;
         cpuChart.render();

         diskChart.options.data = [];
         diskChart.options.data[0] = { type: "line", name: "values" };
         diskChart.options.data[0].dataPoints = cpupoints;
         diskChart.render();

         memoryChart.options.data = [];
         memoryChart.options.data[0] = { type: "line", name: "values" };
         memoryChart.options.data[0].dataPoints = cpupoints;
         memoryChart.render();
      } else {
         console.log("Error in async call");
      }
   };
   xhttp.open("GET", "http://localhost:8080/api/data", true);
   xhttp.send();
}
