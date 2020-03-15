function displayGrid(elem) {
    console.log('Grid status:',elem.checked);
    if (elem.checked){
        showGrid();
    }else{
        hideGrid();
    }
}

function showGrid(){

    let cells = document.getElementsByClassName("cell");
    for(let i=0;i<cells.length;i++){
        cells[i].style.borderStyle = 'solid';
    }

    document.getElementById("gridOnID").style.visibility = 'visible';
    document.getElementById("gridOffID").style.visibility = 'hidden';
}

function hideGrid(){
    let cells = document.getElementsByClassName("cell");
    for(let i=0;i<cells.length;i++){
        cells[i].style.borderStyle = 'hidden';
    }

    document.getElementById("gridOnID").style.visibility = 'hidden';
    document.getElementById("gridOffID").style.visibility = 'visible';

}

function showHidePoint(elem){
    console.log('in show hide point');
    if(elem.style.display === '')
        elem.style.display = 'block';
    else elem.style.display = elem.style.display === 'none' ? 'block' : 'none'
}