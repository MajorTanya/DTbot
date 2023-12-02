CREATE DATABASE IF NOT EXISTS `dtbot` DEFAULT CHARACTER SET 'utf8';

USE `dtbot`;

CREATE TABLE IF NOT EXISTS `appcommandstats`
(
    `command_name` VARCHAR(60) NOT NULL PRIMARY KEY,
    `times_used`   INT         NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS `servers`
(
    `server_id`      BIGINT     NOT NULL PRIMARY KEY,
    `server_prefix`  VARCHAR(3) NOT NULL DEFAULT '+',
    `server_members` INT        NOT NULL DEFAULT 1,
    `bot_in_server`  BOOLEAN    NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS `users`
(
    `user_id`           BIGINT NOT NULL PRIMARY KEY,
    `user_xp`           INT    NOT NULL DEFAULT 0,
    `user_last_xp_gain` INT    NOT NULL DEFAULT 1569888000
);
