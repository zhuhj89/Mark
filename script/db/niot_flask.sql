/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50534
Source Host           : 127.0.0.1:3306
Source Database       : app

Target Server Type    : MYSQL
Target Server Version : 50534
File Encoding         : 65001

Date: 2014-07-08 13:50:58
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `agent_account_record`
-- ----------------------------
DROP TABLE IF EXISTS `agent_account_record`;
CREATE TABLE `agent_account_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) NOT NULL,
  `balance` decimal(8,2) NOT NULL,
  `operate` int(11) NOT NULL,
  `record_desc` varchar(200) DEFAULT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of agent_account_record
-- ----------------------------

-- ----------------------------
-- Table structure for `agent_info`
-- ----------------------------
DROP TABLE IF EXISTS `agent_info`;
CREATE TABLE `agent_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agent_name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `status` int(11) NOT NULL,
  `comp_name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `balance_remind` decimal(8,2) NOT NULL,
  `domain_price_id` int(11) NOT NULL,
  `url` varchar(255) NOT NULL,
  `abuse_email` varchar(255) NOT NULL,
  `abuse_phone` varchar(255) NOT NULL,
  `balance` decimal(8,2) NOT NULL,
  `update_date` datetime NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `agent_name` (`agent_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of agent_info
-- ----------------------------

-- ----------------------------
-- Table structure for `audit_data`
-- ----------------------------
DROP TABLE IF EXISTS `audit_data`;
CREATE TABLE `audit_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `record_id` int(11) NOT NULL,
  `pic_desc` varchar(200) NOT NULL,
  `pic_url` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of audit_data
-- ----------------------------

-- ----------------------------
-- Table structure for `audit_process`
-- ----------------------------
DROP TABLE IF EXISTS `audit_process`;
CREATE TABLE `audit_process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `next_user_id` int(11) DEFAULT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of audit_process
-- ----------------------------

-- ----------------------------
-- Table structure for `audit_record`
-- ----------------------------
DROP TABLE IF EXISTS `audit_record`;
CREATE TABLE `audit_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) NOT NULL,
  `audit_type` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of audit_record
-- ----------------------------

-- ----------------------------
-- Table structure for `audit_record_detail`
-- ----------------------------
DROP TABLE IF EXISTS `audit_record_detail`;
CREATE TABLE `audit_record_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `record_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `to_user_id` int(11) DEFAULT NULL,
  `desc` varchar(400) NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of audit_record_detail
-- ----------------------------

-- ----------------------------
-- Table structure for `audit_user`
-- ----------------------------
DROP TABLE IF EXISTS `audit_user`;
CREATE TABLE `audit_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) NOT NULL,
  `audit_type` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of audit_user
-- ----------------------------

-- ----------------------------
-- Table structure for `auth_info`
-- ----------------------------
DROP TABLE IF EXISTS `auth_info`;
CREATE TABLE `auth_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auth_code` varchar(20) NOT NULL,
  `auth_name` varchar(50) NOT NULL,
  `auth_desc` varchar(100) DEFAULT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_code` (`auth_code`),
  UNIQUE KEY `auth_name` (`auth_name`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_info
-- ----------------------------
INSERT INTO `auth_info` VALUES ('1', 'add_auth', '增加权限', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('2', 'del_auth', '删除权限', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('3', 'upd_auth', '修改权限', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('4', 'que_auth', '查询权限', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('5', 'add_role', '增加角色', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('6', 'del_role', '删除角色', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('7', 'upd_role', '修改角色', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('8', 'que_role', '查询角色', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('9', 'add_user', '增加用户', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('10', 'upd_user', '修改用户', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('11', 'que_user', '查询用户', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('12', 'set_aud_pro', '设置审核流程', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('13', 'add_agent', '增加注册商', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('14', 'upd_agent', '修改注册商', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('15', 'que_agent', '查询注册商', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('16', 'que_bill', '查询账单', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('17', 'que_detail', '查询账单明细', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('18', 'upd_price', '修改域名定价', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('19', 'charge', '充值', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('20', 'deduct', '扣费', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('21', 'set_domain', '设置域名规范', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('22', 'que_domain', '查询域名', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('23', 'que_host', '查询主机', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('24', 'que_contact', '查询联系人', null, '1', '0000-00-00 00:00:00');
INSERT INTO `auth_info` VALUES ('25', 'que_aud', '查询审核信息', null, '1', '0000-00-00 00:00:00');

-- ----------------------------
-- Table structure for `domain_keyword`
-- ----------------------------
DROP TABLE IF EXISTS `domain_keyword`;
CREATE TABLE `domain_keyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword_type` int(11) NOT NULL,
  `content` varchar(100) NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of domain_keyword
-- ----------------------------

-- ----------------------------
-- Table structure for `domain_pay_record`
-- ----------------------------
DROP TABLE IF EXISTS `domain_pay_record`;
CREATE TABLE `domain_pay_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `amount` decimal(8,2) NOT NULL,
  `due_date` datetime NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of domain_pay_record
