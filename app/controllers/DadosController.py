from app.models.tables import Dados
from app.ext.db import db


class DadosController():
    @staticmethod
    def create(data):
        dado = Dados(nome_do_banco=data["banco"], coluna=data["coluna"], desc=data["desc"], nome_tabela=data["tabela"])
        db.session.add(dado)
        db.session.commit()
    
    @staticmethod
    def get(id):
        dados = Dados.query.filter_by(_id=id).first()
        return dados

    @staticmethod
    def get_all(dbname=None):
        if dbname:
            dados = Dados.query.filter_by(nome_do_banco=dbname).all()
        else:
            dados = Dados.query.all()
        return dados
    
    @staticmethod
    def delete(id):
        dado = Dados.query.filter_by(_id=id).first()
        db.session.delete(dado)
        db.session.commit()

    @staticmethod
    def get_viewname(nome):
        view_name = Dados.query.filter_by(coluna=nome).first().nome_tabela
        return view_name
    
    