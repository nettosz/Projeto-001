import uuid
from threading import Thread

import folium.map
from werkzeug.utils import secure_filename
from os.path import join, abspath
from os import remove

import folium
from folium.features import GeoJson
from folium.plugins import MousePosition
from folium.plugins import MeasureControl
import folium.features
import folium.folium
import uuid

from app.controllers.FiltroController import FiltroController

import ast

from branca.element import Template, MacroElement
from app.controllers.DatabaseController import DatabaseController
from app.controllers.DadosController import DadosController

legend_colors = []

#Adiciona legenda com as cores para o mapa
def create_color_legenda(cores_data):

    template_colors = "".join([f"<li><span style='background:{item[0]};opacity:0.7;'></span>{item[1]} - {item[2]}</li>" for item in cores_data])

    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>Legendas</div>
    <div class='legend-scale'>
        <ul class='legend-labels'>
            {}
        </ul>
    </div>
    </div>
    
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}""".replace("{}", template_colors)


    macro = MacroElement()
    macro._template = Template(template)

    return macro

######################
import time

def execution_time(func):
    """Decorator that prints the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_seconds = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_seconds:.4f} seconds to execute.")
        return result
    return wrapper

def gen_map_layer(geojson_data, nome, cor, popup, list_filters):
    content = list_filters[0]["c"]

    geojson_obj = GeoJson(data=geojson_data, name=f"{nome} - {content}", fill_opacity=0.5,line_opacity=0.2,
                        highlight=True,
                        style_function=lambda feature: {
                        "fillColor": cor,
                        "color": "black",
                        "weight": 1,
                    },

                    highlight_function=lambda feature: {
                    "fillColor": (
                        "yellow"
                    ),
                },
                popup=popup,
                popup_keep_highlighted=True,
                control_scale=True,
                )
    
    #Constroi o select no banco (WHERE....)
    where, field = DatabaseController.build_sql_where_clause(list_filters)
    
    #Pega  o nome da tabela 
    view_name = DadosController.get_viewname(field)

    #Puxa os dados do banco e faz o merge com os dados em geojson
    new_features = DatabaseController.data_to_geojson(geojson_obj, where, view_name)

    
    #Adicona as novas features do banco ao mapa
    geojson_obj.data['features'] = new_features

    return geojson_obj


def create_map(id_filtro):

    #Carregado filtro pelo id
    filtro = FiltroController.get(id_filtro)
    
    #Checa se o filtro e nulo
    if not filtro:
        return "error"
    
    #Nome do filtro / descrição
    nome = filtro.nome

    #Puxa a lista de tooltips do filtro
    list_tooltips = filtro.list_tooltips.split(",")

    #coodernadas iniciais
    latitude = filtro.lat  # Santanta - AP
    longitude = filtro.long
    
    #Tipo de mapa
    map_type = filtro.maptype

    # Geojson filepath trocar para conecção com banco
    geojson_data = "app/static/files/GeoJsonFile/AREA_SIG_10052024_EPSG4326.geojson"

    #zoom inicial
    zoom = filtro.zoom

    # Create Folium map object
    map = folium.Map(location=[latitude, longitude], zoom_start=zoom, tiles=map_type)

    #Carrega o mapa filtrado apenas se a lista de filtros nao for vazia
    if filtro.lista_filtros:
        camadas = ast.literal_eval(filtro.lista_filtros)

        # Add GeoJSON layer to the map
    
        for camada in camadas:
            # Cria uma popup com a feature QT_AREA_SI mudar dps para graficos
            popup = folium.GeoJsonPopup(fields=["FORESTSITUATIONDESCRIPTION"])
            

            # Gera uma camada do mapa antes do loop de filtro
            geojson_obj = gen_map_layer(geojson_data,
                                        nome,
                                        camada[0]["cor"], popup, camada)
            
            #Adiciona o Tooltip (on mouse hover)
            geojson_obj.add_child(
                folium.features.GeoJsonTooltip(list_tooltips)
            )

            ############ >>>>>>>>>>>>>>>>

            for filtro in camada:
                if isinstance(filtro, dict):
                    feature = filtro["f"]
                    value = filtro["c"]
                    cor = filtro["cor"]

                    #define a cor e o label na legenda
                    legend_colors.append((cor, feature, value))
            
            
            #Checa se o filtro retornou dados
            if geojson_obj.data["features"]:
                geojson_obj.add_to(map)
    else:
        return "error"
    


    # Adiciona mostrar a coordenada do ponteiro do mouse
    MousePosition().add_to(map)
    # map.add_child(MeasureControl())

    #Mensurar distancia e area
    MeasureControl().add_to(map)

    #Adiciona legenda no mapa com as cores 
    map.get_root().add_child(create_color_legenda(legend_colors))
    
    #Limpa a lista de legendas depois de carregar 
    legend_colors.clear()

    return map

####
####
####

def remove_file(file):
    try:
        remove(abspath(f"app/{file}"))
    except:
        pass

def format_name(filename: str) -> str:
    type = filename.split(".")[-1]
    name = f"{uuid.uuid4()}.{type}"
    return name

def upload_file(f, path):
    if f:
        name = format_name(f.filename)
        p = abspath(join(f"app/{path}", secure_filename(name)))        
        f.save(p)
        return f'{path}/{name}'

def user_message(msg):
    return f"""<!DOCTYPE html>
            <html lang="pt-br">
            <body>
                <div class="fade-in-image">
                    <h1 class="title">
                    <div class="ch">
                        {msg}
                    </div>
                    </h1>
                </div>
            </body>
            </html>"""