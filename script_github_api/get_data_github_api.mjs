import pkg from 'pg';
const { Client } = pkg;

import moment from 'moment';
import fetch from 'node-fetch';
import fs from 'fs';

const accessToken = 'some_git_hub_token'; // Substitua pelo seu token de autenticação do GitHub
const page = 4
const perPage = 100
const startDate = '2021-02-01'; // formato YYYY-MM-DD
const endDate = '2021-03-01';   // formato YYYY-MM-DD

const query = `q=is:public created:${startDate}..${endDate}&sort=created&order=asc&per_page=${perPage}&page=${page}`;
let client;

const parseDateOrNull = (dateString) => {
  const momentDate = moment.utc(dateString);
  return momentDate.isValid() ? momentDate.format('YYYY-MM-DDTHH:mm:ss.SSS') : null;
};

// Função principal (main)
async function main() {
  console.log('\x1b[33m%s\x1b[0m', `Iniciando execução do script...`);
  try {
    // Conectar ao banco de dados
    await connect();

    // Chamar a função para coletar dados
    await fetchAndProcessReposInPage(query, page, accessToken);

  } catch (error) {
    hasError = true; // Define hasError como true se ocorrer um erro
    console.error('Erro durante a execução principal:', error);

  } finally {
    // Sempre desconectar do banco de dados, mesmo em caso de erro
    await disconnect();
  }
}

async function connect() {
  // Certifique-se de que o cliente esteja desconectado antes de criar um novo
  if (client && client.connected) {
    await client.end();
  }

  // Configurações da conexão com o banco de dados
  client = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'github_api',
    password: 'postgres',
    port: 5432,
  });

  await client.connect();
  console.log('Conectado ao banco de dados PostgreSQL');
}

