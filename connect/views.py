from utils import load_data, load_template, writeNote, build_response
import urllib

import sys
sys.path.insert(1, '/home/nicolas/insper/4o/tecweb/projs/proj-1a/db')
from database import Note, Database


def index(request):
    db = Database('notes')

    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split("=")
            params[chave] = urllib.parse.unquote_plus(
                valor, encoding='utf-8', errors='replace')

        if params['method'] == 'POST':    
            db.add(Note(title=params['titulo'], content=params['detalhes']))
        elif params['method'] == 'DELETE':
            db.delete(note_id=params['id']) 
        elif params['method'] == 'PUT':
            note = Note(id=params['id'], title=params['titulo'], content=params['detalhes'])
            db.update(entry=note)

        response = build_response(
            code=303, reason='See Other', headers='Location: /')
        return response

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id=dados.id)
        for dados in db.get_all()
    ]
    notes = '\n'.join(notes_li)
    return build_response(load_template('pages/index.html').format(notes=notes))
