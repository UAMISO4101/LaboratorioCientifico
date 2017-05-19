type = ['','info','success','warning','danger'];


demo = {

    proveedor : 0.0,
    perdida : 0.0,
    experimento: 0.0,
    devolucion: 0.0,
    paso: 0.0,
    labels:[],
    series:[],
    high:0,
    unidad:"",
    nofity:null,
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
    },
    initChartLine: function () {
        var dataSales = {
          labels: this.labels,
          series: [this.series]
        };

        var optionsSales = {
          lineSmooth: false,
          low: 0,
          high: this.high,
          showArea: true,
          height: "280px",
          axisX: {
            showGrid: true,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: true,
          showPoint: true,
            fullWidth: true,
            plugins: [
                    Chartist.plugins.ctAxisTitle({
                        axisX: {
                            axisTitle: 'Fecha de ejecución de Transacción',
                            axisClass: 'ct-axis-title',
                            offset: {
                                x: 0,
                                y: 35
                            },
                            textAnchor: 'middle'
                        },
                        axisY: {
                            axisTitle: 'Cantidad ('+this.unidad+')',
                            axisClass: 'ct-axis-title',
                            offset: {
                                x: -60,
                                y: 0
                            },
                            flipTitle: false
                        }
                    })
                ]
        };

        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];
        Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);
    },
    showNotification: function(from, align, message){
    	this.nofity = $.notify({
        	icon: "pe-7s-info",
        	message: message

        },{
            type: type[1],
            timer: 20000,
            allow_dismiss: false,
            placement: {
                from: from,
                align: align
            }
        });
	},
    closeNotification:function () {
        this.nofity.close();
    },
    actualizarNotificaciones:function()
    {
        $.getJSON("../obtenerProductosOrdenPendiente").done(function (data) {
            if(data)
            {
                productos = data.productos;
                produc = $.parseJSON(productos)
                console.log(produc.length)
                var prod;
                var strn = "";
                if(produc.length > 0)
                {
                    $("#linkOrdenes").html('<i class="fa fa-globe"></i> <b class="caret"></b> <span class="notification">'+produc.length+'</span>');
                    for(prod in produc)
                    {
                        id = produc[prod].id
                        punto_pedido = produc[prod].punto_pedido
                        nivel_actual = produc[prod].nivel_actual
                        message = '<p style="text-align: justify">El recurso actual tiene un <b>nivel disponible</b> de '+ nivel_actual+ ' y un <b>punto de pedido (mínimo)</b> de '+ punto_pedido + ' por lo que se recomienda generar una orden de reposición. Desea generarla automáticamente?</p> <button class="btn btn-success" onclick="demo.crearOrdenReapro('+id+')"><span class="pe-7s-check"></span> Si</button><button style="margin-left: 80px !important;" class="btn btn-danger" onclick="demo.posponerOrdenRepo('+id+')"><span class="pe-7s-close-circle"></span> No</button>';
                        strn+='<li><a href="#" onclick="demo.showNotification(\''+'bottom'+'\')">'+produc[prod].nombre+'</a></li>';
                        prod++;
                    }
                    $("#dropOrdenes").html(strn);
                }
                else
                {
                    $("#linkOrdenes").html('<i class="fa fa-globe"></i> <b class="caret"></b>');
                    $("#dropOrdenes").html('<li><a href="#">No hay ordenes de reposición <br>pendientes.</a> </li>')
                }
            }
        })
    },
    crearOrdenReapro: function (id)
    {
        if(id == null)
        {
            $.getJSON("../crearOrdenReposicion").done(function (data) {
            if(data)
            {
                mensaje = data.mensaje
                console.log(mensaje);
                if(mensaje == "ok")
                {
                    this.closeNotification();
                    $("#modalOrden").modal('show');
                }
                else
                {
                    this.showNotification('bottom', 'center', mensaje)
                }
            }
            })
        }
        else
        {

        }

    },
    posponerOrdenRepo: function(id)
    {
        $.getJSON("../guardarNotificacionOrden").done(function (data) {
            if(data)
            {
                mensaje = data.mensaje
                console.log(mensaje);
                if(mensaje == "ok")
                {
                    this.closeNotification();
                    this.actualizarNotificaciones();
                }
            }
        })
    }
};




