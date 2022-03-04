CREATE DATABASE Reservas_teatro;

USE Reservas_teatro;

CREATE TABLE teatro(
id_teatro INT PRIMARY KEY,
nombre VARCHAR(30) NOT NULL,
gerente VARCHAR(30),
direccion VARCHAR(30),
telefono INT,
capacidad_sillas INT,
otros_detalles VARCHAR(30)
);

CREATE TABLE genero(
codigo_genero INT PRIMARY KEY,
descripcion_genero VARCHAR(30)
);

CREATE TABLE produccion(
id_produccion INT PRIMARY KEY,
codigo_genero INT,
id_teatro INT,
nombre VARCHAR(30),
descripcion VARCHAR(30),
otros_detalles VARCHAR(30),
FOREIGN KEY (codigo_genero) REFERENCES genero(codigo_genero),
FOREIGN KEY (id_teatro) REFERENCES teatro(id_teatro)
);

CREATE TABLE referencia_sillas(
id_codigo_bloque INT PRIMARY KEY,
descripcion_bloque VARCHAR(10)
);

CREATE TABLE sillas_fila(
numero_fila INT PRIMARY KEY,
id_teatro INT,
id_codigo_bloque INT,
contador_silla_por_fila INT,
FOREIGN KEY (id_teatro) REFERENCES teatro(id_teatro),
FOREIGN KEY (id_codigo_bloque) REFERENCES referencia_sillas (id_codigo_bloque)
);

CREATE TABLE actuacion(
id_actuacion INT PRIMARY KEY,
id_produccion INT,
fecha_actuacion DATE,
hora_inicio TIME,
hora_fin TIME,
FOREIGN KEY (id_produccion) REFERENCES produccion (id_produccion)
);

CREATE TABLE cliente(
id_cliente INT PRIMARY KEY,
nombre1 VARCHAR(15),
nombre2 VARCHAR(15),
celular INT,
informacion_tarjeta VARCHAR(90) NOT NULL,
correo VARCHAR(30),
otros_detalles VARCHAR(30)
);

CREATE TABLE reservas(
id_reserva INT PRIMARY KEY,
id_cliente INT,
fecha_reserva DATE,
fecha_en_que_se_hizo DATE,
contador_sillas_disponibles INT,
FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE ref_estado_silla(
estado_silla int PRIMARY KEY,
desc_estado VARCHAR(10)
);

CREATE TABLE sillas_por_actuacion(
numero_silla INT PRIMARY KEY,
numero_fila INT,
id_actuacion INT,
estado_silla VARCHAR(10),
id_reserva INT,
FOREIGN KEY (numero_fila) REFERENCES sillas_fila(numero_fila),
FOREIGN KEY (id_actuacion) REFERENCES actuacion(id_actuacion),
FOREIGN KEY (estado_silla) REFERENCES ref_estado_silla(estado_silla),
FOREIGN KEY (id_reserva) REFERENCES reservas(id_reserva)
);
