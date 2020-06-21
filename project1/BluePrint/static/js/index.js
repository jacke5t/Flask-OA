var myChart = echarts.init(document.getElementById('show'));
var option = {
    title: {
        text: '公司各部门职员人数统计'
    },
    tooltip: {},
    legend: {
        data: ['职员人数']
    },
    xAxis: {
        data: []
    },
    yAxis: {},
    series: [{
        name: '职员人数',
        type: 'bar', //柱状图
        data: []
    }]
};
$.ajax(
    {
        url:"/show",
        type:"get",
        data:"",
        success: function (data) {
            option["xAxis"]["data"] = data["x"]
            option["series"][0]["data"] = data["y"]
            myChart.setOption(option);
        },
        error: function (data) {
            alert("error")
        }
    }
)
