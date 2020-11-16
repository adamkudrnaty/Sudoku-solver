import pygame
import numpy as np

# Drawing the sudoku grid
def draw_the_grid():
    for row in range(9):
        for column in range(9):
            color = BLACK
            for numbers in range(1,10):
                if grid[row][column] == numbers:
                    number[row][column] = myfont.render(str(numbers), False, (255, 255, 255))
            pygame.draw.rect(screen, color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])

def init(array):
    sudoku_array = array
    class END(Exception): pass

    def xy_to_number(x, y): return sudoku_array[(9*(8-y)+x)]
    def xy_to_location(x, y): return (9*(8-y)+x)
    def xy_to_location2(y, x): return (9*(y)+x)

    #CHECK IF THE X LINE MEETS THE RULES
    def is_in_my_line(x, y, number):
        for columns in range(9):
            if(columns != y):
                if (xy_to_number(x, columns) == number): return True
        for rows in range(9):
            if(rows != x):
                if (xy_to_number(rows, y) == number): return True
        return False

    #CHECK IF THE SQUARE MEETS THE RULES
    def my_square(puvodx, puvody, number):
        if (puvodx/3 < 1): square_x = 0
        elif (puvodx/3 >= 2): square_x = 2
        else: square_x = 1

        if (puvody/3 < 1): square_y = 0
        elif (puvody/3 >= 2): square_y = 2
        else: square_y = 1

        for x in range(3*square_x, 3*square_x+3):
            for y in range(3*square_y, 3*square_y+3):
                if(xy_to_number(x, y) == number): return True
        return False


    #CREATE OPTIONS
    def create_options(array):
        options = []
        alloptions = [1,2,3,4,5,6,7,8,9]
        for x in range(len(array)):
            if array[x] == 0: options.append(alloptions)
            else: options.append(array[x])
        return options

    def odstran(number, array):
        custom_array = array
        if(isinstance(custom_array, list)):
            for i in range(len(custom_array)):
                if len(custom_array) == 0: return 0
                if custom_array[i] == number:
                    index = [i]
                    custom_array = np.delete(custom_array, index)
                    return list(custom_array)
        return list(array)

    def check(sudoku_array):
        counter = 0
        for i in range(len(sudoku_array)):
            if(sudoku_array[i] == 0): counter = counter + 1
        return counter

    def check_duplicates(array):
        if len(array) == len(set(array)): return False 
        else: return True

    def check_lines(array):
        numbers_in_line = []
        count_numbers_in_line = 9
        for line in range(81):
            if array[line] != 0 and len(numbers_in_line) != count_numbers_in_line: numbers_in_line.append(array[line])
            elif array[line] == 0 and len(numbers_in_line) != count_numbers_in_line: count_numbers_in_line = count_numbers_in_line - 1
            if len(numbers_in_line) == count_numbers_in_line:
                if check_duplicates(numbers_in_line) == True: return False
                count_numbers_in_line = 9
                numbers_in_line = []
        return True

    def check_rows(array):
        numbers__in_columns = []
        amount_of_numbers_in_columns = 9
        for line in range(9):
            for row in range(9):
                if array[9*row+line] != 0 and len(numbers__in_columns) != amount_of_numbers_in_columns: numbers__in_columns.append(array[9*row+line])
                elif array[9*row+line] == 0 and len(numbers__in_columns) != amount_of_numbers_in_columns: amount_of_numbers_in_columns = amount_of_numbers_in_columns - 1
                if len(numbers__in_columns) == amount_of_numbers_in_columns:
                    if check_duplicates(numbers__in_columns) == True: return False
                    amount_of_numbers_in_columns = 9
                    numbers__in_columns = []
        return True

    def check_squares(array):
        numbers__in_columns = []
        amount_of_numbers_in_columns = 9
        for y in range(3):
            for x in range(3):
                for a in range(3):
                    for b in range(3):
                        if array[xy_to_location(a + x*3, b + y*3)] != 0 and len(numbers__in_columns) != amount_of_numbers_in_columns: numbers__in_columns.append(array[xy_to_location(a + x*3, b + y*3)])
                        elif array[xy_to_location(a + x*3, b + y*3)] == 0 and len(numbers__in_columns) != amount_of_numbers_in_columns: amount_of_numbers_in_columns = amount_of_numbers_in_columns - 1
                        if len(numbers__in_columns) == amount_of_numbers_in_columns:
                            if check_duplicates(numbers__in_columns) == True: return False
                            amount_of_numbers_in_columns = 9
                            numbers__in_columns = []
        return True

    #CHECK IF THE SUDOKU ARRAY DOESN´T BREAK ANY RULES
    def check2(array):
        if check_rows(array) == True and check_lines(array) == True and check_squares(array) == True: return True
        return False

    #DELETE ALL FALSE OPTIONS FOR INDIVIDUAL BOXES
    def delete_options(options):
        for a in range(9):
            for b in range(9):
                for c in range(10):
                    if(xy_to_number(a, b) == 0):
                        if(is_in_my_line(a,b,c) == True):
                            position = xy_to_location(a, b)
                            options[position] = odstran(c, options[position])
                        elif(my_square(a,b,c) == True):
                            position = xy_to_location(a, b)
                            options[position] = odstran(c, options[position])
        return options

    def vykresleni_do_sudoku_array(options, sudoku_array):
        for a in range(81):
            if(isinstance(options[a], list) == True):
                if(len(options[a]) == 1): 
                    styl = options[a]
                    sudoku_array[a] = styl[0]
        return sudoku_array
    
    def draw_sudoku_array(array):
        for row in range(9):
            for column in range(9):
                if array[xy_to_location2(row, column)] != 0:
                    number[row][column] = myfont.render(str(array[xy_to_location2(row, column)]), False, YELLOW)
                    screen.blit(number[row][column],(column*50 + 20 + MARGIN*column,row*50 + 10 + MARGIN*row))
        pygame.display.flip()
                

    predchozi_vysledek = 0
    options = create_options(sudoku_array)

    while(check(sudoku_array) > 1):
        if predchozi_vysledek == check(sudoku_array): break
        predchozi_vysledek = check(sudoku_array)
        options = delete_options(options)
        sudoku_array = vykresleni_do_sudoku_array(options, sudoku_array)
        print(sudoku_array)
        draw_the_grid()
        draw_sudoku_array(sudoku_array)

    if check(sudoku_array) == 0: print(sudoku_array) #done
    else: #backtracking
        print("NOT COMPLETED YET -> backtracking")
        backtracking_sudoku_array, backup_sudoku_array = (sudoku_array for i in range(2))
        backtracking_options, location_backtracking_options, my_options = ([] for i in range(3))
        my_position = 0
        for i in range(len(options)):
            if(isinstance(options[i], list) and len(options[i]) > 1): backtracking_options.append(options[i])

        for i in range(len(backtracking_options)):
            backtracking_options[i] = [0] + backtracking_options[i]
            my_options.append(0)
                
        for i in range(len(sudoku_array)):
            if(sudoku_array[i] == 0): location_backtracking_options.append(i)

        def backtracking(my_position):
            print(backtracking_sudoku_array)
            draw_the_grid()
            draw_sudoku_array(backtracking_sudoku_array)
            if check2(backtracking_sudoku_array) == False:
                if my_options[my_position] < len(backtracking_options[my_position]) - 1:
                    my_options[my_position] += 1
                    backtracking_sudoku_array[location_backtracking_options[my_position]] = backtracking_options[my_position][my_options[my_position]]
                elif my_options[my_position] == len(backtracking_options[my_position]) - 1:
                    backtracking_sudoku_array[location_backtracking_options[my_position]] = 0
                    my_options[my_position] = 0
                    backtracking_sudoku_array[location_backtracking_options[my_position]] = backtracking_options[my_position][my_options[my_position]]
                    my_position -= 1
                    is_done = False
                    while(is_done == False):
                        if my_options[my_position] < len(backtracking_options[my_position]) - 1:
                            my_options[my_position] += 1
                            backtracking_sudoku_array[location_backtracking_options[my_position]] = backtracking_options[my_position][my_options[my_position]]
                            is_done = True
                        else:
                            my_options[my_position] = 0
                            backtracking_sudoku_array[location_backtracking_options[my_position]] = backtracking_options[my_position][my_options[my_position]]
                            my_position -= 1
                return my_position
            else:
                if my_options[my_position] == 0:
                    my_options[my_position] += 1
                    backtracking_sudoku_array[location_backtracking_options[my_position]] = backtracking_options[my_position][my_options[my_position]]
                elif my_position < len(my_options) - 1:
                    my_position += 1
                    my_options[my_position] += 1
                    backtracking_sudoku_array[location_backtracking_options[my_position]] = backtracking_options[my_position][my_options[my_position]]
                else:
                    raise END
            return my_position

        try:
            while True:
                backup_sudoku_array = backtracking_sudoku_array
                my_position = backtracking(my_position)
        except END: pass

