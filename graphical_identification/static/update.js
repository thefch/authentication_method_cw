function update_keyword(elem,value) {

    if(elem === "click"){
        document.getElementById('grid-keyword').append(value);
        document.getElementById('entered-keys').append('click ');

    }
    else if(elem==="keydown"){
        document.getElementById('keydown-keyword').append(value);

        document.getElementById('entered-keys').append('key ');
    }
    //document.getElementById('entered-password').append(value);
    //console.log(document.getElementById('entered-password').textContent);
}