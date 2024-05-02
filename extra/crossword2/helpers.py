from constants import *

def save_grid_image(grid:list, filename:str):
    """
    Create an image representing the grid(a two-dimentional list) and save it to filename.
    """
    from PIL import Image, ImageDraw, ImageFont
    cell_size = 50
    cell_border = 2
    interior_size = cell_size - 2 * cell_border

    img = Image.new(
        "RGBA",
        ( grid.width() * cell_size,
        grid.height() * cell_size),
        "black"
    )

    font = ImageFont.load_default(40)
    draw = ImageDraw.Draw(img)

    for row in range(grid.height()):
        for col in range(grid.width()):
            # Calculate coordinates for the cell
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = (col + 1) * cell_size
            y1 = (row + 1) * cell_size


            # Get the character in the cell
            char = grid.grid[row][col]

            # Ignore EMPTY and WORD_BOUNDRY
            if char not in [None, " "]:

                # Draw cell border
                draw.rectangle([x0, y0, x1, y1], fill="white", outline="black")
                # Calculate text size and position
                # text_size = draw.textsize(char, font=font)
                text_x = x0 + (interior_size - 40) / 2
                text_y = y0 + (interior_size - 40) / 2

                # Draw the character in the cell
                draw.text((text_x, text_y), char, fill="black", font=font)

    img.save(filename)

def word_range(word, row, col, direction):
    if direction == VERTICAL:
        return set([(row + i, col) for i in range(len(word))])
    else:
        return set([(row, col + i) for i in range(len(word))])