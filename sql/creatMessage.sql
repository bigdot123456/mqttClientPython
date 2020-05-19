CREATE TABLE if not exists `macmessagetable` (`id` int8 NOT NULL AUTO_INCREMENT,
`clientID` varchar(32),
`time` datetime,
`topic` varchar(128),
`message` varchar(1024),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

SELECT * FROM fastroot.macblockinfo order by blocknum desc limit 1;

CREATE TABLE if not exists `macblockinfo` (`blocknum` int8 NOT NULL AUTO_INCREMENT,
`index` int8,
`timestamp` datetime,
`winner` varchar(255), -- change from 256 to 255
`winnHash` varchar(64), -- bigint
`winnerAward` int,
`onlineAward` float,
`proof` int8,
`previoushash` int8,
`transactions` varchar(8192), -- should be 8192+32
 PRIMARY KEY (`blocknum`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;