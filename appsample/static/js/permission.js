$(document).ready(function(){
    const modify_permission_dialog = document.getElementById("modify_permission_dialog");

    $('#user_content li button').click(function () {
        $("#account").val($(this).closest('div').parent().find(".account_p").text());
        $("#permission_input").val($(this).closest('div').parent().find(".permission_p").text());
        modify_permission_dialog.showModal();
    });

    if(modify_permission_dialog){
        modify_permission_dialog.addEventListener('click', function (e) {
            const rect = modify_permission_dialog.getBoundingClientRect();
            const isInDialog=(rect.top <= e.clientY && e.clientY <= rect.top + rect.height
              && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
            if (!isInDialog) {
                modify_permission_dialog.close();
            }
        });
    }
})