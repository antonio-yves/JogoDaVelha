def verificar_ganhador(posicoes, cur, partida, jogador1, jogador2, jogador_atual):
	aux = 0
	for x in posicoes:
		if x != 0:
			aux += 1
		else:
			pass
	if aux == 9:
		if posicoes[0] == jogador_atual and posicoes[1] == jogador_atual and posicoes[2] == jogador_atual:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		elif posicoes[3] == 1 and posicoes[4] == 1 and posicoes == [5]:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		elif posicoes[6] == 1 and posicoes[7] == 1 and posicoes == [8]:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		elif posicoes[0] == 1 and posicoes[3] == 1 and posicoes == [6]:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		elif posicoes[1] == 1 and posicoes[4] == 1 and posicoes == [7]:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		elif posicoes[2] == 1 and posicoes[5] == 1 and posicoes == [8]:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		elif posicoes[0] == 1 and posicoes[4] == 1 and posicoes == [8]:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		elif posicoes[2] == 1 and posicoes[4] == 1 and posicoes == [6]:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Jogador 1 venceu!')
		else:
			cur.execute("UPDATE partida SET status = {}".format(2))
			g.db.commit()
			return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2, mensagem = 'Velha')
	else:
		return render_template('game/partida.html', partida = partida, jogador1 = jogador1, jogador2 = jogador2)