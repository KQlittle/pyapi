// echarts-script.js

document.addEventListener('DOMContentLoaded', function() {
    var dom = document.getElementById('container');
    var myChart = echarts.init(dom, null, {
      renderer: 'canvas',
      useDirtyRect: false
    });
  
    var option = {
      title: {
        text: 'Referer of a Website',
        subtext: 'Fake Data',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: 'Access From',
          type: 'pie',
          radius: '50%',
          data: [],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };
  
    if (option && typeof option === 'object') {
      myChart.setOption(option);
    }
  
    // 定义函数用于获取数据和更新图表
    function updateChart() {
      // 使用 jQuery 从 URL 获取 JSON 数据
      $.getJSON('http://127.0.0.1:5000/api', function(data) {
        // 将获取的数据更新到 ECharts 的 option 中
        option.series[0].data = data;
  
        // 使用新的 option 更新图表
        myChart.setOption(option);
      });
    }
  
    // 初始加载一次数据
    updateChart();
  
    // 设置每隔一段时间自动刷新
    setInterval(updateChart, 5000); // 5000 毫秒，即 5 秒刷新一次
  
    window.addEventListener('resize', myChart.resize);
  });
  