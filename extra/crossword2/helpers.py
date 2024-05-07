from constants import *

# def save_grid_image(grid:list, filename:str):
#     """
#     Create an image representing the grid(a two-dimentional list) and save it to filename.
#     """
#     from PIL import Image, ImageDraw, ImageFont
#     cell_size = 50
#     cell_border = 2
#     interior_size = cell_size - 2 * cell_border

#     img = Image.new(
#         "RGBA",
#         ( grid.width() * cell_size,
#         grid.height() * cell_size),
#         "white"
#     )

#     font = ImageFont.load_default(40)
#     draw = ImageDraw.Draw(img)

#     for row in range(grid.height()):
#         for col in range(grid.width()):
#             # Calculate coordinates for the cell
#             x0 = col * cell_size
#             y0 = row * cell_size
#             x1 = (col + 1) * cell_size
#             y1 = (row + 1) * cell_size


#             # Get the character in the cell
#             char = grid.grid[row][col]

#             # Ignore EMPTY and WORD_BOUNDRY
#             if char not in [EMPTY, FILLER]:

#                 # Draw cell border
#                 draw.rectangle([x0, y0, x1, y1], fill="white", outline="black")
#                 # Calculate text size and position
#                 # text_size = draw.textsize(char, font=font)
#                 text_x = x0 + (interior_size - 25) / 2
#                 text_y = y0 + (interior_size - 45) / 2

#                 # Draw the character in the cell
#                 draw.text((text_x, text_y), char, fill="black", font=font)

#     img.save(filename)

# def word_range(word, row, col, direction):
#     if direction == VERTICAL:
#         return set([(row + i, col) for i in range(len(word))])
#     else:
#         return set([(row, col + i) for i in range(len(word))])
    
# def get_absolute_placement(overlap_col, overlap_row, overlap_index, direction):
    # if direction == VERTICAL:
    #     return (overlap_col - overlap_index, overlap_row)
    # else:
    #     return (overlap_col, overlap_row-overlap_index)

def clean(grid:list[list]):
    """
    Returns a copy of grid matrix where FILLER is replaced with None
    """
    clean_grid = []
    for row in grid:
        clean_row = []
        for cell in row:
            if cell == FILLER:
                clean_row.append(EMPTY)
            else:
                clean_row.append(cell)
        clean_grid.append(clean_row)
    return clean_grid

def trim(grid:list[list]):
    """
    Returns a copy of grid matrix where empty columns and empty rows have been removed 
    An empty line is a line where all values == EMPTY

    If called on an empty grid: returns empty grid unchanged.
    """
    # Find the range of rows and columns with non-empty cells
    # grids are assumed to be square
    min_row = min_col = len(grid)
    max_row = max_col = 0
    for row_i, row in enumerate(grid):
        for col_i, cell in enumerate(row):
            if cell is not EMPTY:
                min_row = min(min_row, row_i)
                max_row = max(max_row, row_i)
                min_col = min(min_col, col_i)
                max_col = max(max_col, col_i)

    # Create a new trimmed grid
    trimmed_grid = []
    for row in grid[min_row:max_row + 1]:
        trimmed_grid.append(row[min_col:max_col + 1])

    return trimmed_grid
