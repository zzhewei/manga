$(document).ready(function(){
    const selectElement = document.querySelector('#sorted');
    const delete_dialog = document.getElementById("delete_uc_dialog");
    const modify_dialog = document.getElementById("modify_uc_dialog");

    selectElement.addEventListener('change', (event) => {
        console.log(event.target.value);
        window.location.href = "/"+window.location.href.split("/")[3]+"/user/"+window.location.href.split("/")[5]+"/"+window.location.href.split("/")[6]+"/"+event.target.value;
    });

    $('.manga_content').on('click', 'button', function() {
        console.log($(this).attr("class"));
        if ($(this).attr("class")=='item_delete'){
            $("#delete_mid").val($(this).closest('li').find(".item_mid").val());
            delete_dialog.showModal();
        }else{
            $("#mid").val($(this).closest('li').find(".item_mid").val());
            $("#name").val($(this).closest('li').find(".item_name").val());
            $("#url").val($(this).closest('li').find(".item_url").val());
            $("#pages").val($(this).closest('li').find(".item_page").val());
            $("#author").val($(this).closest('li').find(".item_author").val());
            $("#group").val($(this).closest('li').find(".item_author_group").val());
            modify_dialog.showModal();
        }
    })

    $('#delete_uc_cancel').click(function () {
        delete_dialog.close();
    });

    $('.modify_uc_dialog_cancel').click(function () {
        modify_dialog.close();
    });

    if(delete_dialog){
        delete_dialog.addEventListener('click', function (e) {
            const rect = delete_dialog.getBoundingClientRect();
            const isInDialog=(rect.top <= e.clientY && e.clientY <= rect.top + rect.height
              && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
            if (!isInDialog) {
                delete_dialog.close();
            }
        });
    }

    if(modify_dialog){
        modify_dialog.addEventListener('click', function (e) {
            const rect = modify_dialog.getBoundingClientRect();
            const isInDialog=(rect.top <= e.clientY && e.clientY <= rect.top + rect.height
              && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
            if (!isInDialog) {
                modify_dialog.close();
            }
        });
    }
})