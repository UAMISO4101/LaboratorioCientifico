type = ['','info','success','warning','danger'];


demo = {

    proveedor : 0.0,
    perdida : 0.0,
    experimento: 0.0,
    devolucion: 0.0,
    paso: 0.0,
    initChartDonut: function(){
        Chartist.Pie('#chartPreferences', {
          series: [this.proveedor, this.perdida, this.experimento, this.devolucion, this.paso],
        },
        {
            donut: true,
            donutWidth: 60,
            donutSolid: true,
            total: 100,
            showLabel: false
        });
    }
}




