# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose
from w3lib.html import remove_tags, replace_escape_chars
import re


## Funciones de limpieza #############################
def url_join(value):
    return f"https://www.legalapp.gov.co{value}"

def remove_space(value):
    return value.replace(" ", "")

def remove_line(value):
    return [item for item in value if len(item) > 2]

def remove_costos_abogado_otros(value):
    abogado = [item for item in value if "abogado?" not in item]
    costo = [item for item in abogado if "costo?" not in item]
    return [item for item in costo if "generales" not in item]

def replace_tab(value):
    return [item.replace('\t', ' ') for item in value]

def string_replace_dondeAcudir(value):
    return value.replace("\"", "'").split("var arrDondeAcudir = ")[1].split(".")[0].replace("'","").split("|")

def remove_vineta(value):
    return [item.replace("•", "").strip() for item in value]

def split_dot(value):
    l = value[0].split(".")
    return [item.strip()+"." for item in l]

def normatividad_clean(value):
    return [item[1:].strip() for item in value]

def normatividad_clean2(value):
    if len(value) == 1:
        l = value[0].split(".")
        return [item.strip()+"." for item in l]

def descripcion_clean(value):
    value = value[1:]
    return " ".join(value)




## Class Item -> Home #############################
class HomeLegalAppItem(scrapy.Item):
    categoria = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    
    link = scrapy.Field(
        input_processor=MapCompose(url_join),
        output_processor=TakeFirst()
    )

    abs_link = scrapy.Field(
        #input_processor=MapCompose(remove_space, remove_tags, url_join),
        output_processor=TakeFirst()
    )



## Class Item -> Categoria #############################
class CategoriaLegalAppItem(scrapy.Item):
    subcategoria = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    
    link = scrapy.Field(
        input_processor=MapCompose(url_join),
        output_processor=TakeFirst()
    )
    


## Class Item -> Preguntas #############################
class PreguntasLegalAppItem(scrapy.Item):
    pregunta = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    
    link = scrapy.Field(
        input_processor=MapCompose(url_join, remove_space),
        output_processor=TakeFirst()
    )


## Class Item -> Respuestas #############################
class RespuestasLegalAppItem(scrapy.Item):
    pregunta = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    
    descripcion = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip),
        output_processor=Compose(remove_line, descripcion_clean)
    )
    
    que_hacer = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Compose(remove_line, remove_costos_abogado_otros, replace_tab)
    )
    
    donde_acudir = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip, string_replace_dondeAcudir, str.title),
        #output_processor=TakeFirst()
    )
    
    tenga_encuenta = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip),
        output_processor=Compose(remove_vineta, split_dot, remove_line)
    )
    
    normatividad = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip),
        output_processor=Compose(split_dot, remove_line)
    )
    
    fecha = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    