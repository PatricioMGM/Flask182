use bebidas;
INSERT INTO Marca (Marca) VALUES 
('Coca-Cola'),
('Pepsi'),
('Sprite'),
('Fanta'),
('Dr. Pepper'),
('Mountain Dew'),
('7UP'),
('Mirinda'),
('Crush'),
('Schweppes')
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
('Agua')
;

insert into bebidas (Nombre, Precio, id_clasificacion, id_marca) values
('Pepsi',15,3,2),
('coca-cola',18,3,1)
;








