from flask import Flask, render_template, request
import numpy as np
from game_of_life_03 import Cell
from game_of_life_03 import World


from game_of_life_03 import pattern_list


app = Flask(__name__)

# ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '.', ',', '!', '?']
# def encryption_caesar(cleartext,n):
#     encryption = ""
#     cleartext = cleartext.upper()
#     for letter in cleartext:       
#         position = ALPHABET.index(str(letter))
#         new_position = position + n
#         if new_position > len(ALPHABET):
#             new_position -= len(ALPHABET)
#         new_letter = ALPHABET[new_position]
#         encryption += new_letter  
#     return encryption

X_VISUAL_SIZE=800
Y_VISUAL_SIZE=450
start_num = (800//15)*(450//15)//5
CELL_SIZE = 15
pos_pattern = 0

world = World(random_x_range=X_VISUAL_SIZE, random_y_range=Y_VISUAL_SIZE, cell_size=CELL_SIZE)




@app.route("/")
def index():
    return render_template('index.html')

# @app.route('/encrypt', methods =["POST"])
# def encrypt():
#     plain_text = request.json['data']   # gets data from js
#     cipher_text = encryption_caesar(plain_text, 1)
#     print("hi")
#     return{'cipher': cipher_text} #give data to js

@app.route('/cellsize')
def pass_on_cellsize():
    return{'cellsize': CELL_SIZE} #give data to js

@app.route('/start_cells')
def pass_on_startcells():
    world.kill_all_cells()
    p = world.create_starting_cells(start_num_alive=start_num)
    # print('ur mum')
    return p #give data to js

@app.route('/pattern')
def pass_on_pattern():
    global pos_pattern
    pos_pattern += 1
    if pos_pattern >= len(pattern_list):
        pos_pattern = 0    
    world.kill_all_cells()
    world.create_pattern(pattern_list[pos_pattern])
    p = pattern_list[pos_pattern]
    return p #give data to js


@app.route('/update')
def update_cells():
    p = world.update()
    # print(p)
    return p #give data to js


# @app.route('/pattern')
# def pass_on_pattern():
#     pos_pattern += 1
#     world.kill_all_cells()
#     world.create_pattern(pattern_list[pos_pattern]) 
#     p = pattern_list[pos_pattern]
#     return p #give data to js


# @app.route('/updategame')
# def pass_on_coords():
#     coords = list
#     return coords # dictionary is better not list eventuel umwandeln

if __name__ ==  "__main__":
    app.run()








