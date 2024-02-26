import random
import psycopg2
from faker import Faker
from faker.providers import person, address

fake = Faker()
fake.add_provider(person)
fake.add_provider(address)

# Configuração da conexão com o banco de dados PostgreSQL
try:
    with psycopg2.connect(
        dbname="portfolio",
        user="Thales",
        password="123",
        host="localhost",
        port="5432"
    ) as conn:
        # Criação do cursor
        with conn.cursor() as cursor:

            # Usuário
            try:
                for _ in range(20000):

                    nome = fake.name()
                    idade = fake.random_int(min=18, max=99)
                    email = fake.email()
                    logradouro = fake.street_address()
                    cidade = fake.city()
                    bairro = fake.random_element(elements=('Centro', 'Bairro A', 'Bairro B'))
                    # Usando uuid para CPF, garantindo a unicidade
                    cpf = fake.unique.random_number(digits=11)
                    ataniver = fake.date_of_birth(minimum_age=18, maximum_age=99)

                    cursor.execute("""INSERT INTO usuario (nome, idade, email, logradouro, cidade, bairro, cpf, ataniver)
                                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                      """, (nome, idade, email, logradouro, cidade, bairro, cpf, ataniver))
            except Exception as e:
                print("Erro ao inserir usuário: ", e)

            # Produto
            try:
                # Usando executemany para inserir vários registros em uma única query
                produtos = [
                    ('Geladeira', 'Descrição da geladeira.', 5000.00),
                    ('Fogão', 'Descrição do fogão.', 1050.00),
                    ('Microondas', 'Descrição do microondas.', 568.28)
                ]
                cursor.executemany("""INSERT INTO produto (nome, descricao, valor)
                                     VALUES (%s, %s, %s)""", produtos)
            except Exception as e:
                if conn:
                    conn.rollback()
                print("Erro ao inserir produtos: ", e)

#             # Loja
            try:
                nomes_lojas = ['Log', 'Logistic', 'TFLogi', 'LogisticAu', 'Vertente', 'LogArt', 'LogisticsV']
                for nome in nomes_lojas:
                    gerente = fake.name()
                    logradouro = fake.street_address()
                    cidade = fake.city()
                    bairro = fake.random_element(elements=('Centro', 'Bairro A', 'Bairro B'))

                    cursor.execute("""INSERT INTO loja (nome, gerente, logradouro, cidade, bairro)
                                   VALUES (%s, %s, %s, %s, %s)""", (nome, gerente, logradouro, cidade, bairro))
            except Exception as e:
                print("Erro ao inserir lojas: ", e)

            # Transportadoras
            try:
                nomes_transportadoras = ['Transp', 'Veliz']
                for nome in nomes_transportadoras:
                    cidade = fake.city()
                    cursor.execute("""INSERT INTO transportadoras (nome, cidade, situacao)
                                    VALUES (%s, %s, %s)""", (nome, cidade, 'A'))
            except Exception as e:
                print("Erro ao inserir transportadoras: ", e)

            # Pedidos
            try:
                cursor.execute("SELECT COUNT(*) FROM usuario")
                count_usuario = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM transportadoras")
                count_transportadora = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM loja")
                count_loja = cursor.fetchone()[0]

                for _ in range(20000):
                    usuario = fake.random_int(min=1, max=count_usuario)
                    transportadora = fake.random_int(min=1, max=count_transportadora)
                    loja = fake.random_int(min=1, max=count_loja)
                    data = fake.date_of_birth(minimum_age=0, maximum_age=5)


                    cursor.execute("""INSERT INTO pedidos (idUsuario, idTransportadora, idLoja, dataped)
                                    VALUES (%s, %s, %s, %s)""", (usuario, transportadora, loja, data))
            except Exception as e:
                print("Erro ao inserir pedidos: ", e)

#             # Produto_Pedido
            try:
                cursor.execute("SELECT idPedido FROM pedidos")
                validador_id_pedido = [item[0] for item in cursor.fetchall()]

                cursor.execute("SELECT COUNT(*) FROM produto")
                count_produto = cursor.fetchone()[0]

                cursor.execute("SELECT valor FROM produto")
                valor_produto = [item[0] for item in cursor.fetchall()]

                for index in range(0, len(validador_id_pedido)):

                    if index + 1 not in validador_id_pedido:
                        continue

                    id_produto_valor = fake.random_int(min=1, max=count_produto)
                    quantidade = fake.random_int(min=1, max=10)
                    valor_total = quantidade * int(valor_produto[id_produto_valor - 1])

                    cursor.execute("""INSERT INTO produto_Pedidos (idPedido, idProduto, quantidade, valorTotal)
                                   VALUES (%s, %s, %s, %s)""", ((index + 1), id_produto_valor, quantidade, valor_total))
            except Exception as e:
                print("Erro ao inserir produto_pedido: ", e)

#             # Transacoes
            try:
                cursor.execute("SELECT idPedido, dataped FROM pedidos")
                data_id_pedido = cursor.fetchall()
                valor_pdd = [item[0] for item in cursor.fetchall()]

                cursor.execute("SELECT valorTotal FROM produto_pedidos")
                valor_pdt_pdd = [item[0] for item in cursor.fetchall()]

                for index in range(0, len(data_id_pedido)):

                    forma_pagamento = random.choice(['P', 'C', 'D', 'M'])
                    valor_mkt = float(valor_pdt_pdd[index]) * 0.2
                    valor_lojas = float(valor_pdt_pdd[index]) * 0.8

                    cursor.execute("""INSERT INTO transacoes (formaPagamento, dataTran, valorMkt, valorLojas, valorTrans, idPedido)
                                   VALUES (%s, %s, %s, %s, %s, %s)""", (forma_pagamento, data_id_pedido[index][1], valor_mkt,
                                                                     valor_lojas, valor_pdt_pdd[index], data_id_pedido[index][0]))

            except Exception as e:
                print("Erro ao inserir transacoes: ", e)

except psycopg2.Error as e:
    print("Erro ao conectar ao PostgreSQL:", e)
                
