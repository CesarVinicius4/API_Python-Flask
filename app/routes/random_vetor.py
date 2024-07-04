from flask import jsonify, request, send_file
from app.routes import bp
import random
import matplotlib.pyplot as plt
from io import BytesIO

@bp.route('/vetor', methods=['POST'])
def vetor():
    try:
        data = request.get_json()
        vector = data['vetor']
        # Caso tenha sido passado algum vetor com o nome "vetor", apliquei a lógica de organização de Insertion sort
        for i in range(1, len(vector)):
            key = vector[i]
            j = i - 1
            while j >= 0 and key < vector[j]:
                vector[j + 1] = vector[j]
                j -= 1
            vector[j + 1] = key
        return jsonify({'vetor': vector})
    except Exception as e:
        #Se não foi passado, gera um vetor randomizado de 50 mil valores.
        vector = []
        for _ in range(50000):
            random_number = random.randint(0, 100000)
            vector.append(random_number)

        n = len(vector)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            vector[i], vector[j] = vector[j], vector[i]

        return jsonify({'vetor': vector})

@bp.route('/scatter_plot', methods=['POST'])
def scatter_plot():

    data = request.get_json()

    if not data or 'x' not in data or 'y' not in data:
        return jsonify({'Error': 'Bad Request'})

    eixo_x = data['x']
    eixo_y = data['y']

    # Comando para criar o gráfico de dispersão usando Matplotlib
    plt.scatter(eixo_x, eixo_y)

    # Salva o gráfico em um buffer de BytesIO, que serve para manipular dados em memória, como imagens.
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    plt.close()

    # Retorna o gráfico como uma imagem PNG
    return send_file(plot_buffer, mimetype='image/png')

@bp.route('/line_chart', methods=['POST'])
def line_chart():

    data = request.get_json()

    if not data or 'values' not in data:
        return jsonify({'Error': 'Bad Request'})

    values = data['values']

    # Cria o gráfico de linha usando Matplotlib
    plt.plot(values)

    # Salva o gráfico em um buffer de BytesIO
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    plt.close()

    # Retorna o gráfico como uma imagem PNG
    return send_file(plot_buffer, mimetype='image/png')

@bp.route('/bar_chart', methods=['POST'])
def bar_chart():

    data = request.get_json()

    if not data or 'produtos' not in data or 'valores' not in data:
        return jsonify({'Error': 'Bad Request'})

    produtos = data['produtos']
    valores = data['valores']

    # Cria o gráfico de barras usando Matplotlib
    plt.bar(produtos, valores)

    # Salva o gráfico em um buffer de BytesIO
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    plt.close()

    # Retorna o gráfico como uma imagem PNG
    return send_file(plot_buffer, mimetype='image/png')

@bp.route('/bubble_chart', methods=['POST'])
def bubble_chart():

    data = request.get_json()

    if not data or 'x' not in data or 'y' not in data or 'size' not in data:
        return jsonify({'Error': 'Bad Request'})

    eixo_x = data['x']
    eixo_y = data['y']
    size = data['size']
    #podemos adicionar também mais uma variável de cor, para definirmos qual cor será cada bolha

    # Cria o gráfico de bolhas usando Matplotlib
    plt.scatter(eixo_x, eixo_y, s=size)

    # Salva o gráfico em um buffer de BytesIO
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    plt.close()

    # Retorna o gráfico como uma imagem PNG
    return send_file(plot_buffer, mimetype='image/png')

@bp.route('/dot_plot', methods=['POST'])
def dot_plot():

    data = request.get_json()

    if not data or 'x' not in data or 'y' not in data:
        return jsonify({'Error': 'Bad Request'})

    x = data['x']
    y = data['y']

    # Cria o gráfico de pontos usando Matplotlib
    plt.plot(x, y, marker='o', linestyle='none', markersize=10)

    # Salva o gráfico em um buffer de BytesIO
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    plt.close()

    # Retorna o gráfico como uma imagem PNG
    return send_file(plot_buffer, mimetype='image/png')

# fiz gráficos bem básicos, mas podemos alterar várias coisas no layout dele, como adicionar título, grade e entre outros designs.