type = ['','info','success','warning','danger'];
    	

demo = {

    disponible : 0.0,
    enUso : 0.0,
    initChartDonut: function(){

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };
        
        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };
    
        Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);
        
        Chartist.Pie('#chartPreferences', {
          labels: [this.disponible+'%',this.enUso+'%'],
          series: [this.disponible,this.enUso]
        });   
    },
}

