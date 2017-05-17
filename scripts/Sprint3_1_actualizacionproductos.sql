
--Actualización de tipo_producto_conteo para Productos
update laboratorio_producto set tipo_producto_conteo = 'A' where nombre = 'HCL' and tipo_producto_conteo is null;
update laboratorio_producto set tipo_producto_conteo = 'A' where nombre = 'Lactato de 2-etilhexilo' and tipo_producto_conteo is null;
update laboratorio_producto set tipo_producto_conteo = 'B' where nombre = 'ADN - Generico Mono' and tipo_producto_conteo is null;
update laboratorio_producto set tipo_producto_conteo = 'B' where nombre = 'Hongos para cultivo AG' and tipo_producto_conteo is null;
update laboratorio_producto set tipo_producto_conteo = 'C' where nombre = 'Acido Benzoico' and tipo_producto_conteo is null;
update laboratorio_producto set tipo_producto_conteo = 'A' where tipo_producto_conteo is null;
