from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
# Chave secreta é essencial para a 'session' funcionar
app.secret_key = 'ADS'

# Dicionário de produtos com a lista completa e formatação correta.
produtos = {
    "lanches": [
        {"nome": "X-Burguer", "descricao": "Pão, hambúrguer e queijo.", "preco": 12.00, "imagem": "x-burguer.jpg"},
        {"nome": "X-Bacon", "descricao": "Pão, hambúrguer, queijo e bacon.", "preco": 15.00, "imagem": "x-bacon.jpg"},
        {"nome": "X-Salada", "descricao": "Pão, hambúrguer, queijo, alface e tomate.", "preco": 14.50, "imagem": "x-salada.jpg"},
        {"nome": "Tudo (lanche completo)", "descricao": "O monstro de todos os lanches.", "preco": 21.00, "imagem": "placeholder.png"}
    ],
    "salgados": [
        {"nome": "Americano", "descricao": "Salgado assado com presunto, queijo e tomate.", "preco": 13.00, "imagem": "placeholder.png"},
        {"nome": "Baguete", "descricao": "Baguete recheada.", "preco": 12.00, "imagem": "placeholder.png"},
        {"nome": "Bauru", "descricao": "Pão francês, rosbife, queijo e tomate.", "preco": 12.00, "imagem": "placeholder.png"},
        {"nome": "Pão c/ Ovo", "descricao": "Pão na chapa com ovo.", "preco": 6.90, "imagem": "placeholder.png"},
        {"nome": "Pão c/ Manteiga", "descricao": "Pão na chapa com manteiga.", "preco": 4.25, "imagem": "placeholder.png"}
    ],
    "bebidas": [
        {"nome": "Café Espresso", "descricao": "Café forte e encorpado.", "preco": 6.90, "imagem": "placeholder.png"},
        {"nome": "Refrigerante Lata 350ml", "descricao": "Coca-Cola, Guaraná, etc.", "preco": 6.90, "imagem": "placeholder.png"},
        {"nome": "Suco Natural 300ml", "descricao": "Laranja, abacaxi, morango.", "preco": 9.00, "imagem": "placeholder.png"},
        {"nome": "Água 510ml", "descricao": "Com ou sem gás.", "preco": 2.70, "imagem": "placeholder.png"}
    ],
    "bomboniere": [
        {"nome": "Kit Kat", "descricao": "Chocolate ao leite com wafer.", "preco": 6.90, "imagem": "placeholder.png"},
        {"nome": "Snickers", "descricao": "Chocolate, caramelo e amendoim.", "preco": 5.50, "imagem": "placeholder.png"},
        {"nome": "Sonho de Valsa", "descricao": "Bombom de chocolate com castanha.", "preco": 2.20, "imagem": "placeholder.png"},
        {"nome": "Trident", "descricao": "Goma de mascar sem açúcar.", "preco": 2.20, "imagem": "placeholder.png"}
    ]
}

@app.route('/')
def index():
    """ Rota da página inicial que exibe as categorias. """
    # CORREÇÃO: Alterado para 'RF01-menu.html' para corresponder ao seu nome de arquivo.
    return render_template('RF01-menu.html')

@app.route('/categoria/<nome_categoria>')
def mostrar_categoria(nome_categoria):
    """ Rota que exibe os produtos de uma categoria específica. """
    categoria = nome_categoria.lower()
    if categoria in produtos:
        return render_template('RF02-catalogo.html', categoria=categoria.capitalize(), produtos=produtos[categoria])
    return f"Categoria '{categoria}' não encontrada.", 404

@app.route('/adicionar_ao_carrinho', methods=['POST'])
def adicionar_ao_carrinho():
    """ Rota para adicionar um item ao carrinho via fetch/JavaScript. """
    dados = request.json
    nome = dados.get('nome')
    if 'carrinho' not in session:
        session['carrinho'] = {}
    carrinho = session['carrinho']
    if nome in carrinho:
        carrinho[nome]['quantidade'] += 1
    else:
        carrinho[nome] = {'nome': nome, 'preco': dados.get('preco'), 'imagem': dados.get('imagem'), 'quantidade': 1}
    session.modified = True
    return jsonify({'status': 'sucesso', 'mensagem': f'{nome} adicionado ao carrinho!'})

@app.route('/carrinho')
def ver_carrinho():
    """ Rota que exibe a página do carrinho com todos os itens. """
    carrinho = session.get('carrinho', {})
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())
    return render_template('RF03-carrinho.html', carrinho=carrinho, total=total)

@app.route('/limpar_carrinho', methods=['POST'])
def limpar_carrinho():
    """ Rota para remover todos os itens do carrinho. """
    session.pop('carrinho', None)
    return jsonify({'status': 'sucesso', 'mensagem': 'Carrinho esvaziado.'})

@app.route('/remover_item', methods=['POST'])
def remover_item():
    """ Rota para remover um item específico do carrinho. """
    dados = request.json
    nome_produto = dados.get('nome')
    if 'carrinho' in session and nome_produto in session['carrinho']:
        session['carrinho'].pop(nome_produto, None)
        session.modified = True
        return jsonify({'status': 'sucesso', 'mensagem': f'{nome_produto} removido.'})
    return jsonify({'status': 'erro', 'mensagem': 'Item não encontrado no carrinho.'}), 404

if __name__ == '__main__':
    app.run(debug=True)