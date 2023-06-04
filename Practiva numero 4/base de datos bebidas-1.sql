create database bebidas;
use bebidas;
CREATE TABLE Bebidas (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Nombre VARCHAR(50),
  Precio DECIMAL(10,2),
  id_clasificacion int not null,
  id_marca int not null,
  FOREIGN KEY (id_clasificacion) REFERENCES Clasificaciones(id) ON DELETE CASCADE,
  FOREIGN KEY (id_marca) REFERENCES Marca(id) ON DELETE CASCADE
);

create table Clasificaciones (
id int not null primary key auto_increment,
clasificacion varchar(50)
);

create table Marca (
id int not null primary key auto_increment,
Marca varchar(50)
);

create user 'almacenbeb'@'localhost' identified by '123almabb';
grant all privileges on bebidas.* to 'almacenbeb'@'localhost';