from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectMultipleField, StringField, widgets
from wtforms.validators import InputRequired

class MultiCheckboxFields(SelectMultipleField):
  widget = widgets.ListWidget(prefix_label=False)
  option_widget = widgets.CheckboxInput()

class AdHocUserAccountForm(FlaskForm):
  query_type = RadioField(
    u'Tipo de Consulta',
    choices = [
      ('list_all', 'Listar usuários'),
      ('select_by_filter', 'Selecionar usuário específico'),
      ('multi_table_search', 'Busca em múltiplas tabelas')
    ],
    validators = [InputRequired(message="Selecione uma opção de relatório")],
    render_kw = {'class':'no_bullets'}
  )
  
  select_columns = MultiCheckboxFields(u'Campos desejados na consulta da Tabela user_account',
    choices = [
      ('user_id', 'user_id'),
      ('user_login', 'user_login'),
      ('real_name', 'real_name'),
      ('html_url', 'html_url'),
      ('avatar_url', 'avatar_url')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_column = RadioField(u'Deseja acessar o usuário por qual campo?',
    choices = [
      ('user_id', 'user_id'),
      ('user_login', 'user_login'),
      ('real_name', 'real_name')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_value = StringField(u'Digite o valor que deseja')
  
  table = StringField(u'Table', default='UserAccount')  # Adiciona um campo para a tabela com valor padrão
  submit = SubmitField('Buscar')

class AdHocRepositoryForm(FlaskForm):
  query_type = RadioField(
    u'Tipo de Consulta',
    choices = [
      ('list_all', 'Listar repositórios'),
      ('select_by_filter', 'Selecionar repositório específico'),
      ('multi_table_search', 'Busca em múltiplas tabelas')
    ],
    validators = [InputRequired(message="Selecione uma opção de relatório")],
    render_kw = {'class':'no_bullets'}
  )
  
  select_columns = MultiCheckboxFields(u'Campos desejados na consulta da Tabela repository',
    choices = [
      ('repository_id', 'repository_id'),
      ('owner_id', 'owner_id'),
      ('repo_name', 'repo_name'),
      ('repo_full_name', 'repo_full_name'),
      ('private', 'private'),
      ('created_at', 'created_at'),
      ('updated_at', 'updated_at'),
      ('html_url', 'html_url'),
      ('description', 'description'),
      ('main_language', 'main_language')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_column = RadioField(u'Deseja acessar o repositório por qual campo?',
    choices = [
      ('repository_id', 'repository_id'),
      ('repo_name', 'repo_name'),
      ('repo_full_name', 'repo_full_name'),
      ('main_language', 'main_language')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_value = StringField(u'Digite o valor que deseja')
  
  table = StringField(u'Table', default='Repository')  # Adiciona um campo para a tabela com valor padrão
  submit = SubmitField('Buscar')

class AdHocIssueForm(FlaskForm):
  query_type = RadioField(
    u'Tipo de Consulta',
    choices = [
      ('list_all', 'Listar issues'),
      ('select_by_filter', 'Selecionar issue específica'),
      ('multi_table_search', 'Busca em múltiplas tabelas')
    ],
    validators = [InputRequired(message="Selecione uma opção de relatório")],
    render_kw = {'class':'no_bullets'}
  )
  
  select_columns = MultiCheckboxFields(u'Campos desejados na consulta da Tabela issue',
    choices = [
      ('issue_id', 'issue_id'),
      ('user_id', 'user_id'),
      ('repository_id', 'repository_id'),
      ('title', 'title'),
      ('created_at', 'created_at'),
      ('updated_at', 'updated_at'),
      ('closed_at', 'closed_at'),
      ('labels_name', 'labels_name')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_column = RadioField(u'Deseja acessar a issue por qual campo?',
    choices = [
      ('issue_id', 'issue_id'),
      ('title', 'title'),
      ('repository_id', 'repository_id')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_value = StringField(u'Digite o valor que deseja')
  
  table = StringField(u'Table', default='Issue')  # Adiciona um campo para a tabela com valor padrão
  submit = SubmitField('Buscar')

class AdHocPullRequestForm(FlaskForm):
  query_type = RadioField(
    u'Tipo de Consulta',
    choices = [
      ('list_all', 'Listar pull requests'),
      ('select_by_filter', 'Selecionar pull request específica'),
      ('multi_table_search', 'Busca em múltiplas tabelas')
    ],
    validators = [InputRequired(message="Selecione uma opção de relatório")],
    render_kw = {'class':'no_bullets'}
  )
  
  select_columns = MultiCheckboxFields(u'Campos desejados na consulta da Tabela pull_request',
    choices = [
      ('pull_request_id','pull_request_id'),
      ('user_id','user_id'),
      ('repository_id','repository_id'),
      ('title','title'),
      ('status','status'),
      ('created_at','created_at'),
      ('updated_at','updated_at'),
      ('body','body'),
      ('closed_at','closed_at'),
      ('merged_at','merged_at')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_column = RadioField(u'Deseja acessar a pull request por qual campo?',
    choices = [
      ('pull_request_id','pull_request_id'),
      ('title','title'),
      ('status','status'),
      ('repository_id','repository_id')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_value = StringField(u'Digite o valor que deseja')
  
  table = StringField(u'Table', default='PullRequest')  # Adiciona um campo para a tabela com valor padrão
  submit = SubmitField('Buscar')

class AdHocGitCommitForm(FlaskForm):
  query_type = RadioField(
    u'Tipo de Consulta',
    choices = [
      ('list_all', 'Listar commits'),
      ('select_by_filter', 'Selecionar commit específica'),
      ('multi_table_search', 'Busca em múltiplas tabelas')
    ],
    validators = [InputRequired(message="Selecione uma opção de relatório")],
    render_kw = {'class':'no_bullets'}
  )
  
  select_columns = MultiCheckboxFields(u'Campos desejados na consulta da Tabela git_commit',
    choices = [
      ('commit_id', 'commit_id'),
      ('pull_request_id', 'pull_request_id'),
      ('repository_id', 'repository_id'),
      ('commit_message', 'commit_message'),
      ('created_at', 'created_at'),
      ('html_url', 'html_url'),
      ('approved_at', 'approved_at')
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_column = RadioField(u'Deseja acessar a commit por qual campo?',
    choices = [
      ('commit_id', 'commit_id'),
      ('pull_request_id', 'pull_request_id'),
      ('repository_id', 'repository_id')      
    ],
    render_kw = {'class':'no_bullets'}
  )
  
  select_filter_value = StringField(u'Digite o valor que deseja')
  
  table = StringField(u'Table', default='GitCommit')  # Adiciona um campo para a tabela com valor padrão
  submit = SubmitField('Buscar')