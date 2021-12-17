DROP TABLE IF EXISTS todos;
CREATE TABLE todos
(
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar
(30) NOT NULL,
  `status` varchar
(15) NOT NULL,
  PRIMARY KEY
(`id`)
);

LOCK TABLES `todos` WRITE;