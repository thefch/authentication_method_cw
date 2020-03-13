

//function loadGrid(elem) {
window.onload = () => {
    var lastClicked;
    //console.log('grid:',elem);
    var grid = clickableGrid(10, 10, function (el, row, col, i) {
        console.log("You clicked on item:", i);

        update_keyword('click',i);
        //document.getElementById('entered-password').append(r);
        //console.log(document.getElementById('entered-password').textContent);


        el.className = 'clicked';
        if (lastClicked)
            lastClicked.className = '';
        lastClicked = el;
    });

    document.body.appendChild(grid);

    //init clickable grid
    function clickableGrid(rows, cols, callback) {
        var i = 0;
        var grid = document.createElement('table');
        grid.className = 'grid';
        grid.id = 'grid-id';

        for (var r = 0; r < rows; ++r) {
            var tr = grid.appendChild(document.createElement('tr'));

            for (var c = 0; c < cols; ++c) {
                var cell = tr.appendChild(document.createElement('td'));
                cell.className = 'cell';
                cell.id = 'cell-id';
                cell.style.borderStyle = 'hidden';
                cell.value = ++i;
                //cell.onclick();
                cell.addEventListener('click', (function (el, r, c, i) {

                    return function () {
                        callback(el, r, c, i);

                    }

                })(cell, r, c, i), false);
            }
        }

        return grid;
    }
};

