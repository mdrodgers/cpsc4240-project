/*window.onload = function() {
   var chart = new CanvasJS.Chart("chartContainer", {
      title:{
         text:"Chart Title"
      },
      data:[
         {
            type: "column",
            dataPoints: [
               { label: "a", y: 10}
               { label: "b", y: 12}
               { label: "c", y: 5}
               { label: "d", y: 20}
               { label: "e", y: 23}
            ]
         }
      ]
   });
   chart.render();
}*/

window.onload = function () {

   var chart = new CanvasJS.Chart("chartContainer", {
      title:{
         text: "My First Chart in CanvasJS"              
      },
      data: [              
      {
         // Change type to "doughnut", "line", "splineArea", etc.
         type: "column",
         dataPoints: [
            { label: "apple",  y: 10  },
            { label: "orange", y: 15  },
            { label: "banana", y: 25  },
            { label: "mango",  y: 30  },
            { label: "grape",  y: 28  }
         ]
      }
      ]
   });
   chart.render();
}
