from app.models.tables import Filtro
from app.ext.db import db
from uuid import uuid4

class FiltroController():

    @staticmethod
    def create(data):
        filtro = Filtro(_id = str(uuid4()).split('-')[0] ,nome = data["nome"],
                        lista_filtros = data["lista_filtros"],
                        lat = data["lat"], long = data["long"],
                        zoom = data["zoom"],
                        maptype = data["maptype"],
                        cor = data["cor"],
                        list_tooltips = data["tooltips_list"])
        
        db.session.add(filtro)
        db.session.commit()
    
    @staticmethod
    def get(id):
        filtro = Filtro.query.filter_by(_id=id).first()
        return filtro

    @staticmethod
    def get_all():
        filtros = Filtro.query.all()
        return filtros
    
    @staticmethod
    def delete(id):
        filtro = Filtro.query.filter_by(_id=id).first()
        db.session.delete(filtro)
        db.session.commit()
        