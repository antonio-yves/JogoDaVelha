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
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM partida where status = 0")
	partidas = cur.fetchall()
	if 'name' in session:
		cur.execute("SELECT * FROM jogador WHERE nome = '{}'".format(session['name']))
		usuario = cur.fetchone()
		return render_template('index.html', username = usuario, partidas = partidas)
	else:
		return render_template('index.html', partidas = partidas)

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
		cur.execute("SELECT * FROM jogador")
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
		cur.execute("SELECT * FROM jogador")
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
			cur.execute("INSERT INTO jogador (nome, email, password) VALUES (%s, %s, %s)", (usuario, email, password))
			g.db.commit()
			cur.close()
			return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop('name')
	return redirect(url_for('index'))

@app.route('/partidas')
def partidas():
	if 'name' in session:
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM jogador WHERE nome = '{}'".format(session['name']))
		usuario = cur.fetchone()
		cur.execute("SELECT * FROM partida where status = 1 and id_player1 = {} or id_player2 = {}".format(usuario[0], usuario[0]))
		partidas = cur.fetchall()
		cur.execute("SELECT * FROM partida where status = 2 and (id_player1 = {} or id_player2 = {})".format(usuario[0], usuario[0]))
		partidas_fina = cur.fetchall()
		return render_template('user/partidas.html', partidas = partidas, partidas_fina = partidas_fina, username = session['name'])
	else:
		return redirect(url_for('login'))

@app.route('/criar-partida')
def criar_partida():
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM jogador")
	usuarios = cur.fetchall()
	print (usuarios)
	posicoes = []
	for x in range(9):
		posicoes.append(0)
	for user in usuarios:
		if user[1] == session['name']:
			cur.execute("INSERT INTO partida (id_player1, id_player2, winner, posicoes, jogador_atual, status) VALUES (%s, %s, %s, %s, %s, %s)", (user['id_jogador'], user['id_jogador'], user['id_jogador'], posicoes, user['id_jogador'], 0))
			cur.execute("SELECT * FROM partida WHERE id_player1 = %s and status = '0'", str(user[0]))
			partida = cur.fetchone()
			partida = str(partida[0])
		else:
			pass
	g.db.commit()
	cur.close()
	return redirect(url_for('partida', identificador = partida))

@app.route('/partida/<int:identificador>', methods = ['GET', 'POST'])
def partida(identificador):
	if 'name' in session:
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM partida where id_partida = {}".format(identificador))
		partida = cur.fetchall()
		cur.execute("SELECT * FROM jogador where nome = '{}'".format(session['name']))
		jogador1 = cur.fetchall()
		if partida[0][2] == jogador1[0][0]:
			cur.execute("SELECT * FROM jogador where id_jogador = {}".format(partida[0][1]))
			jogador2 = cur.fetchall()
		else:
			cur.execute("SELECT * FROM jogador where id_jogador = {}".format(partida[0][2]))
			jogador2 = cur.fetchall()
		if partida[0][6] == 0:
			if partida[0][2] != jogador1[0][0]:
				cur.execute("UPDATE partida SET id_player2 = {}".format(jogador1[0][0]))
				cur.execute("UPDATE partida SET status = {}".format(1))
				g.db.commit()
				cur.execute("SELECT * FROM partida where id_partida = {}".format(identificador))
				partida = cur.fetchone()
				return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2)
			else:
				return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2)
		elif partida[0][6] == 1:
			if partida[0][5] == 1:
				if request.method == 'GET':
					return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2)
				else:
					aux = request.form['resposta']
					posicoes = partida[0][4]
					posicoes[int(aux)] = 1
					cur.execute("UPDATE partida SET posicoes = ARRAY{}".format(posicoes))
					cur.execute("UPDATE partida SET jogador_atual = {}".format(partida[0][2]))
					g.db.commit()
					if posicoes[0] == 1 and posicoes[1] == 1 and posicoes[2] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[3] == 1 and posicoes[4] == 1 and posicoes[5] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[6] == 1 and posicoes[7] == 1 and posicoes[8] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[0] == 1 and posicoes[3] == 1 and posicoes[6] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[1] == 1 and posicoes[4] == 1 and posicoes[7] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[2] == 1 and posicoes[5] == 1 and posicoes[8] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[0] == 1 and posicoes[4] == 1 and posicoes[8] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[2] == 1 and posicoes[4] == 1 and posicoes[6] == 1:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					else:
						aux = 0
						for x in posicoes:
							if x != 0:
								aux += 1
							else:
								pass
						if aux == 9:
							cur.execute("UPDATE partida SET status = {}".format(2))
							g.db.commit()
							return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Velha')
						else:
							return redirect(url_for('partidas'))
					return redirect(url_for('partidas'))

			
			else:
				if request.method == 'GET':
					return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2)
				else:
					aux = request.form['resposta']
					posicoes = partida[0][4]
					posicoes[int(aux)] = 2
					cur.execute("UPDATE partida SET posicoes = ARRAY{}".format(posicoes))
					cur.execute("UPDATE partida SET jogador_atual = {}".format(partida[0][1]))
					g.db.commit()
					if posicoes[0] == 2 and posicoes[1] == 2 and posicoes[2] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[3] == 2 and posicoes[4] == 2 and posicoes[5] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[6] == 2 and posicoes[7] == 2 and posicoes[8] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[0] == 2 and posicoes[3] == 2 and posicoes[6] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[1] == 2 and posicoes[4] == 2 and posicoes[7] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[2] == 2 and posicoes[5] == 2 and posicoes[8] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[0] == 2 and posicoes[4] == 2 and posicoes[8] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					elif posicoes[2] == 2 and posicoes[4] == 2 and posicoes[6] == 2:
						cur.execute("UPDATE partida SET status = {}".format(2))
						g.db.commit()
						return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 2 venceu!')
					else:
						aux = 0
						for x in posicoes:
							if x != 0:
								aux += 1
							else:
								pass
						if aux == 9:
							cur.execute("UPDATE partida SET status = {}".format(2))
							g.db.commit()
							return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Velha')
						else:
							return redirect(url_for('partidas'))
					return redirect(url_for('partidas'))
		else:
			return render_template('game/partida-encerrada.html')
	else:
		return redirect(url_for('login'))