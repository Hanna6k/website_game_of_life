console.log("asd");
const canvas = document.getElementById('myCanvas');
const context = canvas.getContext('2d');

let updateCells = false;

async function drawFieldLines(cellSize){
    const canvasWidth = canvas.width;  // Get the canvas width (e.g., 800)
    const canvasHeight = canvas.height;  // Get the canvas height (e.g., 450)
    const numOfVerticalLines = Math.floor(canvasWidth / cellSize) + 1;
    const numOfHorizontalLines = Math.floor(canvasHeight / cellSize) + 1;

    for (let i = 0; i < numOfVerticalLines; i++) {
        pos_x = i*cellSize    
        context.fillStyle = 'black'; 
        context.fillRect(pos_x, 0, 1,canvasHeight);
    }   
    for (let i = 0; i < numOfHorizontalLines; i++) {
        pos_y = i*cellSize    
        context.fillStyle = 'black'; 
        context.fillRect(0, pos_y, canvasWidth,1);
    }  
}

async function fetchCellSize() {
    let response = await fetch('/cellsize', {
        method: 'GET', // Sending a GET request to retrieve the cell size
    });

    let jsonData = await response.json();
    const cellSize = jsonData.cellsize;
    
    return cellSize;
    // Now you can use the 'cellSize' variable in your JavaScript code
}

async function patternCells(event){
    console.log("pressed pattren");
    const cellSize = await fetchCellSize();
    console.log(cellSize)
    let response = await fetch('/pattern',{
        method: 'GET', // because want to send data to server s.t. it can process it
    });
    let jsonData = await response.json();
    console.log('fucj');
    context.clearRect(0, 0, canvas.width, canvas.height);
    drawFieldLines(cellSize);
    for (const elemnt of jsonData){
        let pos_x = elemnt[0]*cellSize;
        let pos_y = elemnt[1]*cellSize;
        console.log(elemnt);
        context.fillStyle = 'blue'; 
        context.fillRect(pos_x, pos_y, cellSize,cellSize);

    }
    
}     


async function handleStartCells(event){
    console.log("pressed start");
    const cellSize = await fetchCellSize();

    let response = await fetch('/start_cells',{
        method: 'GET', // because want to send data to server s.t. it can process it
    });
    let jsonData = await response.json();

    context.clearRect(0, 0, canvas.width, canvas.height);
    drawFieldLines(cellSize);
    for (const elemnt of jsonData){
        let pos_x = elemnt[0] * cellSize;
        let pos_y = elemnt[1] * cellSize;
        console.log(pos_x, pos_y);
        context.fillStyle = 'blue'; 
        context.fillRect(pos_x, pos_y, cellSize,cellSize);
    }   
}

async function startStop(event){
    if (updateCells){
        updateCells = false;
        console.log('stop')
    }
    else{
        updateCells = true;
        console.log('start')

    }
}





async function cellUpdate(){
    if (updateCells){
        const cellSize = await fetchCellSize();
        let response = await fetch('/update',{
            method: 'GET', // because want to send data to server s.t. it can process it
        });
        let jsonData = await response.json();
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawFieldLines(cellSize);
        for (const elemnt of jsonData){
            let pos_x = elemnt[0]*cellSize;
            let pos_y = elemnt[1]*cellSize;
            console.log(elemnt);
            context.fillStyle = 'blue'; 
            context.fillRect(pos_x, pos_y, cellSize,cellSize);
        }
    }
}




setInterval(cellUpdate, 2000);