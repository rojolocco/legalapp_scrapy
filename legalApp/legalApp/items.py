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

def remove_requisitos_generales(value):
    return [item.split('Requisitos generales')[0] for item in value]

def replace_tab(value):
    return [item.replace('\t', ' ') for item in value]

def string_replace_dondeAcudir(value):
    return value.replace("\"", "'").split("var arrDondeAcudir = ")[1].split(".")[0].replace("'","").split("|")

def remove_vineta(value):
    value = [item.replace("•", "").strip() for item in value]
    return [item.replace("-", "").strip() for item in value]

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
    value = value[0].split(')',1)
    return value[1:]

def solo_primero(value):
    return value[0]




## Class Item -> Home #############################
class HomeLegalAppItem(scrapy.Item):
    Id = scrapy.Field(
        output_processor=TakeFirst()
    )
    
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
    Id = scrapy.Field(
        output_processor=TakeFirst()
    )
    
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
    Id_total = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    Id_local = scrapy.Field(
        output_processor=TakeFirst()
    )
    
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
        output_processor=Compose(descripcion_clean, solo_primero)
    )
    
    que_hacer = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip),
        #output_processor=Compose(remove_line, remove_costos_abogado_otros, replace_tab)
        output_processor=Compose(split_dot, remove_line, remove_costos_abogado_otros, remove_requisitos_generales)
    )
    
    donde_acudir = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip, string_replace_dondeAcudir, str.title),
        #output_processor=TakeFirst()
    )
    
    tenga_encuenta = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip),
        #output_processor=Compose(remove_vineta, split_dot, remove_line)
        output_processor=Compose(split_dot, remove_line, remove_vineta)
    )
    
    normatividad = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, str.strip),
        output_processor=Compose(split_dot, remove_line, remove_vineta)
    )
    
    fecha = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    