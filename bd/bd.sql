CREATE DATABASE JOGO;

CREATE TABLE JOGADOR(
	id_jogador serial,
	nome varchar(10),
	email varchar(70),
	password varchar(8),
	vitorias integer,
	derrotas integer,
	primary key(id_jogador)
);

CREATE TABLE PARTIDA(
	id_partida serial,
	id_player1 integer,
	id_player2 integer,
	winner integer,
	posicoes integer[9],
	jogador_atual integer,
	status integer,
	primary key(id_partida),
	foreign key(id_player1) references JOGADOR (id_jogador),
	foreign key(id_player2) references JOGADOR (id_jogador),
	foreign key(winner) references JOGADOR (id_jogador)
);