import { mysqlTable, mysqlSchema, AnyMySqlColumn, int, varchar, text, mysqlEnum, timestamp, index, tinyint } from "drizzle-orm/mysql-core"
import { sql } from "drizzle-orm"

export const contactMessages = mysqlTable("contact_messages", {
	id: int().autoincrement().notNull(),
	name: varchar({ length: 255 }).notNull(),
	email: varchar({ length: 320 }).notNull(),
	subject: varchar({ length: 255 }),
	message: text().notNull(),
	status: mysqlEnum(['unread','read','replied']).default('unread').notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
});

export const dynamicLinks = mysqlTable("dynamic_links", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	key: varchar({ length: 100 }).notNull(),
	label: varchar({ length: 255 }).notNull(),
	url: varchar({ length: 500 }).notNull(),
	icon: varchar({ length: 50 }),
	location: varchar({ length: 100 }),
	isActive: tinyint("is_active").default(1).notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
},
(table) => [
	index("key").on(table.key),
]);

export const scheduleEvents = mysqlTable("schedule_events", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	dayOfWeek: int("day_of_week").notNull(),
	title: varchar({ length: 255 }).notNull(),
	description: text(),
	imageUrl: varchar("image_url", { length: 500 }),
	startTime: varchar("start_time", { length: 50 }),
	endTime: varchar("end_time", { length: 50 }),
	isActive: tinyint("is_active").default(1).notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
	vodUrl: varchar("vod_url", { length: 500 }),
	displayOrder: int("display_order").default(0),
});

export const sponsorshipCategories = mysqlTable("sponsorship_categories", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	name: varchar({ length: 255 }).notNull(),
	description: text(),
	displayOrder: int("display_order").default(0).notNull(),
	isActive: tinyint("is_active").default(1).notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
	vodUrl: varchar("vod_url", { length: 500 }),
});

export const sponsorshipPricing = mysqlTable("sponsorship_pricing", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	contentType: varchar("content_type", { length: 255 }).notNull(),
	price: varchar({ length: 50 }).notNull(),
	description: text(),
	isActive: tinyint("is_active").default(1).notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
	displayOrder: int("display_order").default(0),
	vodUrl: varchar("vod_url", { length: 500 }),
});

export const sponsorships = mysqlTable("sponsorships", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	categoryId: int("category_id").notNull(),
	title: varchar({ length: 255 }).notNull(),
	description: text(),
	imageUrl: varchar("image_url", { length: 500 }),
	externalUrl: varchar("external_url", { length: 500 }),
	displayOrder: int("display_order").default(0).notNull(),
	isActive: tinyint("is_active").default(1).notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
	vodUrl: varchar("vod_url", { length: 500 }),
});

export const streamerProfile = mysqlTable("streamer_profile", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	twitchUsername: varchar("twitch_username", { length: 255 }).notNull(),
	twitchUserId: varchar("twitch_user_id", { length: 255 }),
	biography: text(),
	youtubeUrl: varchar("youtube_url", { length: 500 }),
	twitchUrl: varchar("twitch_url", { length: 500 }),
	profileImageUrl: varchar("profile_image_url", { length: 500 }),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
	displayOrder: int("display_order").default(0),
	vodUrl: varchar("vod_url", { length: 500 }),
	isActive: tinyint("is_active").default(1),
});

export const users = mysqlTable("users", {
	id: int().autoincrement().notNull(),
	openId: varchar({ length: 64 }).notNull(),
	name: text(),
	email: varchar({ length: 320 }),
	loginMethod: varchar({ length: 64 }),
	role: mysqlEnum(['user','admin']).default('user').notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
	lastSignedIn: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
});

export const vods = mysqlTable("vods", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	title: varchar({ length: 255 }).notNull(),
	description: text(),
	videoUrl: varchar("video_url", { length: 500 }).notNull(),
	thumbnailUrl: varchar("thumbnail_url", { length: 500 }),
	platform: varchar({ length: 50 }).default('youtube'),
	duration: varchar({ length: 50 }),
	isActive: tinyint("is_active").default(1).notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
});

export const watchedContent = mysqlTable("watched_content", {
	id: int().autoincrement().notNull(),
	userId: int("user_id").notNull(),
	title: varchar({ length: 255 }).notNull(),
	description: text(),
	imageUrl: varchar("image_url", { length: 500 }),
	externalUrl: varchar("external_url", { length: 500 }),
	rating: int(),
	contentType: varchar("content_type", { length: 100 }),
	displayOrder: int("display_order").default(0).notNull(),
	isActive: tinyint("is_active").default(1).notNull(),
	createdAt: timestamp({ mode: 'string' }).default('CURRENT_TIMESTAMP').notNull(),
	updatedAt: timestamp({ mode: 'string' }).defaultNow().onUpdateNow().notNull(),
	vodUrl: varchar("vod_url", { length: 500 }),
	year: int(),
	studio: varchar({ length: 255 }),
});
