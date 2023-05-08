-- SQLite

INSERT INTO users (id, name, email, is_admin, password) VALUES ("01","admin", "admin", true, "0000");

INSERT INTO plants (id, name, sort, humidity, temperature, p_code, image_path, ref_temperature, ref_humidity, ref_salinity) VALUES ("PL1", "Crocatum", "Piper", 50, 22, "PT1", "assets\\thumbs\plants\Crocatum_130x130.png", 20, 50, 1.8);

INSERT INTO plants (id, name, sort, humidity, temperature, p_code, image_path, ref_temperature, ref_humidity, ref_salinity) VALUES ("PL2", "Deliciosa Variegated", "Monstera", 60, 23, "PT2", "assets\\thumbs\plants\Deliciosa_Variegated_130x130.png", 20, 50, 1.8);

INSERT INTO plants (id, name, sort, humidity, temperature, p_code, image_path, ref_temperature, ref_humidity, ref_salinity) VALUES ("PL3", "Fernwood Mikado", "Sansevieria", 55, 21, "PT3", "assets\\thumbs\plants\Fernwood_Mikado_130x130.png", 20, 50, 1.8);

INSERT INTO plants (id, name, sort, humidity, temperature, p_code, image_path, ref_temperature, ref_humidity, ref_salinity) VALUES ("PL4", "McDowell", "Philodendron", 70, 25, "PT4", "assets\\thumbs\plants\McDowell_1_130x130.png", 20, 50, 1.8);

INSERT INTO plants (id, name, sort, humidity, temperature, p_code, image_path, ref_temperature, ref_humidity, ref_salinity) VALUES ("PL5", "Paraiso Verde", "Philodendron", 45, 20, "PT5", "assets\\thumbs\plants\Paraiso_Verde_130x130.png", 20, 50, 1.8);

INSERT INTO plants (id, name, sort, humidity, temperature, p_code, image_path, ref_temperature, ref_humidity, ref_salinity) VALUES ("PL6", "White Wizard", "Philodendron", 65, 24, "PT6", "assets\\thumbs\plants\White_Wizard_130x130.png", 20, 50, 1.8);


INSERT INTO pots (id, name, radius, image_path) VALUES ("PT1", "Pablo Basket Jute Cream", 14, "assets\\thumbs\pots\Pablo_Basket_Jute_Cream_130x130.png");
INSERT INTO pots (id, name, radius, image_path) VALUES ("PT2", "Stu Pot Green", 14, "assets\\thumbs\pots\Stu_Pot_Green_130x130.png");
INSERT INTO pots (id, name, radius, image_path) VALUES ("PT3", "Lexi Pot Black", 18, "assets\\thumbs\pots\Lexi_Pot_Black_130x130.png");
INSERT INTO pots (id, name, radius, image_path) VALUES ("PT4", "Penny Pot Dark Grey", 17, "assets\\thumbs\pots\Penny_Pot_Dark_Grey_130x130.png");
INSERT INTO pots (id, name, radius, image_path) VALUES ("PT5", "Stan Pot Dark Green", 14, "assets\\thumbs\pots\Stan_Pot_Dark_Green_1_130x130.png");
INSERT INTO pots (id, name, radius, image_path) VALUES ("PT6", "Carlos Pot Green", 13, "assets\\thumbs\pots\Carlos_Pot_Green_130x130.png");
