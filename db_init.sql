CREATE DATABASE auto_anime;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `anime_list`;
CREATE TABLE `anime_list` (
  `index` int NOT NULL AUTO_INCREMENT,
  `mikan_id` int DEFAULT NULL,
  `anime_name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `update_day` int DEFAULT NULL COMMENT '剧场版和ova为8',
  `img_url` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `anime_type` int DEFAULT NULL COMMENT '0为番剧,1为剧场版,2为ova',
  `subscribe_status` int DEFAULT NULL COMMENT '0为未订阅,1为已订阅',
  PRIMARY KEY (`index`),
  UNIQUE KEY `anime_name` (`anime_name`),
  UNIQUE KEY `mikan_id` (`mikan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;