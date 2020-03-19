

//function loadGrid(elem) {
window.onload = () => {
    let rowsCols = 40;
    let lastClicked;
    //console.log('grid:',elem);
    const grid = clickableGrid(rowsCols, rowsCols, function (el, row, col, i) {
        console.log("You clicked on item:", i);

        update_keyword('click', i);
        //document.getElementById('entered-password').append(r);
        //console.log(document.getElementById('entered-password').textContent);


        el.className = 'clicked';

        // show hide selected cell's point
        var span = el.children[0];
        span.style.display = span.style.display === 'none' ? 'block' : 'none';

        if (lastClicked)
            lastClicked.className = '';
        lastClicked = el;

        // document.getElementById(el.id).style.borderStyle = "solid";

    });

    document.body.appendChild(grid);

    //init clickable grid
    function clickableGrid(rows, cols, callback) {
        let i = 0;
        const grid = document.createElement('table');
        grid.className = 'grid';
        grid.id = 'grid-id';

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
};

