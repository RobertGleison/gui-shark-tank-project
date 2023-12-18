import db
import logging
from flask import abort, render_template, Flask
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

APP = Flask(__name__)

@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
       SELECT * FROM (SELECT COUNT(*) n_empreendedores FROM empreendedor) JOIN
      (SELECT COUNT(*) n_projetos FROM projeto) JOIN
      (SELECT COUNT(*) n_investimentos FROM investimento) JOIN 
      (SELECT COUNT(*) n_episodios FROM episodio) JOIN 
      (SELECT COUNT(*) n_sharks FROM shark);
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html', stats=stats)

@APP.route('/empreendedores')
def list_empreendedores():
    empreendedores = db.execute('''
      SELECT empreendedor_id, nome, genero, projeto_id
      FROM empreendedor
      ORDER BY nome;
    ''').fetchall()
    return render_template('empreendedor-list.html', empreendedor=empreendedores)

@APP.route('/empreendedores/<int:id>/')
def view_projects_by_empreeendedor(id):
    num_id = int(id)
    empreendedores = db.execute('''
      SELECT empreendedor_id, nome, genero, projeto_id
      FROM empreendedor
      WHERE empreendedor_id = ?;
    ''', [num_id]).fetchone()
    
    if empreendedores is None:
        abort(404, 'ID do empreendedor {} não existe .'.format(num_id))
  
    projetos = db.execute('''
      SELECT p.projeto_id, p.nome, p.website, p.valor_de_mercado, p.categoria, p.descricao, p.numero_do_episodio
      FROM projeto p
      INNER JOIN empreendedor e ON p.projeto_id = e.projeto_id
      WHERE e.empreendedor_id = ?
      ORDER BY p.nome;
    ''', [num_id]).fetchall()
    return render_template('empreendedor.html', empreendedor=empreendedores, projeto=projetos)

@APP.route('/empreendedores/search/<expr>/')
def search_empreendedor(expr):
    temp = str(expr)
    string = '%' + str(expr) + '%'
    search = {'response': temp }
    empreendedores = db.execute(
        ''' 
    SELECT empreendedor_id, nome, genero, projeto_id
    FROM empreendedor 
    WHERE nome LIKE ?;
    ''',[string]).fetchall()
    return render_template('empreendedor-search.html', search=search, empreendedor=empreendedores)

@APP.route('/projetos')
def list_projetos():
    projetos = db.execute('''
      SELECT projeto_id, nome, website, valor_de_mercado, categoria, descricao, numero_do_episodio
      FROM projeto
      ORDER BY projeto_id;
    ''').fetchall()
    return render_template('projeto-list.html', projeto=projetos)

@APP.route('/projetos/<int:id>/')
def view_episodes_by_project(id):
    num_id = int(id)
    projetos = db.execute('''
      SELECT projeto_id, nome, website, valor_de_mercado,
      categoria, descricao, numero_do_episodio
      FROM projeto
      WHERE projeto_id = ?
      ORDER BY projeto_id;
    ''', [num_id]).fetchone()

    if projetos is None:
        abort(404, 'ID do projeto {} não existe .'.format(num_id))

    episodios = db.execute('''
      SELECT numero_do_episodio, temporada 
      FROM episodio
      WHERE numero_do_episodio = ?;
    ''', [num_id]).fetchall()
    return render_template('projeto.html', episodio=episodios, projeto=projetos)

@APP.route('/projetos/search/<expr>/')
def search_projeto(expr):
    temp = str(expr)
    string = '%' + str(expr) + '%'
    search = {'response': temp }
    projetos = db.execute(''' 
      SELECT projeto_id, nome, website, valor_de_mercado,
      categoria, descricao, numero_do_episodio
      FROM projeto
      WHERE nome LIKE ?;
    ''',[string]).fetchall()
    return render_template('projeto-search.html', search=search, projeto=projetos)
