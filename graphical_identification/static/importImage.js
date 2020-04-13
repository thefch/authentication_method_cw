function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        var filename = $("#import-img").val();
        filename = filename.substring(filename.lastIndexOf('\\')+1);
        reader.onload = function(e) {
            $('#external-image').attr('src', e.target.result);
            $('#external-image').hide();
            $('#external-image').fadeIn(500);

        };
        reader.readAsDataURL(input.files[0]);
    }
}

function setStyle() {
    console.log('set style');
    document.getElementById('images-tb').style.display = 'none';
    document.getElementById('external-image-container').style.display = 'block';

    document.getElementById('img_file-btn').type = 'submit';
    document.getElementById('import-img').style.visibility='hidden';
}

function previewImage(input){

    readURL(input);
    setStyle();
}

function closeImage(elem){
    console.log('close imported image.');

    document.getElementById('images-tb').style.display = 'block';
    document.getElementById('external-image-container').style.display = 'none';

    document.getElementById('import-img').src ='';
    document.getElementById('import-img').style.visibility='visible';

    document.getElementById('import-img').value = '';


    document.getElementById('img_file-btn').type = 'hidden';
    document.getElementById('resolution-msg').style.visibility = 'hidden';
}