async function insertData(data, tableName) {
  let sql_query;

  try {
    const fields = Object.keys(data).join(', ');
    const values = Object.values(data).map(value => {
      // Tratamento especial para arrays
      if (Array.isArray(value)) {
        return value.length > 0 ? `'{${value.join(',')}}'` : 'NULL';
      }

      // Tratamento especial para valores nulos
      if (value === null) {
        return 'NULL';
      }

      // Escapar as aspas simples nas strings
      if (typeof value === 'string') {
        value = value.replace(/'/g, "''");
        value = value.replace(/[\r]/g, '\\r');
        value = value.replace(/[\n]/g, '\\n');
      }

      return `'${value}'`;
    }).join(', ');

    // Verificação da existência do user_id (em tabelas que ele é foreign key)
    if (["pull_request", "issue"].includes(tableName)) {
      const userIdExist = await client.query('SELECT user_id FROM user_account WHERE user_id = $1', [data.user_id]);

      if (userIdExist.rows.length === 0) {
        console.log(`Ignorando ${tableName} com user_id ${data.user_id}, pois o usuário não existe no banco.`);
        return; // Ignora Pull Requests e Issues que não têm usuário cadastrado no banco
      }
    }

    sql_query = `INSERT INTO ${tableName} (${fields}) VALUES (${values}) ON CONFLICT DO NOTHING;`;

    // console.log('Query a ser executada:', sql_query);

    await client.query(sql_query);
  } catch (error) {
    console.error(`Erro ao inserir dados no PostgreSQL.`);
    console.error(`Campo: ${error.column}`);
    console.error(`Consulta: ${sql_query}`);
    console.error('Código de erro: ', error.code);
    console.error('Detalhes do erro:', error.detail);
    throw error;
  }
}

async function disconnect() {
  try {
    await client.end();
    console.log('Desconectado do banco de dados PostgreSQL');
  } catch (error) {
    console.error('Erro ao desconectar do banco de dados PostgreSQL', error);
    throw error;
  }
}

async function fetchAndRetry(url) {
  const headers = {
    'Authorization': `Bearer ${accessToken}`,
    'User-Agent': 'GitHub-API-Request',
    'X-GitHub-Api-Version': '2022-11-28'
  };
  let response;
  for (let attempt = 0; attempt < 3; attempt++) {
    response = await fetch(url, { headers });
    if (response.status === 200) {
      return await response.json();
    }
  }
  throw new Error(`Erro na solicitação à API do GitHub: ${response.statusText}`);
}

async function fetchPullRequestsData(owner, repoName) {
  const pullRequestsUrl = `https://api.github.com/repos/${owner}/${repoName}/pulls`;
  return fetchAndRetry(pullRequestsUrl);
}

async function fetchPullRequestCommits(owner, repo, pullNumber) {
  const perPage = 5; // Limita a 10 commits por página
  const page = 1; // Começando na primeira página
  const apiVersion = '2022-11-28';

  const url = `https://api.github.com/repos/${owner}/${repo}/pulls/${pullNumber}/commits?per_page=${perPage}&page=${page}`;
  const headers = {
    'Authorization': `Bearer ${accessToken}`, // Substitua com seu token de autenticação
    'User-Agent': 'GitHub-API-Request',
    'Accept': `application/vnd.github.v3+json; version=${apiVersion}`
  };

  const response = await fetch(url, { headers });
  if (response.status === 200) {
    const data = await response.json();
    return data;
  } else {
    throw new Error(`Erro na solicitação à API do GitHub: ${response.statusText}`);
  }
}

async function fetchIssuesData(owner, repoName) {
  const issuesUrl = `https://api.github.com/repos/${owner}/${repoName}/issues`;
  return fetchAndRetry(issuesUrl);
}

async function fetchUserData(userLogin) {
  const userUrl = `https://api.github.com/users/${userLogin}`;
  try {
    const userData = await fetchAndRetry(userUrl);

    if (userData) {
      return userData;
    } else {
      console.error(`Erro na solicitação à API do GitHub para o usuário ${userLogin}: ${userResponse.status} - ${userResponse.statusText}`);
      return null;
    }
  } catch (error) {
    console.error(`Erro na solicitação à API do GitHub para o usuário ${userLogin}: ${error.message}`);
    return null;
  }
}

async function saveToFile(data, fileName) {
  fs.writeFileSync(fileName, JSON.stringify(data, null, 2), 'utf-8');
  console.log(`Dados salvos em ${fileName}`);
}

async function readFromFile(fileName) {
  return new Promise((resolve, reject) => {
    fs.readFile(fileName, 'utf-8', (err, data) => {
      if (err) {
        console.error(`Erro ao ler o arquivo ${fileName}:`, err);
        return reject(err);
      }

      try {
        // Verificar se o arquivo não está vazio
        if (data.trim() === '') {
          return resolve([]);
        }

        const parsedData = JSON.parse(data);
        resolve(parsedData);
      } catch (parseError) {
        console.error(`Erro ao fazer parse do JSON do arquivo ${fileName}:`, parseError);
        reject(parseError);
      }
    });
  });
}

async function fetchAndProcessReposInPage(query, page, accessToken) {
  const searchUrl = `https://api.github.com/search/repositories?${query}`;
  const headers = {
    'Authorization': `Bearer ${accessToken}`,
    'User-Agent': 'GitHub-API-Request',
    'X-GitHub-Api-Version': '2022-11-28'
  };

  try {
    const response = await fetch(searchUrl, { headers });
    if (response.status === 200) {
      const searchData = await response.json();
      const repositories = searchData.items;
      let _iteracao = 0;

      for (const repo of repositories) {
        _iteracao = _iteracao + 1;
        console.log('\x1b[33m%s\x1b[0m', `Iniciando iteração n° ${_iteracao}...`);
        await client.query('BEGIN'); // Inicia a transação

        try {
          await fetchAndProcessSingleRepo(repo);
          await client.query('COMMIT'); // Comita a transação se tudo ocorrer bem
        } catch (error) {
          await client.query('ROLLBACK'); // Faz o rollback se houver um erro
          console.error(`Erro durante o processamento do repositório ${repo.full_name}:`, error);
        }
        console.log("\n-------------------------------------------\n-------------------------------------------\n");
      }
    } else {
      console.error('Erro na solicitação à API do GitHub:', response.statusText);
    }
  } catch (error) {
    console.error('Erro na solicitação:', error);
    throw error;
  }
}

async function fetchAndProcessSingleRepo(repo) {
  // Carregar repositórios já obtidos do arquivo
  let existingRepos = await readFromFile('repositories_history.json');

  // Filtrar repositórios para remover os existentes
  const isNewRepo = !existingRepos.some(existingRepo => existingRepo.id === repo.id);

  if (isNewRepo) {
    const repositoryId = repo.id;
    const repositoryName = repo.name;
    const repositoryOwner = repo.owner.login;

    console.log('-------------------------------------------');
    console.log('Iniciando leitura do repositório Público:');
    console.log(`ID do Repositório: ${repositoryId}`);
    console.log(`Nome do Repositório: ${repositoryName}`);
    console.log(`Login do Proprietário: ${repositoryOwner}`);
    console.log('-------------------------------------------');
    
    
    // Criar o array para coletar as informações de login dos usuário
    const users = new Set();
    users.add(repositoryOwner);
    
    // Coletar informações do repositório
    console.log('Coletando informações do repositório')
    
    // Mapear os dados do repositório para um novo objeto contendo apenas os campos desejados
    // const repositoryData = await fetchRepoData(repositoryOwner, repositoryName);
    const simplifiedRepositoryData = {
      repository_id: repositoryId,
      owner_id: repo.owner.id,
      repo_name: repositoryName,
      repo_full_name: repo.full_name,
      private: repo.private,
      description: repo.description,
      main_language: repo.language,
      created_at: parseDateOrNull(repo.created_at),
      updated_at: parseDateOrNull(repo.updated_at),
      html_url: repo.html_url
    };
    // await saveToFile(simplifiedRepositoryData, 'json_data/repository_data.json');
    //---------------------------------------------------------------------------------

    // Coletar informações sobre pull requests
    console.log('Coletando informações dos pull requests')
    const pullRequestsData = await fetchPullRequestsData(repositoryOwner, repositoryName);
    const simplifiedPullRequestsData = pullRequestsData.map(pullRequest => {
      // Adicionar o login do usuário ao conjunto 'users'
      if (pullRequest.user && pullRequest.user.login) {
        users.add(pullRequest.user.login);
      }

      return {
        pull_request_id: pullRequest.number,
        user_id: pullRequest.user.id,
        repository_id: repositoryId,
        title: pullRequest.title,
        body: pullRequest.body,
        status: pullRequest.state,
        created_at: parseDateOrNull(pullRequest.created_at),
        updated_at: parseDateOrNull(pullRequest.updated_at),
        closed_at: parseDateOrNull(pullRequest.closed_at),
        merged_at: parseDateOrNull(pullRequest.merged_at)
      };
    });
    // await saveToFile(simplifiedPullRequestsData, 'json_data/pull_requests_data.json');
    //---------------------------------------------------------------------------------

    // Coletar informações sobre commits
    console.log('Coletando informações dos commits');
    const simplifiedCommitsData = [];

    for (const pullRequest of simplifiedPullRequestsData) {
      const pullRequestCommitsData = await fetchPullRequestCommits(repositoryOwner, repositoryName, pullRequest.pull_request_id);

      const commitsInfo = pullRequestCommitsData.map(commit => ({
        commit_id: commit.sha,
        pull_request_id: pullRequest.pull_request_id,
        repository_id: repositoryId,
        commit_message: commit.commit.message,
        created_at: parseDateOrNull(commit.commit.author.date),
        approved_at: parseDateOrNull(commit.commit.committer.date),
        html_url: commit.html_url
      }));

      simplifiedCommitsData.push(...await Promise.all(commitsInfo));
    }
    // await saveToFile(await Promise.all(simplifiedCommitsData), 'json_data/commits_data.json');
    //---------------------------------------------------------------------------------

    // Coletar informações sobre as issues
    console.log('Coletando informações das issues');
    const issuesData = await fetchIssuesData(repositoryOwner, repositoryName);
    const simplifiedIssuesData = issuesData.map(issue => {
      // Adicionar o login do usuário ao conjunto 'users'
      if (issue.user && issue.user.login) {
        users.add(issue.user.login);
      }

      return {
        issue_id: issue.id,
        user_id: issue.user.id,
        repository_id: repositoryId,
        title: issue.title,
        created_at: parseDateOrNull(issue.created_at),
        updated_at: parseDateOrNull(issue.updated_at),
        closed_at: parseDateOrNull(issue.closed_at),
        // Extrair os valores de labels.name e armazená-los em labels_name
        labels_name: issue.labels ? issue.labels.map(label => label.name) : []
      };
    });
    // await saveToFile(simplifiedIssuesData, 'json_data/issues_data.json');
    //---------------------------------------------------------------------------------


    // Coletar informações dos usuários
    console.log('Coletando informações dos usuários');
    const userData = Array.from(users);
    const usersData = [];
    for (const userLogin of userData) {
      const userData = await fetchUserData(userLogin);
      if (userData) {
        usersData.push(userData);
      }
    }

    const filteredUsersData = usersData.map(user => ({
      user_id: user.id,
      user_login: user.login,
      real_name: user.name ? user.name : null,
      avatar_url: user.avatar_url ? user.avatar_url : null,
      html_url: user.html_url
    }));
    // await saveToFile(filteredUsersData, 'json_data/users_data.json');
    //---------------------------------------------------------------------------------

    // Envia as informações coletadas ao banco
    console.log('\x1b[32m%s\x1b[0m', 'Iniciando envio de dados ao banco...');

    console.log(`Enviando ${filteredUsersData.length} dados à tabela user_account`);
    for (const user of filteredUsersData) {
      await insertData(user, 'user_account');
    }

    console.log('Enviando 1 dado  à tabela repository');
    await insertData(simplifiedRepositoryData, 'repository');

    console.log(`Enviando ${simplifiedIssuesData.length} dados à tabela issue`);
    for (const issue of simplifiedIssuesData) {
      await insertData(issue, 'issue');
    }

    console.log(`Enviando ${simplifiedPullRequestsData.length} dados à tabela pull_request`);
    for (const pullRequest of simplifiedPullRequestsData) {
      await insertData(pullRequest, 'pull_request');
    }

    console.log(`Enviando ${simplifiedPullRequestsData.length} dados à tabela git_commit`);
    for (const commit of simplifiedCommitsData) {
      await insertData(commit, 'git_commit');
    }

    console.log('\x1b[32m%s\x1b[0m', 'Finalizando envio de dados...');

    console.log('\x1b[32m%s\x1b[0m', 'Atualizando histórico de repositórios...');
    // Adicionar o repositório escolhido à lista de repositórios existentes
    existingRepos.push({ id: repo.id });

    // Salvar a lista atualizada no arquivo
    await saveToFile(existingRepos, 'repositories_history.json');
  } else {
    console.log(`Repositório ${repo.name} já adicionado ao banco.`);
  }
}

// Executar a função principal
await main();
