var click_indexes = [];
var key_indexes = [];

function update_keyword(elem,key_val,value) {
    if(key_val === "click"){
        if (elem.className === 'clicked') {
            addClick(value);
        }else{
            removeClick(value);
        }
    }
    else if(key_val==="keydown"){
        if(value === "Backspace"){
            removeKey(value);
        }else{

            addKey(value);
        }
    }
}

function addKey(value) {
    if(value.length>1){
        return
    }
    let i = value.toString().charCodeAt(0);
    console.log(value,i);
    let tempValue = value.toString() + '/';
    let tempKeydown = 'K' + '/';
    document.getElementById('keydown-keyword').append(tempValue);
    document.getElementById('entered-keys').append(tempKeydown);


    key_indexes.push([value, document.getElementById('entered-keys').textContent.length - 2]);

}

function removeKey(value){
        try {
            let last = key_indexes[key_indexes.length - 1][0];
            console.log(last);

            let keydown_text = document.getElementById('keydown-keyword').textContent;
            keydown_text = replaceChar(keydown_text, '', keydown_text.length - 2);
            document.getElementById('keydown-keyword').textContent = keydown_text;

            // console.log('value',last);
            // console.log('index:',getIndex(last,'keydown'));

            let entered_keys_txt = document.getElementById('entered-keys').textContent;
            let index = getIndex(last, 'keydown');
            console.log('index:', index);

            entered_keys_txt = replaceChar(entered_keys_txt, '', index[0]);
            document.getElementById('entered-keys').textContent = entered_keys_txt;
            //console.log(key_indexes[key_indexes.length-1][1]);

            key_indexes.pop();

            console.log('key indexes:', key_indexes);

        } catch (error) {
            console.log(error);
        }

    /*
        1. get the last button entered
        2. remove it from keydown txt
        3. get its index for the entered keyword
        4. remove it
     */
}

function addClick(value) {
    let tempValue = value.toString() + '/';
    let tempClick = 'C' + '/';
    document.getElementById('grid-keyword').append(tempValue);
    document.getElementById('entered-keys').append(tempClick);

    click_indexes.push([parseInt(value,10),document.getElementById('entered-keys').textContent.length-2]);

}

function removeClick(value) {
    let grid_text = document.getElementById('grid-keyword').textContent;
    grid_text = grid_text.replace(value.toString()+'/','');
    document.getElementById('grid-keyword').textContent = grid_text;

    //
    let entered_keys_txt = document.getElementById('entered-keys').textContent;
    let index = getIndex(value,'click');
    // console.log('index:',index);
    entered_keys_txt = replaceChar(entered_keys_txt,'',index[0]);
    document.getElementById('entered-keys').textContent = entered_keys_txt;

    click_indexes.splice(index[1]);
    // console.log('click indexes:',click_indexes);
}

function getIndex(value,type){
    //console.log('type:',type);
    //console.log('value:',value);

    if (type === 'click') {
        for (let i = 0; i < click_indexes.length; i++) {
            if (parseInt(value, 10) === click_indexes[i][0]) {
                let index =click_indexes[i][1];
                return [index,i];
            }
        }
    }
    else if(type === 'keydown'){
        for (let i = 0; i < key_indexes.length; i++) {
            if (value === key_indexes[i][0]) {
                return [key_indexes[i][1],i];
            }
        }
    }
    return [-1,-1]
}

function replaceChar(origString, replaceChar, index) {
    if(index !== -1) {
        let firstPart = origString.substr(0, index);
        let lastPart = origString.substr(index + 2);

        return firstPart + replaceChar + lastPart;
    }else{
        return origString;
    }
}