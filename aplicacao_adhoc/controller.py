from flask import Flask, redirect, render_template, url_for, jsonify, session, request
from flask_wtf.csrf import CSRFProtect

# Import Database Handler
from models import DatabaseHandler

# Import Form templates
from forms import AdHocUserAccountForm
from forms import AdHocRepositoryForm
from forms import AdHocIssueForm
from forms import AdHocPullRequestForm
from forms import AdHocGitCommitForm

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'chave_ultra_secreta_e_extremamente_segura'

class Controller:
  def __init__(self):
    self.db_handler = DatabaseHandler()

  def start(self):
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    print(f'Servidor iniciado em http://{host}:{port}/')
    app.run(host=host, port=port, debug=True)

  @app.route('/', methods=['GET', 'POST'])
  @csrf.exempt
  def login():
    error_message = ''

    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']

      is_valid = controller.db_handler.validate_credentials(username, password)

      if is_valid:
        # Autenticação bem-sucedida, define a variável de sessão
        session['authenticated'] = True
        return redirect(url_for('show_home'))
      else:
        # Autenticação falhou, configura a mensagem de erro
        error_message = 'Usuário ou senha inválidos'
        return render_template('login.html', error_message=error_message)

    # Renderiza a página de login, passando a mensagem de erro
    return render_template('login.html', error_message=error_message)

  @app.route('/home', methods=['GET'])
  def show_home():
    if 'authenticated' not in session or not session['authenticated']:
      return redirect(url_for('login'))
    
    info_to_search = {
      "search_option": "single_table",
      "table": "t_count_data_in_database",
      "columns": [],
      "filters": []
    }
    
    # Implemente a lógica para renderizar a página inicial (home.html) aqui
    json_data = controller.db_handler.search_in_database(info_to_search)

    data_dict = {}
    for i, column in enumerate(json_data['columns']):
      data_dict[column] = json_data['aaData'][0][i]

    return render_template('home.html', **data_dict)


  # --- ADHOC USER ACCOUNT ---
  @app.route('/ad_hoc_user_account', methods=['GET'])
  def ad_hoc_user_account():
    form = AdHocUserAccountForm()
    return render_template('ad_hoc_repository.html', form=form)
  
  @app.route('/ad_hoc_user_account/data', methods=['GET', 'POST'])
  def ad_hoc_user_account_result():
    if request.method == 'POST':
      # Obtém os parâmetros da consulta do request
      table = request.args.get('table', 'UserAccount')
      columns = request.form.getlist('select_columns')
      filters = []
      
      if not columns:
        columns = ['user_id', 'user_login', 'html_url', 'real_name', 'avatar_url']
        
      # Verifica se query_type está no corpo da solicitação POST
      query_type = request.form.get('query_type', '')
      
      if query_type == "select_by_filter":
        filters = [
          {
            "column": request.form.get('select_filter_column', ''),
            "value": request.form.get('select_filter_value', '')
          }
        ]

      # Monta o JSON info_to_search
      info_to_search = {
        "search_option": "single_table",
        "table": table,
        "columns": columns,
        "filters": filters
      }
      
      json_data = controller.db_handler.search_in_database(info_to_search)
      return jsonify(json_data)
    
    # O formulário não foi submetido, renderiza a página com o formulário
    return redirect('/ad_hoc_user_account')


  # --- ADHOC REPOSITORY ---
  @app.route('/ad_hoc_repository', methods=['GET'])
  def ad_hoc_repository():
    form = AdHocRepositoryForm()
    return render_template('ad_hoc_repository.html', form=form)

  @app.route('/ad_hoc_repository/data', methods=['GET', 'POST'])
  def ad_hoc_repository_result():
    if request.method == 'POST':
      # Obtém os parâmetros da consulta do request
      table = request.args.get('table', 'Repository')
      columns = request.form.getlist('select_columns')
      filters = []
      
      if not columns:
        columns = ['repository_id', 'owner_id', 'repo_name', 'repo_full_name', 'private', 'created_at', 'updated_at', 'html_url', 'description', 'main_language']
        
      # Verifica se query_type está no corpo da solicitação POST
      query_type = request.form.get('query_type', '')
      
      if query_type == "select_by_filter":
        filters = [
          {
            "column": request.form.get('select_filter_column', ''),
            "value": request.form.get('select_filter_value', '')
          }
        ]

      # Monta o JSON info_to_search
      info_to_search = {
        "search_option": "single_table",
        "table": table,
        "columns": columns,
        "filters": filters
      }
      
      json_data = controller.db_handler.search_in_database(info_to_search)
      return jsonify(json_data)
    
    # O formulário não foi submetido, renderiza a página com o formulário
    return redirect('/ad_hoc_repository')

  
  # --- ADHOC ISSUE ---
  @app.route('/ad_hoc_issue', methods=['GET'])
  def ad_hoc_issue():
    form = AdHocIssueForm()
    return render_template('ad_hoc_issue.html', form=form)
  
  @app.route('/ad_hoc_issue/data', methods=['GET', 'POST'])
  def ad_hoc_issue_result():
    if request.method == 'POST':
      # Obtém os parâmetros da consulta do request
      table = request.args.get('table', 'Issue')
      columns = request.form.getlist('select_columns')
      filters = []
      
      if not columns:
        columns = ['issue_id', 'user_id', 'repository_id', 'title', 'created_at', 'updated_at', 'closed_at', 'labels_name']
        
      # Verifica se query_type está no corpo da solicitação POST
      query_type = request.form.get('query_type', '')
      
      if query_type == "select_by_filter":
        filters = [
          {
            "column": request.form.get('select_filter_column', ''),
            "value": request.form.get('select_filter_value', '')
          }
        ]

      # Monta o JSON info_to_search
      info_to_search = {
        "search_option": "single_table",
        "table": table,
        "columns": columns,
        "filters": filters
      }
      
      json_data = controller.db_handler.search_in_database(info_to_search)
      return jsonify(json_data)
    
    # O formulário não foi submetido, renderiza a página com o formulário
    return redirect('/ad_hoc_issue')


  # --- ADHOC PULL REQUEST ---
  @app.route('/ad_hoc_pull_request', methods=['GET'])
  def ad_hoc_pull_request():
    form = AdHocPullRequestForm()
    return render_template('ad_hoc_pull_request.html', form=form)

  @app.route('/ad_hoc_pull_request/data', methods=['GET', 'POST'])
  def ad_hoc_pull_request_result():
    if request.method == 'POST':
      # Obtém os parâmetros da consulta do request
      table = request.args.get('table', 'PullRequest')
      columns = request.form.getlist('select_columns')
      filters = []
      
      if not columns:
        columns = ['pull_request_id', 'user_id', 'repository_id', 'title', 'status', 'created_at', 'updated_at', 'body', 'closed_at', 'merged_at']
        
      # Verifica se query_type está no corpo da solicitação POST
      query_type = request.form.get('query_type', '')
      
      if query_type == "select_by_filter":
        filters = [
          {
            "column": request.form.get('select_filter_column', ''),
            "value": request.form.get('select_filter_value', '')
          }
        ]

      # Monta o JSON info_to_search
      info_to_search = {
        "search_option": "single_table",
        "table": table,
        "columns": columns,
        "filters": filters
      }
      
      json_data = controller.db_handler.search_in_database(info_to_search)
      return jsonify(json_data)
    
    # O formulário não foi submetido, renderiza a página com o formulário
    return redirect('/ad_hoc_pull_request')
  

  # --- ADHOC GIT COMMIT ---
  @app.route('/ad_hoc_git_commit', methods=['GET'])
  def ad_hoc_git_commit():
    form = AdHocGitCommitForm()
    return render_template('ad_hoc_git_commit.html', form=form)

  @app.route('/ad_hoc_git_commit/data', methods=['GET', 'POST'])
  def ad_hoc_git_commit_result():
    if request.method == 'POST':
      # Obtém os parâmetros da consulta do request
      table = request.args.get('table', 'GitCommit')
      columns = request.form.getlist('select_columns')
      filters = []
      
      if not columns:
        columns = ['commit_id', 'pull_request_id', 'repository_id', 'commit_message', 'created_at', 'html_url', 'approved_at']
        
      # Verifica se query_type está no corpo da solicitação POST
      query_type = request.form.get('query_type', '')
      
      if query_type == "select_by_filter":
        filters = [
          {
            "column": request.form.get('select_filter_column', ''),
            "value": request.form.get('select_filter_value', '')
          }
        ]

      # Monta o JSON info_to_search
      info_to_search = {
        "search_option": "single_table",
        "table": table,
        "columns": columns,
        "filters": filters
      }
      
      json_data = controller.db_handler.search_in_database(info_to_search)
      return jsonify(json_data)
    
    # O formulário não foi submetido, renderiza a página com o formulário
    return redirect('/ad_hoc_git_commit')

if __name__ == '__main__':
  controller = Controller()
  controller.start()