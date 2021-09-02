from types import resolve_bases
import urllib
from utils import load_data, load_template, writeNote, build_response
import sys
sys.path.insert(1, '/home/nicolas/TecWeb/projeto-1/db')
from database import Note, Database

def index(request):

    db = Database('notes')

    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            keyList = chave_valor.split("=")
            keyList[0] = urllib.parse.unquote_plus(keyList[0], encoding = 'utf-8')
            keyList[1] = urllib.parse.unquote_plus(keyList[1], encoding = 'utf-8')
            params[keyList[0]] = keyList[1]
        print("================{}======================".format(params))
        db.add(Note(title=params['titulo'], content=params['detalhes']))
        writeNote(params)
        response = build_response(code=303, reason='See Other', headers='Location: /')
        return response
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content)
        for dados in db.get_all()
    ]
    notes = '\n'.join(notes_li)
    return build_response(load_template('index.html').format(notes=notes))