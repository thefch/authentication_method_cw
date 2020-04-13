
const MAX_NUM_POINTS = 4;
var points = initArray();
const rowsNum = 40;
const colsNum = 40;
let numberOfPointsSelected = 0;

window.onload = () => {
    let lastClicked;
    const grid = clickableGrid(rowsNum, colsNum, function (el, row, col, i) {
        // console.log("You clicked on item:", i);

        if(el.className === 'clicked'){
            el.className = '';
            setPoint('remove',i);
            // points[numberOfPointsSelected] = null;
            // numberOfPointsSelected--;
        }else{
            // console.log(numberOfPointsSelected);
            if (numberOfPointsSelected < MAX_NUM_POINTS) {
                el.className = 'clicked';
                setPoint('add', i);
                // points[numberOfPointsSelected] = i;
                // numberOfPointsSelected++;
            }
        }
        console.log('number of points:',numberOfPointsSelected);


        update_keyword(el,'click', i);
        // console.log('number of points:');

        // show hide selected cell's point
        var span = el.children[0];
        span.style.display = span.style.display === 'none' ? 'block' : 'none';

        // if (lastClicked)
        //     lastClicked.className = '';
        //     //lastClicked.className = 'unClicked';
        // lastClicked = el;

        // document.getElementById(el.id).style.borderStyle = "solid";

    });

    //document.body.appendChild(grid);
    //init clickable grid
    function clickableGrid(rows, cols, callback) {
        let i = 0;
        //const grid = document.createElement('table');
        const grid = document.getElementById('grid-id');
        //grid.className = 'grid';
        //grid.id = 'grid-id';

        for (let r = 0; r < rows; ++r) {
            let tr = grid.appendChild(document.createElement('tr'));

            for (let c = 0; c < cols; ++c) {
                let cell = tr.appendChild(document.createElement('td'));
                cell.className = 'cell';
                cell.id = 'cell-id';
                cell.style.borderStyle = 'hidden';
                cell.value = ++i;
                //cell.onclick();

                let span = cell.appendChild(document.createElement('span'));
                span.className='dot';
                span.style.display = 'none';

                cell.addEventListener('click', (function (el, r, c, i) {

                    return function () {


                        callback(el, r, c, i);
                    }
                })
                (cell, r, c, i), false);
            }
        }

        return grid;
    }


    document.getElementById('loading-gif').hidden = "hidden";
    //document.getElementById('grid-id').appendChild(grid);

};

function setPoint(method,value){
    // console.log(points);
    if(method==='remove'){
        points[points.indexOf(value)] = null;
        numberOfPointsSelected--;
    }
    else if (method==='add') {
        for (let i = 0; i < MAX_NUM_POINTS; i++) {
            // console.log(i,' ',points[i]);
            if(points[i] === null){
                points[i] = value;
                numberOfPointsSelected++;
                return
            }
        }
    }
}

function resetPoint(pointNum){
    let cell = findCell(pointNum);
    //console.log(cell);
    if (cell){
        // console.log('cell:',cell);
        // console.log('cell:',cell.children[0]);
        cell.children[0].style.backgroundColor = 'grey';
    }
}

function peekPoint(pointNum){

    let cell = findCell(pointNum);
    // console.log(cell);
    if (cell){
        // console.log('cell:',cell);
        // console.log('cell:',cell.children[0]);
        cell.children[0].style.backgroundColor = 'blue';
    }
}

function findCell(pointNum){
    let found = false;
    let point = points[pointNum];
    // let cell;
    if(point) {
        let colIndex = Math.floor(point-1 % colsNum)-1;
        let rowIndex = Math.floor(point-1 / rowsNum);
        let rows = document.getElementById('grid-id').children;
        for (let i = 0; i < rows.length; i++) {
            for (let c = 0; c < rows[i].children.length; c++) {
                let val = rows[i].children[c].value;
                if(val === point){
                    // console.log('actual index: ',i,',',c);
                    return rows[i].children[c];
                    // found = true;
                    // break;
                }
            }
            // if (found){
            //     break;
            // }
        }

    }else {
        // console.log('no point selected!');
    }
    // console.log('point:',point);

    return null;
}

function initArray() {
    let arr = [];
    for (let i = 0; i < MAX_NUM_POINTS; i++) {
        arr[i] = null;
    }
    return arr;
}
