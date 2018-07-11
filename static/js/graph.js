d3.queue()
    .defer(d3.json, "http://127.0.0.1:5000/get_recipes")
    .await(makeGraphs);


function makeGraphs(error, recipeData) {
    var ndx = crossfilter(recipeData);

    show_category_selector(ndx);
    show_category_graph(ndx);

    dc.renderAll();
}


function show_category_selector(ndx) {
    var categorySelectorDim = ndx.dimension(dc.pluck("category"));
    var categorySelectorSelect = categorySelectorDim.group();

    dc.selectMenu("#category-selector")
        .dimension(categorySelectorDim)
        .group(categorySelectorSelect);
}

function show_category_graph(ndx) {
    var categoryDim = ndx.dimension(dc.pluck("recipe_name"));
    var categoryMix = categoryDim.group().reduceSum(dc.pluck('category'));

    dc.barChart("#category-graph")
        .width(350)
        .height(250)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(categoryDim)
        .group(categoryMix)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .elasticY(true)
        .xAxisLabel("Category")
        .yAxis().ticks(20);
}
