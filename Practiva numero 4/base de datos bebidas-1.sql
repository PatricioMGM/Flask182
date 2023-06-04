DROP DATABASE IF EXISTS bebidas;
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

create user 'almacenbeb'@'localhost' identified by '';
grant all privileges on bebidas.* to 'almacenbeb'@'localhost';

INSERT INTO Marca (Marca) VALUES 
('Coca-Cola'),
('Pepsi'),
('Sprite'),
('Lipton'),
('Gatorade'),
('Fanta'),
('Nescafé'),
('Redbull'),
('Monster'),
('Sevenup')
;

INSERT INTO Clasificaciones (clasificacion) VALUES 
('Agua mineral'),
('Bebidas energéticas'),
('Refrescos'),
('Bebidas gaseosas'),
('Té helado'),
('Café'),
('Bebidas isotónicas'),
('Bebidas alcohólicas'),
('Batidos y smoothies'),
('Agua natural')
;

insert into bebidas (Nombre, Precio, id_clasificacion, id_marca) values
('Pepsi',15,3,2),
('coca-cola',18,3,1)
;