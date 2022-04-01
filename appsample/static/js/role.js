$(document).ready(function(){
    const modify_role_dialog = document.getElementById("modify_role_dialog");

    $('#user_content li button').click(function () {
        $("#uid").val($(this).closest('div').parent().find(".user_id").val());
        $("#username").val($(this).closest('div').parent().find(".username_p").text());
        document.getElementById('userrole').value=$(this).closest('div').parent().find(".role_id").val();
        modify_role_dialog.showModal();
    });

    $('.modify_role_dialog_cancel').click(function () {
        modify_role_dialog.close();
    });

    if(modify_role_dialog){
        modify_role_dialog.addEventListener('click', function (e) {
            const rect = modify_role_dialog.getBoundingClientRect();
            const isInDialog=(rect.top <= e.clientY && e.clientY <= rect.top + rect.height
              && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
            if (!isInDialog) {
                modify_role_dialog.close();
            }
        });
    }
})