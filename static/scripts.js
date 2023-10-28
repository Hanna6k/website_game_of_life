const canvas = document.getElementById('myCanvas');
const context = canvas.getContext('2d');

let updateCells = false; 

async function drawFieldLines(cellSize){ // this funktion draws all the lines
    const canvasWidth = canvas.width;  
    const canvasHeight = canvas.height;  
    const numOfVerticalLines = Math.floor(canvasWidth / cellSize) + 1;
    const numOfHorizontalLines = Math.floor(canvasHeight / cellSize) + 1;

    for (let i = 0; i < numOfVerticalLines; i++) {
        pos_x = i*cellSize    
        context.fillStyle ='rgb(51, 51, 51)'; 
        context.fillRect(pos_x, 0, 1,canvasHeight);
    }   
    for (let i = 0; i < numOfHorizontalLines; i++) {
        pos_y = i*cellSize    
        context.fillStyle = 'rgb(51, 51, 51)'; 
        context.fillRect(0, pos_y, canvasWidth,1);
    }  
}

async function fetchCellSize() { // gets cell size from app.py
    let response = await fetch('/cellsize', {
        method: 'GET', 
    });
    let jsonData = await response.json();
    const cellSize = jsonData.cellsize;    
    return cellSize;
}


async function fetchTimeInterval() { // get time_for new uodate but it doesn't work
    let response = await fetch('/time_new_update', {
        method: 'GET', 
    });
    let jsonData = await response.json();
    const timeNewCell = jsonData.cellsize;    
    return timeNewCell;
}


async function patternCells(event){ // gets coordinates of a pattern
    console.log("pressed pattren");
    const cellSize = await fetchCellSize();
    let response = await fetch('/pattern',{
        method: 'GET', 
    });
    let jsonData = await response.json();
    context.clearRect(0, 0, canvas.width, canvas.height);
    for (const elemnt of jsonData){ // draw cells on canvas
        let pos_x = elemnt[0]*cellSize;
        let pos_y = elemnt[1]*cellSize;
        context.fillStyle = 'rgb(222, 221, 181)'; 
        context.fillRect(pos_x, pos_y, cellSize,cellSize);
    }   
    drawFieldLines(cellSize);
}     


async function randomCells(event){ // gets coordinates of random placed cells
    console.log("pressed random");
    const cellSize = await fetchCellSize();

    let response = await fetch('/random_cells',{
        method: 'GET', // because want to send data to server s.t. it can process it
    });
    let jsonData = await response.json();

    context.clearRect(0, 0, canvas.width, canvas.height);
    for (const elemnt of jsonData){ // draws them
        let pos_x = elemnt[0] * cellSize;
        let pos_y = elemnt[1] * cellSize;
        context.fillStyle = 'rgb(222, 221, 181)'; 
        context.fillRect(pos_x, pos_y, cellSize,cellSize);
    }   
    drawFieldLines(cellSize);
}

async function startStop(event){ // is for the stop and start button
    if (updateCells){
        updateCells = false;
        console.log('stop')
    }
    else{
        updateCells = true;
        console.log('start')

    }
}

async function cellUpdate(){ // gets the updated coordinates
    if (updateCells){
        const cellSize = await fetchCellSize();
        let response = await fetch('/update',{
            method: 'GET', 
        });
        let jsonData = await response.json();
        context.clearRect(0, 0, canvas.width, canvas.height);
        for (const elemnt of jsonData){// draws cells
            let pos_x = elemnt[0]*cellSize;
            let pos_y = elemnt[1]*cellSize;
            context.fillStyle = 'rgb(222, 221, 181)'; 
            context.fillRect(pos_x, pos_y, cellSize,cellSize);
        }
        drawFieldLines(cellSize);
    }
}

// const time_inbetween_new_update = await fetchTimeInterval();   don't know how i should do this since await only works in async funktions
setInterval(cellUpdate, 1000); // the cellUpdate funktion is called every second

