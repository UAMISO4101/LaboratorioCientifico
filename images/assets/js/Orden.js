function Orden(idEstado, idProveedor, idUsuarioCreacion,
                observaciones) {
    this.idEstado = idEstado;
    this.idProveedor = idProveedor;
    this.idUsuarioCreacion = idUsuarioCreacion;
    this.observaciones = observaciones;
    this.items = new Array();
}
