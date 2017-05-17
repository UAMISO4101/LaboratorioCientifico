
-- STATUSCONTEO
INSERT INTO laboratorio_tipo (grupo, nombre, valor) SELECT 'STATUSCONTEO', 'Ejecutada', '1'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'STATUSCONTEO' and nombre = 'Ejecutada');

INSERT INTO laboratorio_tipo (grupo, nombre, valor) SELECT 'STATUSCONTEO', 'Conteo Fisico', '2'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'STATUSCONTEO' and nombre = 'Conteo Fisico');

INSERT INTO laboratorio_tipo (grupo, nombre, valor) SELECT 'STATUSCONTEO', 'Ajustes', '3'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'STATUSCONTEO' and nombre = 'Ajustes');

INSERT INTO laboratorio_tipo (grupo, nombre, valor) SELECT 'STATUSCONTEO', 'Cerrada', '4'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'STATUSCONTEO' and nombre = 'Cerrada');


-- TIPOINVENTARIOPRODUCTO
INSERT INTO laboratorio_tipo (grupo, nombre) SELECT 'TIPOINVENTARIOPRODUCTO', 'A'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'TIPOINVENTARIOPRODUCTO' and nombre = 'A');

INSERT INTO laboratorio_tipo (grupo, nombre) SELECT 'TIPOINVENTARIOPRODUCTO', 'B'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'TIPOINVENTARIOPRODUCTO' and nombre = 'B');

INSERT INTO laboratorio_tipo (grupo, nombre) SELECT 'TIPOINVENTARIOPRODUCTO', 'C'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'TIPOINVENTARIOPRODUCTO' and nombre = 'C');


-- TIPODIFERENCIA
INSERT INTO laboratorio_tipo (grupo, nombre, valor) SELECT 'TIPODIFERENCIA', 'Exceso', '1'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'TIPODIFERENCIA' and nombre = 'Exceso');

INSERT INTO laboratorio_tipo (grupo, nombre, valor) SELECT 'TIPODIFERENCIA', 'Defecto', '2'
WHERE NOT EXISTS (SELECT 1 FROM laboratorio_tipo WHERE grupo = 'TIPODIFERENCIA' and nombre = 'Defecto');