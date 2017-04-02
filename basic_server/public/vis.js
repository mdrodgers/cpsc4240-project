/*d3.select("body")
.append("svg")
.attr("width", 50)
.attr("height", 50)
.append("circle")
.attr("cx", 25)
.attr("cy", 25)
.attr("r", 25)
.style("fill", "purple");*/

/*
d3.select(".chart")
   .selectAll("div")
      .data([1, 3, 7, 2, 5])
   .enter().append("div")
      .style('width', function(d) { return d * 10 + 'px'; })
      .text(function(d) { return d; });
*/

var data = [1, 3, 7, 2, 5];

var svg = d3.select('body').append('svg')
   .attr('height', '100%')
   .attr('width', '100%');

svg.selectAll('rect')
   .data(data)
   .enter().append('rect')
      .attr('class', 'bar')
      .attr('height', function(d, i) { return (d * 10); })
      .attr('width', '40')
      .attr('x', function(d, i) { return (i * 60) + 25; })
      .attr('y', function(d, i) { return 400 - (d * 10); });
