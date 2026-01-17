import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./db/schema.ts",
  out: "./drizzle",
  dialect: "mysql",
  dbCredentials: {
    host: "gateway01.us-east-1.prod.aws.tidbcloud.com",
    port: 4000,
    user: "h6W26w7VsTqTswg.root",
    password: "uXcL29gfOSzifpIF",
    database: "test",
    ssl: {
      rejectUnauthorized: true,
    },
  },
});
