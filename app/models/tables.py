from app.ext.db import db
from datetime import datetime

##
## Declaração das models
##

#Lista de colunas no banco
class ListaColunas(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #Nome da tabela
    tabela = db.Column(db.String, nullable=False)
    
    #Nome da coluna
    colunas = db.Column(db.String, nullable=False)

class Dados(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #Nome do banco Protheus / Zenith
    nome_do_banco = db.Column(db.String, nullable=False)
    coluna = db.Column(db.String, nullable=False)
    nome_tabela = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)

class Filtro(db.Model):
    _id = db.Column(db.String, primary_key=True)

    #Nome / descrição do filtro
    nome = db.Column(db.String, nullable=False)

    #Latitude inicial
    lat = db.Column(db.String, nullable=False)

    #longitude inicial
    long = db.Column(db.String, nullable=False)

    #Zoom inicial
    zoom = db.Column(db.Integer, nullable=False)

    #Tipo de mapa
    maptype = db.Column(db.String, nullable=False)

    #Cor do filtro (marca os talhoes filtrados com essa cor no mapa)
    cor = db.Column(db.String, nullable=False)

    #lista de filtros no formato [('feature', 'conteudo'), ...]
    lista_filtros = db.Column(db.String, nullable=False)

    #Lista de tooltips que aparecem quando passa o mouse ["nome1", "nome2", ...]
    list_tooltips = db.Column(db.String)

    #Lista de perfil que podem utilizar o filtro separado por virgula
    perfis = db.Column(db.String, nullable=False, default="") 

#Usuario do sistema
class User(db.Model):
    _id = db.Column(db.String, primary_key=True)
    file = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    dep = db.Column(db.String, default="")
    admin = db.Column(db.Boolean, default=False)

    allow = db.Column(db.Boolean, default=False)

#Perfil com permiçoes para funcionalidades
class Perfil(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False) # Nome do departamento / permissoes

    #Pode criar filtros
    create_filter = db.Column(db.Boolean, default=False)

    #Pode criar campos de dados
    create_dados = db.Column(db.Boolean, default=False)
    
    #Pode visualizar e utilizar a editar lista de usuarios 
    view_users = db.Column(db.Boolean, default=False)

    #Pode visualizar e editar a lista de perfis
    view_perfis = db.Column(db.Boolean, default=False)

