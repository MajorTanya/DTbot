USE `dtbot`;

-- App Command Stats

CREATE PROCEDURE IF NOT EXISTS `AddNewAppCommand`(IN `newCommandName` varchar(30))
BEGIN
    INSERT IGNORE INTO `appcommandstats` (command_name) VALUES (newCommandName);
END;

CREATE PROCEDURE IF NOT EXISTS `CheckAppCommandExist`(IN `lookupCommandName` varchar(30))
BEGIN
    SELECT IFNULL((SELECT TRUE FROM `appcommandstats` WHERE command_name = lookupCommandName LIMIT 1), FALSE);
END;

CREATE PROCEDURE IF NOT EXISTS `IncrementAppCommandUsage`(IN `targetCommandName` varchar(30))
BEGIN
    UPDATE IGNORE `appcommandstats` SET times_used = times_used + 1 WHERE command_name = targetCommandName;
END;

-- Servers

CREATE PROCEDURE IF NOT EXISTS `AddNewServer`(IN `newServerId` bigint, IN `newServerMembers` int)
BEGIN
    INSERT INTO `servers` (server_id, server_members)
    VALUES (newServerId, newServerMembers)
    ON DUPLICATE KEY UPDATE server_members = newServerMembers, bot_in_server = 1;
END;

CREATE PROCEDURE IF NOT EXISTS `GetServers`()
BEGIN
    SELECT server_id FROM `servers` WHERE bot_in_server = 1;
END;

CREATE PROCEDURE IF NOT EXISTS `InvalidateMissingServer`(IN `serverIdToInvalidate` bigint)
BEGIN
    UPDATE `servers` SET bot_in_server = 0 WHERE server_id = serverIdToInvalidate;
END;

-- Users

CREATE PROCEDURE IF NOT EXISTS `AddNewUser`(IN `newUserId` bigint)
BEGIN
    INSERT IGNORE INTO `users` (user_id) VALUES (newUserId);
END;

CREATE PROCEDURE IF NOT EXISTS `CheckUserExist`(IN `lookupUserId` bigint)
BEGIN
    SELECT IFNULL((SELECT TRUE FROM `users` WHERE user_id = lookupUserId LIMIT 1), FALSE);
END;

CREATE PROCEDURE IF NOT EXISTS `CheckXPTime`(IN `lookupUserId` bigint)
BEGIN
    SELECT user_last_xp_gain FROM `users` WHERE user_id = lookupUserId LIMIT 1;
END;

CREATE PROCEDURE IF NOT EXISTS `GetUserXp`(IN `lookupUserId` bigint)
BEGIN
    SELECT IFNULL((SELECT user_xp FROM `users` WHERE user_id = lookupUserId LIMIT 1), 0);
END;

CREATE PROCEDURE IF NOT EXISTS `IncreaseXP`(IN `targetUserId` bigint, IN `newXp` int, IN `lastXpGain` int)
BEGIN
    UPDATE IGNORE `users`
    SET user_xp           = user_xp + newXp,
        user_last_xp_gain = lastXpGain
    WHERE user_id = targetUserId;
END;
