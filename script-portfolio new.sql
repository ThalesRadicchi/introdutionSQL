CREATE TABLE usuario (
	idUsuario SERIAL PRIMARY KEY, 
	nome VARCHAR(50) NOT NULL,
	idade INTEGER,
	email VARCHAR(50) NOT NULL,
	logradouro VARCHAR(100) NOT NULL,
	cidade VARCHAR(50) NOT NULL,
	bairro VARCHAR(50),
	cpf INTEGER NOT NULL,
	ataniver DATE NOT NULL
)

CREATE TABLE produto (
	idProduto SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	descricao TEXT NOT NULL,
	valor DECIMAL(10,2) NOT NULL
)

CREATE TABLE loja (
	idLoja SERIAL PRIMARY KEY,
	nome VARCHAR(50) NOT NULL,
	gerente VARCHAR(50) NOT NULL,
	logradouro VARCHAR(100),
	cidade VARCHAR(50), 
	bairro VARCHAR(50)
)

CREATE TABLE transportadora (
	idTransportadora SERIAL PRIMARY KEY,
	nome VARCHAR(50) NOT NULL,
	cidade VARCHAR(50) NOT NULL,
	situacao CHAR(1) NOT NULL
)

CREATE TABLE pedidos (
	idPedido SERIAL PRIMARY KEY,
	idUsuario INTEGER NOT NULL,
	idTransportadora INTEGER NOT NULL,
	idLoja INTEGER NOT NULL, 
	dataPed DATE NOT NULL,

	CONSTRAINT fk_pedido_loja FOREIGN KEY (idLoja) REFERENCES loja(idLoja),
	CONSTRAINT fk_pedido_transportadora FOREIGN KEY (idTransportadora) REFERENCES transportadora(idTransportadora),
	CONSTRAINT fk_pedido_usuario FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
)

CREATE TABLE produto_Pedidos (
	idPedido INTEGER NOT NULL,
	idProduto INTEGER NOT NULL,
	quantidade INTEGER NOT NULL,
	valorTotal DECIMAL(10,2),

	CONSTRAINT fk_prodped_pedido FOREIGN KEY (idPedido) REFERENCES pedidos(idPedido),
	CONSTRAINT fk_prodped_produto FOREIGN KEY (idProduto) REFERENCES produto(idProduto)
)

CREATE TABLE transacoes (
	idTransacao SERIAL PRIMARY KEY,
	formaPagamento CHAR(1) NOT NULL,
	dataTran DATE NOT NULL,
	valorMKT DECIMAL(10,2) NOT NULL,
	valorLojas DECIMAL(10,2) NOT NULL,
	valorTrans DECIMAL(10,2) NOT NULL,
	idPedido INTEGER NOT NULL,

	CONSTRAINT fk_transacoes_pedido FOREIGN KEY (idPedido) REFERENCES idPedido(idPedido)
)