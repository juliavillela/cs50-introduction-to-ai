from generate import CrosswordGenerator
from helpers import validate_word_list
from constants import *


word_list_1 = [
    "scooby",
    "eva",
    "onilda",
    "peido",
    "grude",
    "dengo",
    "mafalda",
    "caneca",
]

word_list_2 = [
    "proletariado",
    "meiosdeproducao",
    "maisvalia",
    "lucro",
    "capital",
    "burguesia",
    "classesocial",
    "tempo",
    "maodeobra",
    "terra",
    "trabalho"
]

word_list_3 = [
    "cafecomleite",
    "agua",
    "suco",
    "paonachapa",
    "paodequeijo",
    "tapioca",
    "bolo",
    "queijo",
    "geleia",
    "manteiga"
]

word_list_4 = word_list_3 + word_list_2
word_list_5 = word_list_3 + word_list_1
word_list_6 = word_list_5 + word_list_4 # invalid

def generate_crossword(word_list):
    validate_word_list(word_list)
    gen = CrosswordGenerator(word_list)
    crossword = gen.generate()
    if crossword:
        crossword.save_key_img(f"grids/test_key.png")
        crossword.save_blank_img("grids/test_blank.png")
    else:
        print("COULD NOT generate")

generate_crossword(word_list_6)