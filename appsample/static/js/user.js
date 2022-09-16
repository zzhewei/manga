$(document).ready(function(){
    const modify_avatar_dialog = document.getElementById("modify_avatar_dialog");
    const modify_aboutme_dialog = document.getElementById("modify_aboutme_dialog");
    let cropper = '';

    $('.avatar_image').click(function () {
        modify_avatar_dialog.showModal();
    });

    $('#modify_aboutme').click(function () {
        modify_aboutme_dialog.showModal();
    });

    $('.modify_close').click(function () {
        modify_avatar_dialog.close();
        modify_aboutme_dialog.close();
    });


    if(modify_avatar_dialog){
        modify_avatar_dialog.addEventListener('click', function (e) {
            const rect = modify_avatar_dialog.getBoundingClientRect();
            const isInDialog=(rect.top <= e.clientY && e.clientY <= rect.top + rect.height
              && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
            if (!isInDialog) {
                modify_avatar_dialog.close();
                //cropper.destroy();
                //$('.preview img').remove();
            }
        });
    }


    if(modify_aboutme_dialog){
        modify_aboutme_dialog.addEventListener('click', function (e) {
            const rect = modify_aboutme_dialog.getBoundingClientRect();
            const isInDialog=(rect.top <= e.clientY && e.clientY <= rect.top + rect.height
              && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
            if (!isInDialog) {
                modify_aboutme_dialog.close();
            }
        });
    }


    /*頭像*/
    $('input[type="file"]').change(function() {
        let preview = document.querySelector('.preview');
        const file = $(this)[0].files[0];
        const reader = new FileReader;

        reader.onload = function(e) {
            let img = document.createElement('img');
			img.id = 'select_image';
			img.src = e.target.result
			// clean result before
			preview.innerHTML = '';
			// append new image
            preview.appendChild(img);
            cropper = new Cropper(img);
         };
        reader.readAsDataURL(file);
    });

    $('#modify_avatar_save').click(function () {
        if (cropper) {
            // 取得裁切的圖並轉成base64
            let imgSrc = cropper.getCroppedCanvas({ width: 300 }).toDataURL();
            //console.log(imgSrc);
            $("#avatar_base64").val(imgSrc);
        }
        else{
            alert('Upload Avatar Please!');
        }
    });
    /*=============================*/

})