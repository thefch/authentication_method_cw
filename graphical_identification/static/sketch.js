

let WIDTH = 300;
let HEIGHT = 300;
var NUM_ROWS = HEIGHT/30;
var NUM_COLS = WIDTH/30;
var grid = [];
var countX =0;
var countY =0;
let img;
var imgPath = "../static/kitten.jpg"

/*
    TODO:
        set sizes of the grid according of the images DIMENSIONS
*/

function preload(){
    img = loadImage(imgPath);
}

function setup(){
    createCanvas(WIDTH,HEIGHT);

    initGrid();
}
function drawTable() {
    var x = 30;
    var y = 20;
    var t = '<table cellspacing="0" border="1" cellpadding="0" class="grxd">';
    for (var i = 1; i <= (x * y); i++) {
        t += (i == 1 ? '<tr>' : '');
        t += '<td style="cursor:pointer;"></td>';
        if (i == (x * y)) {
            t += '</tr>';
        } else {
            t += (i % 30 === 0 ? '</tr><tr>' : '');
        }

    }
    t += '</table>';
    $("#drawTable").html(t);
}
function draw(){
    //background(100,200,50);
    //image(img, 0, 0);
    image(img,0,0 , img.width, img.height);
    drawGrid();
}

function drawGrid(){
    countY = 0;

    for (var y = 0; y <= HEIGHT; y +=10 ) {
        countX=countY;
        for (var x = 0; x <= WIDTH; x +=10) {
            stroke(0);
            strokeWeight(1);
            line(x, 0, x, HEIGHT);
            line(0, y, WIDTH, y);
            textSize(5);
            text(countX-1, x+2, y-2);
            countX ++;
        }
        countY++;
    }
}

function initGrid(){
    for(var i =0;i<NUM_COLS;i++){
        grid[i] = [];
        for(var k =0;k<NUM_ROWS;k++){
            grid[i][k] = i+k;
        }
    }
    console.log(grid)
}