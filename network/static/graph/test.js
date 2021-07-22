    const ROOT_PATH = location.protocol + '//' + location.host
    console.log(ROOT_PATH)
    $.ajax({
        url: ROOT_PATH+'/api/v1',
        type:"GET",
        data:{

        },
        dataType:'json',
        success:function(data){
        am4core.useTheme(am4themes_animated);
        // Themes end
        console.log(data)
        var chart = am4core.create("chartdiv", am4plugins_forceDirected.ForceDirectedTree);

        var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())
        networkSeries.dataFields.linkWith = "linkWith";
        networkSeries.dataFields.name = "name";
        networkSeries.dataFields.id = "name";
        networkSeries.dataFields.value = "value";
        networkSeries.dataFields.children = "children";
        networkSeries.dataFields.color = "color"
        networkSeries.maxLevels =1
        networkSeries.nodes.template.label.text = "{name}"
        networkSeries.fontSize = 15;
        networkSeries.linkWithStrength = 0;

        networkSeries.minRadius = 20;
        networkSeries.maxRadius = 50;


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
        nodeTemplate.events.on("over", function (event) {
            var dataItem = event.target.dataItem;
            dataItem.childLinks.each(function (link) {
                link.isHover = true;
            })
        })

        nodeTemplate.events.on("out", function (event) {
            var dataItem = event.target.dataItem;
            dataItem.childLinks.each(function (link) {
                link.isHover = false;
            })
        })

        }

    })

    function local(){
        var company = $('#company').val()
        var industrial = $('#industrial').val()
        var phase = $('#phase').val()
        var capital = $('#capital').val()

        $.ajax({
        url: ROOT_PATH+'/api/v1/',
        type:"POST",
        data:{
            "company": company,
            "industrial": industrial,
            "phase": phase,
            "capital": capital
        },
        dataType:'json',
        success:function(data){
            am4core.useTheme(am4themes_animated);
        // Themes end
        var chart = am4core.create("chartdiv", am4plugins_forceDirected.ForceDirectedTree);

        var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())
        networkSeries.dataFields.linkWith = "link";
        networkSeries.dataFields.name = "name";
        networkSeries.dataFields.id = "id";
        networkSeries.dataFields.value = "value";
        networkSeries.dataFields.children = "children";
        networkSeries.dataFields.color = "color"
        networkSeries.maxLevels =1
        networkSeries.nodes.template.label.text = "{name}"
        networkSeries.fontSize = 15;
        networkSeries.linkWithStrength = 0;

        networkSeries.minRadius = 20;
        networkSeries.maxRadius = 40;

        networkSeries.centerStrength = 2;
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
  console.log(event.target.dataItem)
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




        },
        error: function(data){
            alert("검색결과가 없습니다.")
        }
        })
    }


