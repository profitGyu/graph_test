async function MakeStartupNetworkChart(data){

        var chart = am4core.create("networkGraph", am4plugins_forceDirected.ForceDirectedTree);

        var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())
        networkSeries.dataFields.linkWith = "link";
        networkSeries.dataFields.name = "name";
        networkSeries.dataFields.id = "id";
        networkSeries.dataFields.value = "value";
        networkSeries.dataFields.children = "children";
        networkSeries.dataFields.color = "color"
        networkSeries.maxLevels =1
        networkSeries.nodes.template.label.text = "{name}"
        networkSeries.fontSize = 10;
        networkSeries.linkWithStrength = 0;

        networkSeries.nodes.template.label.verticalCenter = "bottom";
        networkSeries.nodes.template.label.dy = -15;
        networkSeries.nodes.template.label.fill = am4core.color("#000");

        networkSeries.minRadius = 10;
        networkSeries.maxRadius = 20;

        networkSeries.centerStrength = 1;
        var nodeTemplate = networkSeries.nodes.template;
        nodeTemplate.tooltipText = "{name}";
        nodeTemplate.fillOpacity = 1;
        nodeTemplate.label.hideOversized = true;
        nodeTemplate.label.truncate = true;


<!--        chart.legend = new am4charts.Legend();-->


        var linkTemplate = networkSeries.links.template;
        linkTemplate.strokeWidth = 1;
        var linkHoverState = linkTemplate.states.create("hover");
        linkHoverState.properties.strokeOpacity = 1;
        linkHoverState.properties.strokeWidth = 2;
        networkSeries.data =data
        networkSeries.dragFixedNodes = true;
        networkSeries.nodes.template.events.on("dragstop", function(event) {
          event.target.dataItem.fixed = true;
        })

        networkSeries.nodes.template.events.on("down", function(event) {
          event.target.dataItem.fixed = false;
        })
        // end of disabling physics

        networkSeries.nodes.template.events.on("over", function(event) {

          event.target.dataItem.childLinks.each(function(link) {
            link.isHover = true;
          })
            if (event.target.dataItem.linkWith){
            event.target.dataItem.linkWith.isHover =true;
          }
          if (event.target.dataItem.parentLink) {
            event.target.dataItem.parentLink.isHover = true;
          }

        })

        networkSeries.nodes.template.events.on("out", function(event) {
          event.target.dataItem.childLinks.each(function(link) {
            link.isHover = false;
          })
          if (event.target.dataItem.parentLink) {
            event.target.dataItem.parentLink.isHover = false;
          }
        })

       }