-- Current sql file was generated after introspecting the database
-- If you want to run this migration please uncomment this code before executing migrations
/*
CREATE TABLE `contact_messages` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`email` varchar(320) NOT NULL,
	`subject` varchar(255),
	`message` text NOT NULL,
	`status` enum('unread','read','replied') NOT NULL DEFAULT 'unread',
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP'
);
--> statement-breakpoint
CREATE TABLE `dynamic_links` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`key` varchar(100) NOT NULL,
	`label` varchar(255) NOT NULL,
	`url` varchar(500) NOT NULL,
	`icon` varchar(50),
	`location` varchar(100),
	`is_active` tinyint(1) NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP
);
--> statement-breakpoint
CREATE TABLE `schedule_events` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`day_of_week` int(11) NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` text,
	`image_url` varchar(500),
	`start_time` varchar(50),
	`end_time` varchar(50),
	`is_active` tinyint(1) NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	`vod_url` varchar(500),
	`display_order` int(11) DEFAULT 0
);
--> statement-breakpoint
CREATE TABLE `sponsorship_categories` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`name` varchar(255) NOT NULL,
	`description` text,
	`display_order` int(11) NOT NULL DEFAULT 0,
	`is_active` tinyint(1) NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	`vod_url` varchar(500)
);
--> statement-breakpoint
CREATE TABLE `sponsorship_pricing` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`content_type` varchar(255) NOT NULL,
	`price` varchar(50) NOT NULL,
	`description` text,
	`is_active` tinyint(1) NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	`display_order` int(11) DEFAULT 0,
	`vod_url` varchar(500)
);
--> statement-breakpoint
CREATE TABLE `sponsorships` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`category_id` int(11) NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` text,
	`image_url` varchar(500),
	`external_url` varchar(500),
	`display_order` int(11) NOT NULL DEFAULT 0,
	`is_active` tinyint(1) NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	`vod_url` varchar(500)
);
--> statement-breakpoint
CREATE TABLE `streamer_profile` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`twitch_username` varchar(255) NOT NULL,
	`twitch_user_id` varchar(255),
	`biography` text,
	`youtube_url` varchar(500),
	`twitch_url` varchar(500),
	`profile_image_url` varchar(500),
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	`display_order` int(11) DEFAULT 0,
	`vod_url` varchar(500),
	`is_active` tinyint(1) DEFAULT 1
);
--> statement-breakpoint
CREATE TABLE `users` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`openId` varchar(64) NOT NULL,
	`name` text,
	`email` varchar(320),
	`loginMethod` varchar(64),
	`role` enum('user','admin') NOT NULL DEFAULT 'user',
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	`lastSignedIn` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP'
);
--> statement-breakpoint
CREATE TABLE `vods` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` text,
	`video_url` varchar(500) NOT NULL,
	`thumbnail_url` varchar(500),
	`platform` varchar(50) DEFAULT 'youtube',
	`duration` varchar(50),
	`is_active` tinyint(1) NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP
);
--> statement-breakpoint
CREATE TABLE `watched_content` (
	`id` int(11) AUTO_INCREMENT NOT NULL,
	`user_id` int(11) NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` text,
	`image_url` varchar(500),
	`external_url` varchar(500),
	`rating` int(11),
	`content_type` varchar(100),
	`display_order` int(11) NOT NULL DEFAULT 0,
	`is_active` tinyint(1) NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
	`updatedAt` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	`vod_url` varchar(500),
	`year` int(11),
	`studio` varchar(255)
);
--> statement-breakpoint
CREATE INDEX `key` ON `dynamic_links` (`key`);
*/