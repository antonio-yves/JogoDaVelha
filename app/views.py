from flask import g, session, request, redirect, url_for, render_template
from app import app
import psycopg2
import psycopg2.extras

@app.before_request
def before_request():
   g.db = psycopg2.connect("dbname=jogo user=postgres password=sousa123 host=127.0.0.1")

# Disconnect database
@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def index():
	if 'name' in session:
		usuario = session['name']
		return render_template('index.html', username = usuario)
	else:
		return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		if 'name' in session:
			return redirect(url_for('index'))
		else:
			return render_template('user/login.html')
	else:
		usuario = request.form['id_username']
		password = request.form['id_password']
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM usuario")
		usuarios = cur.fetchall()
		aux = 0
		for user in usuarios:
			if user['nome'] == usuario and user['password'] == password:
				session['name'] = user['nome']
				return redirect(url_for('index'))
			elif user['nome'] == usuario and user['password'] != password:
				return render_template('user/login.html', error='Senha incorreta!')
			else:
				pass
		return render_template('user/login.html', error='Usuário não encontrado!')

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
	if request.method == 'GET':
		if 'name' in session:
			return redirect(url_for('index'))
		else:
			return render_template('user/cadastro.html')
	else:
		usuario = request.form['id_usuario']
		email = request.form['id_email']
		password = request.form['id_password']
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM usuario")
		usuarios = cur.fetchall()
		aux = 0
		for user in usuarios:
			if user['nome'] == usuario:
				aux = 1
			else:
				pass
		if aux == 1:
			return render_template('user/cadastro.html', error='Usuário já cadastrado, escolha outro nome de usuário!')
		else:
			cur.execute("INSERT INTO usuario (nome, email, password) VALUES (%s, %s, %s)", (usuario, email, password))
			g.db.commit()
			cur.close()
			return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop('name')
	return redirect(url_for('index'))

@app.route('/partida')
def partida():
	return render_template('game/partida.html')


