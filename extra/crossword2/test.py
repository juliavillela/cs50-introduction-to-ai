from generate import CrosswordGenerator
from evaluate import score_grid
from helpers import save_grid_image

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

gen = CrosswordGenerator(word_list_3, 5, 1, 40)

gen.generate()

for index,grid in enumerate(gen.grids):
    print(index, score_grid(grid.grid))
    save_grid_image(grid, f"grids/test{index}.png")