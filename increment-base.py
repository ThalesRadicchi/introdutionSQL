import random
import psycopg2
from faker import Faker
from faker.providers import person, address

fake = Faker()
fake.add_provider(person)
fake.add_provider(address)


# Configuração da conexão com o banco de dados PostgreSQL
with psycopg2.connect(
    dbname="portfolio",
    user="Thales",
    password="123",
    host="localhost",
    port="5432"
) as conn:
    # Criação do cursor
    with conn.cursor() as cursor:
        
# Usuario

        try:
            for _ in range(20000):
                nome = fake.name()
                idade = fake.random_int(min=18, max=99)
                email = fake.email()
                logradouro = fake.street_address()
                cidade = fake.city()
                bairro = fake.random_element(elements=('Centro', 'Bairro A', 'Bairro B'))
                cpf = fake.unique.random_number(digits=11)
                ataniver = fake.date_of_birth(minimum_age=18, maximum_age=99)

                cursor.execute("""INSERT INTO usuario (nome, idade, email, logradouro, cidade, bairro, cpf, ataniver)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (nome, idade, email, logradouro, cidade, bairro, cpf, ataniver))
        except Exception as e:
            print("Valor do usuário erro: ", e)

# Produto

        try:

            cursor.execute("""INSERT INTO produto (nome, descricao, valor)
                            VALUES ('Gelardeira', 'Muito espaço interno e tecnologias para o armazenamento perfeito dos alimentos: o Refrigerador Four Door da Crissair é ideal para grandes projetos de cozinha gourmet.
                            Com capacidade total de 518 litros, sendo 367 litros no refrigerador e 151 litros no freezer, o Refrigerador Four Door RFD 540 traz tecnologias como Dual Cooling System que ajuda na preservação dos alimentos, motor compressor com tecnologia inverter, freezer NO-FROST e ainda iluminação interna em LED, gerando menos calor e mais economia de energia.
                            No design, acabamento em aço inox, comando touch e estilo french door com quatro portas, trazendo estilo e praticidade na hora de manusear os alimentos.
                            Compre aqui seu Refrigerador Crissair RFD 540!' , 5000.00),
                            ('Fogao', 'O Fogão de Piso 4 Bocas Bali da Esmaltec é perfeito para o preparo de deliciosas refeições na sua cozinha. 
                            Produzido em aço inox de alta qualidade, possui acendimento manual e forno limpa fácil com porta de vidro que oferece melhor
                            visibilidade dos alimentos durante o cozimento. As grades duplas e os botões são removíveis e por isso facilitam a limpeza do
                            produto. Possui queimador família que oferece maior rapidez no preparo dos alimentos.', '1050.00'),
                            ('Microondas', 'ANTIBACTERIA AG O ST67L inibe 99,9 da proliferação das bactérias*, pois tem em seu interior o novo revestimento com camada de
                            tinta com sistema antimicrobiano., DUPLA REFEIÇÃO Sabe quando você vai almoçar com alguém e precisa esperar um prato ficar
                            pronto para esquentar o outro? A Dupla Refeição foi criada para resolver situações como essa. Com uma grelha removível, a 
                            função pode ser ativada para aquecer 300g, 500g e 700g (peso total das duas porções) em pratos diferentes. Para aproveitar,
                            basta colocar uma refeição no prato giratório e outra na grelha., DESIGN SOFISTICADO Agora a linha está ainda mais moderna
                            e sofisticada, com um novo painel., PEGA FÁCIL Sabe quando você vai aquecer algo em uma xícara e, quando o micro-ondas para
                            , ela está no fundo do aparelho, com a asa virada para trás? É um dos problemas que a tecnologia Pega Fácil resolve para você
                            . Assim que o aquecimento termina, o prato faz uma rotação para que você pegue o utensílio exatamente onde o deixou.', '568.28')""")
        except Exception as e:
            if conn:
                conn.rollback()
            print("Valor do usuário erro: ", e)

# Loja

        try:
            nome = list(('Log', 'Logistic', 'TFLogi', 'LogisticAu', 'Vertente', 'LogArt', 'LogisticsV'))
            for i in range(7):
                gerente = fake.name()
                logradouro = fake.street_address()
                cidade = fake.city()
                bairro = fake.random_element(elements=('Centro', 'Bairro A', 'Bairro B'))

                cursor.execute("""INSERT INTO loja (nome, gerente, logradouro, cidade, bairro)
                               VALUES (%s, %s, %s, %s, %s)""", (nome[i], gerente, logradouro, cidade, bairro))
        except Exception as e:
            print("Valor do usuário erro: ", e)

# Transportadoras

        try:
            nome = list(('Transp', 'Veliz'))
            for i in range(2):                
                cidade = fake.city()
                cursor.execute("""INSERT INTO transportadoras (nome, cidade, situacao)
                                VALUES (%s, %s, %s)""", (nome[i], cidade, 'A'))
        except Exception as e:
            print("Valor do usuário erro: ", e)

# Pedidos
        try:
            cursor.execute("SELECT COUNT(*) FROM usuario")
            countUsuario = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM transportadoras")
            countTransportadora = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM loja")
            countLoja = cursor.fetchone()[0]

            for _ in range(20000):
                usuario = fake.random_int(min=1, max=countUsuario)
                transportadora = fake.random_int(min=1, max=countTransportadora)
                loja = fake.random_int(min=1, max=countLoja)
                data = fake.date_of_birth(minimum_age=0, maximum_age=5)

                cursor.execute("""INSERT INTO pedidos (idUsuario, idTransportadora, idLoja, dataped)
                                VALUES (%s, %s, %s, %s)""", (usuario, transportadora, loja, data))
        except Exception as e:
            print("Valor do usuário erro: ", e)


# produto_Pedido
        cursor.execute("SELECT idPedido FROM pedidos")
        validadoridPedido = [item[0] for item in cursor.fetchall()]

        cursor.execute("SELECT COUNT(*) FROM produto")
        produto = cursor.fetchone()[0]

        cursor.execute("SELECT valor FROM produto")
        valor_produto = cursor.fetchall()

        try:
            for index in range(1, len(validadoridPedido) + 1):
                print(index)

                if index not in validadoridPedido:
                    print(index - 1, validadoridPedido[index])
                    indexinue

                idProduto_valor = fake.random_int(min=1, max=produto[0])
                quantidade = fake.random_int(min=1, max=10)
                valortotal = quantidade * int(valor_produto[idProduto_valor - 1][0])

                cursor.execute("""INSERT INTO produto_Pedidos (idPedido, idProduto, quantidade, valorTotal)
                               VALUES (%s, %s, %s, %s)""", (index - 1, idProduto_valor, quantidade, valortotal))            
        except Exception as e:
            print("A excessão é: ", e)


# transacoes (idTransacao, formaPagamento, dataTran, valorMkt, valorLojas, valorTrans, idPedido)

        cursor.execute("SELECT idPedido, dataped FROM pedidos")
        dataIdPedido = cursor.fetchall()
        countUsuario = [item[0] for item in dataIdPedido] 

        cursor.execute("SELECT valorTotal FROM produto_pedidos")
        valorPdd = [item[0] for item in cursor.fetchall()]

        try:
            for index in range(0, len(countUsuario)):
               
                formaPagamento = random.choice(['P', 'C', 'D', 'M'])
                
                valorMkt = float(valorPdd[index]) * .2 
                valorLojas = float(valorPdd[index]) * .8 

                cursor.execute("""INSERT INTO transacoes (formaPagamento, dataTran, valorMkt, valorLojas, valorTrans, idPedido)
                               VALUES (%s, %s, %s, %s, %s, %s)""", (formaPagamento, dataIdPedido[index][1] , valorMkt, valorLojas, valorPdd[index] , dataIdPedido[index][0]))

        except Exception as e:
            print("A excessão é: ", e)
