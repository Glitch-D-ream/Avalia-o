import { drizzle } from "drizzle-orm/mysql2";
import mysql from "mysql2/promise";
import * as schema from "./schema";

// Criar conexão com o banco de dados
const connectionString = process.env.DATABASE_URL || 
  "mysql://h6W26w7VsTqTswg.root:uXcL29gfOSzifpIF@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/test?ssl=true";

// Pool de conexões
const poolConnection = mysql.createPool({
  uri: connectionString,
  ssl: {
    rejectUnauthorized: true,
  },
});

// Instância do Drizzle ORM
export const db = drizzle(poolConnection, { schema, mode: "default" });

// Exportar schema para uso em outras partes da aplicação
export { schema };
