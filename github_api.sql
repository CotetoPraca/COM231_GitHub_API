---------------------
--- CREATE TABLES ---
---------------------
CREATE TABLE user_account (
  	user_id INT PRIMARY KEY,
  	user_login VARCHAR(40) NOT NULL,
  	real_name VARCHAR(64) NOT NULL,
  	avatar_url VARCHAR(255),
  	html_url VARCHAR(255) NOT NULL
);

CREATE TABLE repository (
    repository_id INT PRIMARY KEY,
	owner_id INT NOT NULL,
    repo_name VARCHAR(40) NOT NULL,
    repo_full_name VARCHAR(100) NOT NULL,
    private BOOLEAN NOT NULL,
    description TEXT,
	main_language VARCHAR(30),
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	html_url VARCHAR(255) NOT NULL,
	
	FOREIGN KEY (owner_id) REFERENCES user_account(user_id)
);

CREATE TABLE issue (
	issue_id INT PRIMARY KEY,
	user_id INT NOT NULL,
	repository_id INT NOT NULL,
	title VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	closed_at TIMESTAMP,
	labels_name VARCHAR(50) ARRAY,
	
	FOREIGN KEY (user_id) REFERENCES user_account(user_id),
	FOREIGN KEY (repository_id) REFERENCES repository(repository_id)
);

CREATE TABLE pull_request (
	pull_request_id INT PRIMARY KEY,
	user_id INT NOT NULL,
	repository_id INT NOT NULL,
	title VARCHAR(70) NOT NULL,
	body TEXT,
	status VARCHAR(15) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	closed_at TIMESTAMP,
	merged_at TIMESTAMP,
	
	FOREIGN KEY (user_id) REFERENCES user_account(user_id),
	FOREIGN KEY (repository_id) REFERENCES repository(repository_id)
);

CREATE TABLE git_commit (
	commit_id CHAR(40) PRIMARY KEY,
	pull_request_id INT NOT NULL,
	repository_id INT NOT NULL,
	commit_message TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL,
	approved_at TIMESTAMP,
	html_url VARCHAR(255) NOT NULL,
	
	FOREIGN KEY (pull_request_id) REFERENCES pull_request(pull_request_id),
	FOREIGN KEY (repository_id) REFERENCES repository(repository_id)
);

---------------
--- INDEXES ---
---------------
CREATE INDEX idx_user_login ON user_account(user_login); -- Índice para achar o usuário pelo login
CREATE INDEX idx_repo_owner_id ON repository(owner_id); -- Índice para encontrar o repositório ID do dono
CREATE INDEX idx_issue_repo_id ON issue(repository_id); -- Índice para encontrar as issues de um repositório
CREATE INDEX idx_pull_req_repo_id ON pull_request(repository_id); -- Índice para encontrar as pull requests de um repositório
CREATE INDEX idx_commit_pull_req_id ON git_commit(pull_request_id); -- Índice para encontrar os commits de uma pull request
CREATE INDEX idx_commit_repo_id ON git_commit(repository_id); -- Índice para encontrar os commits em um repositório

-- Deleção dos índices para testes de performance
DROP INDEX idx_user_login;
DROP INDEX idx_repo_owner_id;
DROP INDEX idx_issue_repo_id;
DROP INDEX idx_pull_req_repo_id;
DROP INDEX idx_commit_pull_req_id;
DROP INDEX idx_commit_repo_id;

--------------------
--- SELECT TESTS ---
--------------------
SELECT COUNT (repository_id) AS repositories_count FROM repository;
SELECT COUNT (user_id) AS users_count FROM user_account;
SELECT COUNT (issue_id) AS issues_count FROM issue;
SELECT COUNT (pull_request_id) AS pull_requests_count FROM pull_request;
SELECT COUNT (commit_id) AS commits_count FROM git_commit;

--------------------
--- CREATE VIEWS ---
--------------------
CREATE VIEW count_data_in_database AS
SELECT
    (SELECT COUNT(repository_id) FROM repository) AS repositories_count,
    (SELECT COUNT(user_id) FROM user_account) AS users_count,
    (SELECT COUNT(issue_id) FROM issue) AS issues_count,
    (SELECT COUNT(pull_request_id) FROM pull_request) AS pull_requests_count,
    (SELECT COUNT(commit_id) FROM git_commit) AS commits_count,
    (SELECT SUM(count) 
        FROM (
	   SELECT COUNT(repository_id) AS count FROM repository
	   UNION ALL
	   SELECT COUNT(user_id) FROM user_account
	   UNION ALL
	   SELECT COUNT(issue_id) FROM issue
	   UNION ALL
	   SELECT COUNT(pull_request_id) FROM pull_request
	   UNION ALL
	   SELECT COUNT(commit_id) FROM git_commit 
        ) AS subquery 
    ) AS total_count;
	
SELECT * FROM count_data_in_database;

DROP VIEW count_data_in_database;

--------------------
--- CREATE USERS ---
--------------------
CREATE USER myuser WITH PASSWORD 'user';
CREATE USER myadmin WITH PASSWORD 'admin';

------------------
--- USER ROLES ---
------------------
CREATE ROLE usuario_padrao;
CREATE ROLE usuario_admin;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO usuario_padrao;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO usuario_admin;

GRANT usuario_padrao TO myuser;
GRANT usuario_admin TO myadmin;





