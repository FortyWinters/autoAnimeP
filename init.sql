/*
 Navicat Premium Data Transfer

 Source Server         : autoAnime
 Source Server Type    : MySQL
 Source Server Version : 80100 (8.1.0)
 Source Host           : 10.112.5.25:3306
 Source Schema         : auto_anime

 Target Server Type    : MySQL
 Target Server Version : 80100 (8.1.0)
 File Encoding         : 65001

 Date: 20/09/2023 21:35:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for anime_list
-- ----------------------------
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

-- ----------------------------
-- Table structure for anime_seed
-- ----------------------------
DROP TABLE IF EXISTS `anime_seed`;
CREATE TABLE `anime_seed` (
  `index` int NOT NULL AUTO_INCREMENT,
  `mikan_id` int NOT NULL,
  `subgroup_id` int NOT NULL,
  `episode` int NOT NULL,
  `seed_name` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `seed_url` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `seed_url` (`seed_url`)
) ENGINE=InnoDB AUTO_INCREMENT=434 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
-- Table structure for anime_task
-- ----------------------------
DROP TABLE IF EXISTS `anime_task`;
CREATE TABLE `anime_task` (
  `index` int NOT NULL AUTO_INCREMENT,
  `mikan_id` int NOT NULL,
  `status` int DEFAULT NULL COMMENT '下载的状态 0表示还没有开始下载 1表示下载成功 2表示下载开始但是过程失败',
  `episode` int NOT NULL,
  `torrent_name` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;