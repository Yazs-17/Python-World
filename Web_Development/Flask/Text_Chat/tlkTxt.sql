/*
Navicat SQLite Data Transfer

Source Server         : tlkDB
Source Server Version : 30808
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30808
File Encoding         : 65001

Date: 2017-01-13 19:43:57
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for tlkTxt
-- ----------------------------
DROP TABLE IF EXISTS "main"."tlkTxt";
CREATE TABLE "tlkTxt" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"own"  INTEGER,
"txt"  TEXT
);

-- ----------------------------
-- Indexes structure for table tlkTxt
-- ----------------------------
CREATE INDEX "main"."inx_id"
ON "tlkTxt" ("id" DESC);