sudoku_array = []
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (244,175,27)
WIDTH = 50 # WIDTH of each square
HEIGHT = 50 # HEIGHT of each square
MARGIN = 2 # Margin between each cell
 
# Create a 2 dimensional array(grid) that we´ll later fill with sudoku numbers #
grid, number = ([] for i in range(2))

for row in range(10):
    grid.append([])
    number.append([])
    for column in range(10):
        grid[row].append(0)
        number[row].append(0)

def erase():
    for row in range(10):
        for column in range(10):
            grid[row][column] = 0
            number[row][column] = 0

pygame.init() # Initialize pygame (gui)

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)

WINDOW_SIZE = [900, 475]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sudoku solver")

done = False

# -------- Main Loop until the user clicks the close button----------- #
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  done = True  # Flag that we are done -> we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            if column > 9 or row > 9:
                if(pos[0] > 600 and pos[0] < 800 and pos[1] < 125 and pos[1] > 50):
                    # Solve the sudoku
                    for row in range(9):
                        for column in range(9):
                            sudoku_array.append(grid[row][column])
                    init(sudoku_array)
                elif(pos[0] > 600 and pos[0] < 800 and pos[1] < 205 and pos[1] > 130):
                    # Erase the sudoku board
                    erase()
                    sudoku_array = []
            elif grid[row][column] == 9:
                grid[row][column] = 0
                number[row][column] = myfont.render("", False, (255, 255, 255))
                screen.blit(number[row][column],(column*50 + 20 + MARGIN*column,row*50 + 10 + MARGIN*row))
            else: grid[row][column] += 1
 
    # Set the screen background
    screen.fill(WHITE)
    draw_the_grid()
    
    # Displaying sudoku numbers that we chose
    for row in range(9):
        for column in range(9):
            if number[row][column] != 0: screen.blit(number[row][column],(column*50 + 20 + MARGIN*column,row*50 + 10 + MARGIN*row))

    pygame.draw.rect(screen, BLACK,[600,50,200,75])
    pygame.draw.rect(screen, BLACK,[600,130,200,75])
    SOLVE = myfont.render("SOLVE", False, YELLOW)
    ERASE = myfont.render("ERASE", False, YELLOW)
    screen.blit(SOLVE,(650,75))
    screen.blit(ERASE,(650,150))
 
    # Updates the screen
    pygame.display.flip()

pygame.quit()
