from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

##
## Declaração dos Formularios com Wtforms
##

class Dep(FlaskForm):
    dep = SelectField("departamento", choices=[
    ("TI", "TI"),
    ("Colheita", "Colheita"),
    ("Geoprocessamento", "Geoprocessamento"),
    ("Juridico", "Juridico"),
    ("Pesquisa", "Pesquisa"),
    ("Relaçoes com Comunidade", "Relaçoes com Comunidade"),
    ("DMAST", "DMAST"),
    ("Gerencia", "Gerencia"),
    ("Interprete", "Interprete"),
    ("Administrativo", "Administrativo"),
    ("Import/Export", "Import/Export"),
    ("Diretoria", "Diretoria"),
    ("Compras", "Compras"),
    ("Soja", "Soja"),
    ("GFundiário", "GFundiário"),
    ], coerce=str)

    def insert_data(self, data):
        self.dep.data = data.dep
        

