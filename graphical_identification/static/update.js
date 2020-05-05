var entered_keys_list = [];

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
    updateEnteredKeys()
}

function addKey(value) {
    if(value.length>1){
        return
    }

    document.getElementById('keydown-keyword').value +=  value.toString();

    let keyIndex = document.getElementById('entered-keys').value.length - 2;
    entered_keys_list.push({
        type:'keydown',
        shortType:'K',
        index:keyIndex,
        value:value,
        displayInfo : function(){
            console.log('type: ${this.name}  index:${this.index}  value:${this.value}');
        }
    });
}

function removeKey(value){
    try {
        let keydown_text = document.getElementById('keydown-keyword').value;

        //remove the last char entered
        document.getElementById('keydown-keyword').value =
            keydown_text.substring(0,keydown_text.length-1);
        entered_keys_list = remove(value,entered_keys_list,'keydown');

    } catch (error) {
        console.log(error);
    }
}

function addClick(value) {
    document.getElementById('grid-keyword').value += value.toString() + '/';

    let clickIndex = document.getElementById('entered-keys').value.length-2;

    entered_keys_list.push({
        type:'click',
        shortType:'C',
        index:clickIndex,
        value:value,
        displayInfo : function(){
            console.log('type: ${this.name}  index:${this.index}  value:${this.value}');
        }
    });
}

function removeClick(value) {
    let grid_text = document.getElementById('grid-keyword').value;
    grid_text = grid_text.replace(value.toString()+'/','');
    document.getElementById('grid-keyword').value = grid_text;

    entered_keys_list = remove(value,entered_keys_list,'click');
}

function updateEnteredKeys(){
    let out='';
    for (let i=0; i<entered_keys_list.length; i++){
        out+=entered_keys_list[i].shortType+'/';
    }
    document.getElementById('entered-keys').value=out;
}

function remove(value, arr,type){
    if(type === 'keydown'){
        for (let i = arr.length-1; i >= 0; i--) {
            if(arr[i].type === type){
                arr[i]=null;
                break;
            }
        }
    }else if(type==='click') {
        for (let i = 0; i < arr.length; i++) {
            if (arr[i].value === value) {
                console.log('arr:', arr[i], '   val:', value);
                arr[i] = null;
            }
        }
    }
    return arr.filter(function (el) {
        return el != null;
    });
}
