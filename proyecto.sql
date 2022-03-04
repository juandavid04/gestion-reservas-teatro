CREATE DATABASE Reservas_teatro;

USE Reservas_teatro;

CREATE TABLE teatro(
id_teatro INT  AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(30) NOT NULL,
gerente VARCHAR(30),
direccion VARCHAR(30) NOT NULL,
telefono VARCHAR(30) NOT NULL,
correo VARCHAR(50) UNIQUE,
contraseña VARCHAR(200),
capacidad_sillas INT,
otros_detalles VARCHAR(30)
);

CREATE TABLE genero(
id_genero INT AUTO_INCREMENT PRIMARY KEY,
descripcion_genero VARCHAR(30) NOT NULL
);

CREATE TABLE produccion(
id_produccion INT AUTO_INCREMENT PRIMARY KEY,
id_genero INT,
id_teatro INT,
nombre VARCHAR(100) NOT NULL,
descripcion VARCHAR(30),
otros_detalles VARCHAR(30),
FOREIGN KEY (id_genero) REFERENCES genero(id_genero),
FOREIGN KEY (id_teatro) REFERENCES teatro(id_teatro)
);

CREATE TABLE bloque_de_sillas(
id_bloque INT AUTO_INCREMENT PRIMARY KEY,
id_teatro INT,
descripcion_bloque VARCHAR(10),
FOREIGN KEY (id_teatro) REFERENCES teatro(id_teatro)
);


CREATE TABLE fila_de_sillas(
id_fila INT AUTO_INCREMENT PRIMARY KEY,
numero_fila INT ,
id_bloque INT,
contador_sillas_por_fila INT,
FOREIGN KEY (id_bloque) REFERENCES bloque_de_sillas (id_bloque)
);

CREATE TABLE actuacion(
id_actuacion INT AUTO_INCREMENT PRIMARY KEY,
id_produccion INT,
fecha_actuacion DATE NOT NULL,
hora_inicio TIME NOT NULL,
hora_fin TIME NOT NULL,
FOREIGN KEY (id_produccion) REFERENCES produccion (id_produccion)
);

CREATE TABLE cliente(
id_cliente INT AUTO_INCREMENT PRIMARY KEY,
nombre1 VARCHAR(15) NOT NULL,
nombre2 VARCHAR(15) NOT NULL,
celular INT NOT NULL,
informacion_tarjeta VARCHAR(90) NOT NULL,
correo VARCHAR(30),
otros_detalles VARCHAR(30)
);

CREATE TABLE reserva(
id_reserva INT AUTO_INCREMENT PRIMARY KEY,
id_cliente INT,
fecha_reserva DATE NOT NULL,
fecha_en_que_se_hizo DATE NOT NULL,
contador_sillas_disponibles INT,
FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE estado_silla(
id_estado VARCHAR(10) PRIMARY KEY,
desc_estado VARCHAR(10) NOT NULL
);

CREATE TABLE sillas_por_actuacion(
numero_silla INT PRIMARY KEY,
id_fila INT,
id_actuacion INT,
id_estado VARCHAR(10),
id_reserva INT,
FOREIGN KEY (id_fila) REFERENCES fila_de_sillas(id_fila),
FOREIGN KEY (id_actuacion) REFERENCES actuacion(id_actuacion),
FOREIGN KEY (id_estado) REFERENCES estado_silla(id_estado),
FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);
ALTER TABLE sillas_por_Actuacion CHANGE numero_silla id_silla INT;
ALTER TABLE sillas_por_Actuacion MODIFY id_silla INT AUTO_INCREMENT;
ALTER TABLE sillas_por_actuacion ADD numero_silla INT; 


delimiter $$
DROP TRIGGER if exists capacidad$$
CREATE TRIGGER capacidad after INSERT ON sillas_por_actuacion
FOR EACH ROW
BEGIN 
	if NEW.id_actuacion IS NULL then 
		UPDATE teatro SET capacidad_sillas = capacidad_sillas + 1
		WHERE id_teatro = (SELECT id_teatro FROM bloque_de_sillas b
								 INNER JOIN fila_de_sillas f ON f.id_bloque = b.id_bloque
								 WHERE f.id_fila = NEW.id_fila );
	END if;	
END
$$
delimiter ;

delimiter $$
DROP TRIGGER if exists disminuir_capacidad$$
CREATE TRIGGER disminuir_capacidad BEFORE DELETE ON sillas_por_actuacion
FOR EACH ROW
BEGIN 
	if OLD.id_actuacion IS NULL then 
		UPDATE teatro SET capacidad_sillas = capacidad_sillas - 1
		WHERE id_teatro = (SELECT id_teatro FROM bloque_de_sillas b
								 INNER JOIN fila_de_sillas f ON f.id_bloque = b.id_bloque
								 WHERE f.id_fila = OLD.id_fila );
	END if;	
END
$$
delimiter ;