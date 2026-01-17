import mysql from 'mysql2/promise';

async function testConnection() {
  console.log('🔍 Testando conexão com TiDB...\n');
  
  const config = {
    host: 'gateway01.us-east-1.prod.aws.tidbcloud.com',
    port: 4000,
    user: 'h6W26w7VsTqTswg.root',
    password: 'uXcL29gfOSzifpIF',
    database: 'test',
    ssl: {
      rejectUnauthorized: true,
    },
  };

  try {
    // Criar conexão
    console.log('📡 Conectando ao banco de dados...');
    const connection = await mysql.createConnection(config);
    console.log('✅ Conexão estabelecida com sucesso!\n');

    // Testar query simples
    console.log('📊 Listando tabelas...');
    const [tables] = await connection.query('SHOW TABLES');
    console.log('Tabelas encontradas:', tables.length);
    tables.forEach((table) => {
      console.log('  -', Object.values(table)[0]);
    });
    console.log('');

    // Testar inserção em uma tabela existente (contact_messages)
    console.log('💾 Testando inserção de dados...');
    const testData = {
      name: 'Test Admin',
      email: 'admin@test.com',
      subject: 'Test from admin panel',
      message: 'Testing database connection and save functionality',
      status: 'unread',
    };

    const [insertResult] = await connection.query(
      'INSERT INTO contact_messages (name, email, subject, message, status) VALUES (?, ?, ?, ?, ?)',
      [testData.name, testData.email, testData.subject, testData.message, testData.status]
    );
    
    console.log('✅ Dados inseridos com sucesso!');
    console.log('   ID inserido:', insertResult.insertId);
    console.log('');

    // Verificar se os dados foram salvos
    console.log('🔍 Verificando dados salvos...');
    const [rows] = await connection.query(
      'SELECT * FROM contact_messages WHERE id = ?',
      [insertResult.insertId]
    );
    
    if (rows.length > 0) {
      console.log('✅ Dados recuperados com sucesso!');
      console.log('   Dados:', JSON.stringify(rows[0], null, 2));
    } else {
      console.log('❌ Erro: Dados não foram encontrados após inserção');
    }
    console.log('');

    // Limpar dados de teste
    console.log('🧹 Limpando dados de teste...');
    await connection.query('DELETE FROM contact_messages WHERE id = ?', [insertResult.insertId]);
    console.log('✅ Dados de teste removidos\n');

    await connection.end();
    console.log('✅ Teste concluído com sucesso! O banco de dados está funcionando corretamente.\n');
    
  } catch (error) {
    console.error('❌ Erro durante o teste:');
    console.error('   Mensagem:', error.message);
    console.error('   Código:', error.code);
    console.error('   Stack:', error.stack);
    process.exit(1);
  }
}

testConnection();
