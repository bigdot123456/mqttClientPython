DROP TABLE IF EXISTS `macmessagetable`;
CREATE TABLE if not exists `macmessagetable` (`id` int8 NOT NULL AUTO_INCREMENT,
`clientID` varchar(32),
`time` datetime, 
`topic` varchar(128),
`message` varchar(1024),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

