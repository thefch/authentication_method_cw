
const MAX_NUM_POINTS = 4;
var points = initArray();
const rowsNum = 40;
const colsNum = 40;
let numberOfPointsSelected = 0;
var hasEnough = false;
window.onload = () => {
    let lastClicked;

    const grid = clickableGrid(rowsNum, colsNum, function (el, row, col, i) {
        if (numberOfPointsSelected < MAX_NUM_POINTS) {

            if (el.className === 'clicked') {
                updatePoint(el,'remove',i);

            } else {
                updatePoint(el,'add',i);

            }

            update_keyword(el, 'click', i);
            // console.log('number of points:');

            updateCell(el);
            /*// show hide selected cell's point
            var span = el.children[0];
            span.style.display = span.style.display === 'none' ? 'block' : 'none';*/
        }else{
            if(isAlreadySelected(el)) {
                console.log('cell:', i, '  is already selected');
                updatePoint(el,'remove',i);


                update_keyword(el, 'click', i);
                // console.log('number of points:');

                updateCell(el);

            }
        }

        hasEnough = numberOfPointsSelected === MAX_NUM_POINTS;

        console.log('has enough? ',hasEnough);
        console.log('number of points:', numberOfPointsSelected);
    });


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
                span.className = 'dot';
                span.style.display = 'none';

                cell.addEventListener('click', (function (el, r, c, i) {

                    return function () {
                        //checkIfCredentialReady();

                        callback(el, r, c, i);
                    }
                })
                (cell, r, c, i), false);

                // cell.oninput= checkIfCredentialReady();
            }
        }

        return grid;
    }

    document.getElementById('loading-gif').hidden = "hidden";


};

function updatePoint(el,method,i){
    if (method==='remove'){
        el.className = '';
        setPoint(method, i);
        // points[numberOfPointsSelected] = null;
        // numberOfPointsSelected--;
        console.log(i,' unclicked');
    }else{
        // console.log(numberOfPointsSelected);
        //if (numberOfPointsSelected < MAX_NUM_POINTS) {
        el.className = 'clicked';
        setPoint(method, i);
        // points[numberOfPointsSelected] = i;
        // numberOfPointsSelected++;
        //}
        console.log(i,' clicked');
    }
}

function updateCell(el){
    // show hide selected cell's point
    let span = el.children[0];
    span.style.display = span.style.display === 'none' ? 'block' : 'none';
}

function isAlreadySelected(elem){
    return elem.className === 'clicked';

}

// assign the point to the array
// the counter for points is monitored here
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

function showImportImage(){

    document.getElementById('grid').style.display = 'block';
}

