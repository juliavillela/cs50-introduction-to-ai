from generate import CrosswordGenerator

word_list = [
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

# word_list.extend(word_list_2)
generator = CrosswordGenerator(word_list_3, 16)
generator.iterative_placement()
# generator.grid.display()
generator.save("test.txt")