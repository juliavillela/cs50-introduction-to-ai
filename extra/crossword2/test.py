from generate import CrosswordGenerator

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

gen = CrosswordGenerator(word_list_4, 25, 5, 40)

gen.generate()