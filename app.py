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
    ''', [num_id]).fetchone()

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

    empreendedores = db.execute('''
      SELECT empreendedor_id, nome 
      FROM empreendedor
      WHERE projeto_id  = ?;
    ''', [num_id]).fetchall()

    investimentos = db.execute('''
      SELECT * 
      FROM investimento
      WHERE projeto_id  = ?;
    ''', [num_id]).fetchall()
    return render_template('projeto.html', empreendedor=empreendedores, projeto=projetos, investimento= investimentos)

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

@APP.route('/investimentos')
def list_investimentos():
    investimentos = db.execute('''
      SELECT shark_id, projeto_id, valor_do_investimento, porcentagem_vendida_do_projeto
      FROM investimento
      ORDER BY projeto_id, shark_id;         
      ''' ).fetchall()
    return render_template('investimento-list.html', investimento=investimentos)

@APP.route('/investimentos/<int:id_projeto>/<int:id_shark>')
def view_investments_by_ids(id_projeto, id_shark):
    num_id_projeto = int(id_projeto)
    num_id_shark = int(id_shark)

    projetos = db.execute('''
      SELECT projeto_id, nome
      FROM projeto
      WHERE projeto_id = ?;
    ''', [num_id_projeto]).fetchone()

    sharks = db.execute('''
      SELECT shark_id, nome
      FROM shark
      WHERE shark_id = ?
      ORDER BY shark_id;
    ''', [num_id_shark]).fetchone()

    if projetos is None:
        abort(404, 'ID do projeto {} não existe .'.format(num_id_projeto))

    if sharks is None:
        abort(404, 'ID do shark {} não existe .'.format(num_id_shark))    

    investimentos = db.execute('''
      SELECT projeto_id, shark_id, valor_do_investimento, porcentagem_vendida_do_projeto 
      FROM investimento
      WHERE projeto_id = ? AND shark_id = ?
      ORDER BY projeto_id, shark_id;
    ''', [num_id_projeto, num_id_shark]).fetchone()

    if investimentos is None:
      abort(404, 'ID do investimento {} não existe .'.format(str({num_id_projeto} +'/' + {num_id_shark})))

    return render_template('investimento.html', investimento=investimentos, projeto=projetos, shark=sharks)

@APP.route('/investimentos/search/<expr>/')
def search_investimento(expr):
    temp = int(expr)
    integer = '%' + int(expr) + '%'
    search = {'response': temp }
    investimentos = db.execute(''' 
      SELECT shark_id, projeto_id, valor_do_investimento, porcentagem_vendida_do_projeto
      FROM investimento
      WHERE valor_do_investimento LIKE ?;
    ''',[integer]).fetchall()
    return render_template('projeto-search.html', search=search, investimento=investimentos)

@APP.route('/episodios')
def list_episodios():
    episodios = db.execute('''
        SELECT numero_do_episodio, temporada
        FROM episodio
        ORDER BY numero_do_episodio;
    ''').fetchall()
    return render_template('episodio-list.html', episodio=episodios)

@APP.route('/episodios/<int:id>/')
def view_episodes_by_id(id):
    num_id = int(id)
    episodios = db.execute('''
      SELECT numero_do_episodio, temporada
      FROM episodio
      WHERE numero_do_episodio = ?
      ORDER BY numero_do_episodio;
    ''', [num_id]).fetchone()

    projetos = db.execute('''
      SELECT *
      FROM projeto
      WHERE numero_do_episodio = ?
      ORDER BY projeto_id;
    ''', [num_id]).fetchall()

    sharks = db.execute('''
    SELECT *
    FROM shark s 
    join episodio_shark es on s.shark_id = es.shark_id
    WHERE es.numero_do_episodio = ?
    ''', [num_id]).fetchall()

    if episodios is None:
        abort(404, 'ID do episodio {} não existe .'.format(num_id))

    return render_template('episodio.html', episodio=episodios, projeto = projetos, shark = sharks)

@APP.route('/episodios/temporada/<int:id>/')
def view_episodes_by_season(id):
    num_id = int(id)
    episodios = db.execute('''
      SELECT numero_do_episodio, temporada
      FROM episodio
      WHERE temporada = ?
      ORDER BY numero_do_episodio;
    ''', [num_id]).fetchone()

    if episodios is None:
        abort(404, 'ID do episodio {} não existe .'.format(num_id))

    return render_template('episodio-season.html', episodio=episodios)

@APP.route('/sharks')
def list_shark():
    sharks = db.execute('''
      SELECT shark_id, nome
      FROM shark
      ORDER BY shark_id;
    ''').fetchall()
    return render_template('shark-list.html', shark=sharks)

@APP.route('/sharks/<int:id>/')
def view_episodes_by_shark(id):
    num_id = int(id)
    sharks = db.execute('''
      SELECT nome
      FROM shark
      WHERE shark_id = ?
      ORDER BY shark_id;
    ''', [num_id]).fetchone()

    if sharks is None:
        abort(404, 'ID do shark {} não existe .'.format(num_id))

    episodios = db.execute('''
      SELECT e.numero_do_episodio, temporada
      FROM episodio e NATURAL JOIN episodio_shark es
      WHERE es.shark_id = ?;
    ''', [num_id]).fetchall()

    investimentos = db.execute('''
    SELECT * 
    FROM investimento
    WHERE shark_id  = ?;
    ''', [num_id]).fetchall()
    return render_template('shark.html', episodio=episodios, shark=sharks, investimento = investimentos)

@APP.route('/sharks/search/<expr>/')
def search_shark(expr):
    temp = str(expr)
    string = '%' + str(expr) + '%'
    search = {'response': temp }
    sharks = db.execute(''' 
      SELECT nome
      FROM shark
      WHERE nome LIKE ?;
    ''',[string]).fetchall()
    return render_template('shark-search.html', search=search, shark=sharks)