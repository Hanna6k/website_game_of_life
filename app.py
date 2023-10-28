from flask import Flask, render_template, request
from game_of_life_03 import World
from game_of_life_03 import pattern_list

app = Flask(__name__)

X_VISUAL_SIZE=800
Y_VISUAL_SIZE=450
CELL_SIZE = 15
TIME_NEW_CELL = 1000
number_of_random_cells = (X_VISUAL_SIZE//CELL_SIZE)*(Y_VISUAL_SIZE//CELL_SIZE)//4
pos_pattern = 0

world = World(random_x_range=X_VISUAL_SIZE, random_y_range=Y_VISUAL_SIZE, cell_size=CELL_SIZE)

@app.route("/")
def index():
    canvas_width = X_VISUAL_SIZE
    canvas_height = Y_VISUAL_SIZE
    return render_template('index.html',canvas_width=canvas_width, canvas_height=canvas_height)

@app.route('/cellsize') # only passes on cell size
def pass_on_cellsize():
    return{'cellsize': CELL_SIZE} #give data to js

@app.route('/time_new_update') # only passes on cell size
def pass_on_time():
    return{'time_update': TIME_NEW_CELL} #give data to js

@app.route('/random_cells') # passes on coordinates of random generated cells
def pass_on_startcells():
    world.kill_all_cells()
    random_cells = world.create_random_cells(start_num_alive=number_of_random_cells)
    return random_cells #give data to js

@app.route('/pattern')
def pass_on_pattern():  # passes on coordinates of of a pattern
    global pos_pattern
    pos_pattern += 1
    if pos_pattern >= len(pattern_list):
        pos_pattern = 0    
    world.kill_all_cells()
    world.create_pattern(pattern_list[pos_pattern])
    pattern = pattern_list[pos_pattern]
    return pattern #give data to js

@app.route('/update')
def update_cells(): # passes on the updated coordinates
    updated_cells = world.update()
    return updated_cells #give data to js

if __name__ ==  "__main__":
    app.run()








