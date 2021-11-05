lista_fechamento=new_list=pedidos_fechados=[]
cardapio=estoque=status_mesas=pedidos=dict()
lista_comandos=['+ atualizar mesas', '+ relatorio mesas','+ atualizar cardapio','+ relatorio cardapio','+ atualizar estoque','+ relatorio estoque','+ fazer pedido','+ relatorio pedidos','+ fechar restaurante']
print('=> restaurante aberto')
def atualizar_estoque(): #armazena o estoque em um dicionario (chamado estoque) no qual as chaves são o insumo e os valores a qtd deles. ( deve ser alterado no decorrer do programa)
    global estoque
    entrada = input()
    file = open(entrada)
    for linha in file:
        linha = linha.split(',')
        if linha[0] in estoque:
            estoque[linha[0]] += int(linha[1])
        if linha[0] not in estoque:
            estoque[linha[0]] = 0
            estoque[linha[0]] = int(linha[1])
        estoque = {key: val for key, val in sorted(estoque.items(), key=lambda ele: ele[0])}
    file.close()
    return estoque

def atualizar_cardapio(): # armazena o nome do prato como a chave do dicionario e dentro da chave há outros dicionarios com a chave sendo o ingrediente e o valor sendo a qtd.

    entrada = input()
    global cardapio
    file = open(entrada)
    for linha in file:
        linha=linha.rstrip('\n')
        linha = linha.split(',')
        if linha[0] in cardapio:
            del cardapio[linha[0]]
        if linha[0] not in cardapio:
            cardapio[linha[0]] = {}
            cardapio = {key: val for key, val in sorted(cardapio.items(), key=lambda ele: ele[0])}
        for e in range(1, len(linha)):
            if linha[e] not in cardapio[linha[0]]:
                cardapio[linha[0]][linha[e]] = 0
            cardapio[linha[0]] = {key: val for key, val in sorted(cardapio[linha[0]].items(), key=lambda ele: ele[0])}
            cardapio[linha[0]][linha[e]] += 1
    file.close()
    return cardapio
def atualizar_mesas():
    global status_mesas
    entrada = input()
    file = open(entrada)
    for linha in file:
        linha = linha.rstrip('\n')
        linha = linha.rstrip(' ')
        linha = linha.split(',')
        lista_fechamento.append(linha[1])
        lista_fechamento.sort()
        if linha[1] not in status_mesas:
            status_mesas[linha[1]] = {}
            new_list.append(linha[1])
            new_list.sort()
        status_mesas = {key: val for key, val in sorted(status_mesas.items(), key=lambda ele: ele[0])}
        for area in new_list:
            if area in status_mesas:
                if linha[0] in status_mesas[area].keys():
                    del status_mesas[area][linha[0]]
        if linha[0] not in status_mesas[linha[1]]:
            status_mesas[linha[1]][linha[0]] = ''
        status_mesas[linha[1]][linha[0]] = linha[2]
        status_mesas[linha[1]] = {key: val for key, val in sorted(status_mesas[linha[1]].items(), key=lambda ele: ele[0])}
    for area in new_list:
        if area in status_mesas:
            if status_mesas[area] == {}:
                del status_mesas[area]
    return status_mesas
def relatorio_mesas():
    if status_mesas=={}:
        print('- restaurante sem mesas')
    else:
        for area in new_list:
            print(f'area:{area}')
            if area not in status_mesas:
                print('- area sem mesas')
            else:
                for mesa in status_mesas[area]:
                    print(f'- mesa: {mesa}, status:{status_mesas[area][mesa]}')
def relatorio_cardapio():
    if cardapio=={}:
        print('- cardapio vazio')
    else:
        for item in cardapio:
            print(f'item: {item}')
            for ingrediente in cardapio[item]:
                print(f'-{ingrediente}: {cardapio[item][ingrediente]}')
def relatorio_estoque():
    estoque_vazio= False
    if estoque=={} or sum(estoque.values())== 0:
        print('- estoque vazio')
    else:
        for ingrediente in estoque:
            if estoque[ingrediente] == 0:
                pass
            else:
                print(f'{ingrediente}: {estoque[ingrediente]}')
def fazer_pedido():
    nova_lista=[]
    global pedidos
    mesa_existente = False
    mesa_disponivel= False
    item_existente= False
    ingredientes_suficientes= True
    n_mesa, pedido = input().split(',')
    pedido = pedido.lstrip()
    for area in status_mesas:
        if n_mesa in status_mesas[area]: # valida se a mesa existe
            mesa_existente = True
            if status_mesas[area][n_mesa]==' ocupada': # valida se tem gente na mesa
                mesa_disponivel= True
    if mesa_existente== mesa_disponivel == True:
        if pedido in cardapio: # valida se o pedido existe
            item_existente = True
            for ingredientes in cardapio[pedido]:
                ingredientes=ingredientes.lstrip()
                if estoque=={}:
                    ingredientes_suficientes = False
                    break
                if estoque[ingredientes] < cardapio[pedido][' '+ingredientes]:
                    ingredientes_suficientes = False
    if mesa_existente == False:
        print(f'erro >> mesa {n_mesa} inexistente')
    else:
        if mesa_disponivel == False:
            print(f'erro >> mesa {n_mesa} desocupada')
        elif item_existente == False:
            print(f'erro >> item {pedido} nao existe no cardapio')
        elif ingredientes_suficientes == False or estoque=={}:
            print(f'erro >> ingredientes insuficientes para produzir o item {pedido}')
    if mesa_disponivel== mesa_existente  == item_existente == ingredientes_suficientes == True: #pedido feijo
        print(f'sucesso >> pedido realizado: item {pedido} para mesa {n_mesa}')
        if n_mesa not in pedidos:
            pedidos[n_mesa] = []
        pedidos = {key: val for key, val in sorted(pedidos.items(), key=lambda ele: ele[0])}
        pedidos[n_mesa].append(pedido)
        pedidos[n_mesa].sort()
        for item in cardapio[pedido]:
            if estoque=={}:
                break
            item = item.lstrip()
            estoque[item] -= cardapio[pedido][' ' + item]
        nova_lista.append(n_mesa)
        nova_lista.append(pedido)
        pedidos_fechados.append(nova_lista)
def relatorio_pedidos():
    if pedidos == {}:
        print('- nenhum pedido foi realizado')
    for n_mesa in pedidos:
        print(f'mesa: {n_mesa}')
        for pedido in pedidos[n_mesa]:
            print(f'- {pedido}')
def fechar_restaurante():
    if pedidos_fechados==[]:
        print('- historico vazio')
    else:
        n=1
        for lista in pedidos_fechados:
            print(f'{n}. mesa {lista[0]} pediu {lista[1]}')
            n+=1
    print('=> restaurante fechado')

comando= input()
while True:
    if comando not in lista_comandos:
        print('erro >> comando inexistente')
    if comando == '+ fechar restaurante':
        fechar_restaurante()
        break
    if comando =='+ atualizar mesas':
        status_mesas= atualizar_mesas()
    if comando =='+ atualizar cardapio':
        cardapio=atualizar_cardapio()

    if comando =='+ atualizar estoque':
        estoque=atualizar_estoque()

    if comando =='+ relatorio mesas':
        relatorio_mesas()
    if comando == '+ relatorio cardapio':
        relatorio_cardapio()
    if comando== '+ relatorio estoque':
        relatorio_estoque()
    if comando== '+ fazer pedido':
        fazer_pedido()
    if comando =='+ relatorio pedidos':
        relatorio_pedidos()
    comando=input()