-- ----------------------------

-- ----------------------------
-- Table structure for `domain_price`
-- ----------------------------
DROP TABLE IF EXISTS `domain_price`;
CREATE TABLE `domain_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` decimal(8,2) NOT NULL,
  `pay_type` int(11) NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of domain_price
-- ----------------------------

-- ----------------------------
-- Table structure for `migrate_version`
-- ----------------------------
DROP TABLE IF EXISTS `migrate_version`;
CREATE TABLE `migrate_version` (
  `repository_id` varchar(250) NOT NULL,
  `repository_path` text,
  `version` int(11) DEFAULT NULL,
  PRIMARY KEY (`repository_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of migrate_version
-- ----------------------------
INSERT INTO `migrate_version` VALUES ('database repository', 'G:\\Test\\NiotFlask\\db_repository', '0');

-- ----------------------------
-- Table structure for `role_auth_info`
-- ----------------------------
DROP TABLE IF EXISTS `role_auth_info`;
CREATE TABLE `role_auth_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `auth_id` int(11) NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role_auth_info
-- ----------------------------
INSERT INTO `role_auth_info` VALUES ('1', '1', '1', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('2', '1', '2', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('3', '1', '3', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('4', '1', '4', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('5', '1', '5', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('6', '1', '6', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('7', '1', '7', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('8', '1', '8', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('9', '1', '9', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('10', '1', '10', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('11', '1', '11', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('12', '1', '12', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('13', '2', '13', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('14', '2', '14', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('15', '2', '15', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('16', '2', '16', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('17', '2', '17', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('18', '2', '18', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('19', '2', '19', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('20', '2', '20', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('21', '2', '21', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('22', '2', '22', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('23', '2', '23', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('24', '2', '24', '1', '0000-00-00 00:00:00');
INSERT INTO `role_auth_info` VALUES ('25', '3', '25', '1', '0000-00-00 00:00:00');

-- ----------------------------
-- Table structure for `role_info`
-- ----------------------------
DROP TABLE IF EXISTS `role_info`;
CREATE TABLE `role_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_code` varchar(20) NOT NULL,
  `role_name` varchar(50) NOT NULL,
  `role_desc` varchar(100) DEFAULT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_code` (`role_code`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role_info
-- ----------------------------
INSERT INTO `role_info` VALUES ('1', 'sys_admin', '系统管理员', null, '0', '0000-00-00 00:00:00');
INSERT INTO `role_info` VALUES ('2', 'bus_admin', '业务管理员', null, '1', '0000-00-00 00:00:00');
INSERT INTO `role_info` VALUES ('3', 'operator', '审核员', null, '2', '0000-00-00 00:00:00');

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(80) NOT NULL,
  `role` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `ix_user_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for `user_info`
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `creator` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES ('1', 'admin', 'admin', '1', '1', '系统管理员', 'xiaoqian@cnnic.cn', '', '0', '0000-00-00 00:00:00');
