$(document).ready(function(){
    const delete_dialog = document.getElementById("delete_dialog");
    const modify_dialog = document.getElementById("modify_dialog");

    $('#search_input').on('input', function() {
        text = $('#search_input').val();
        csrf_token = $('#csrf_token').val();
        if (text != ""){
            $.ajax({
                url: "/zh/fuzzy",
                headers: {'X-CSRF-TOKEN': csrf_token},
                type: "post",
                contentType: 'application/json; charset=UTF-8',
                data: JSON.stringify({"input": text}),
                success: function(response) {
                    $("#main_content").html(response);
                },
                error: function(xhr) {
                    alert("Search error");
                }
            });
        }
    });

    $('#main_content').on('click', 'button', function() {
        const btn_name = $(this).attr('class');
        const id = $(this).closest('li').find(".item_mid").val();
        if (btn_name.includes('modify')){
            $("#mid").val(id);
            $("#name").val($(this).closest('li').find(".item_name").val());
            $("#url").val($(this).closest('li').find(".item_url").val());
            $("#pages").val($(this).closest('li').find(".item_page").val());
            $("#author").val($(this).closest('li').find(".item_author").val());
            $("#group").val($(this).closest('li').find(".item_author_group").val());
            modify_dialog.showModal();
        }
        else if (btn_name.includes('delete')){
            $("#delete_mid").val(id);
            console.log(id);
            delete_dialog.showModal();
        }
    })

    $('#add_button').click(function () {
        document.getElementById("mid").value = '';
        document.getElementById("name").value = '';
        document.getElementById("author").value = '';
        document.getElementById("group").value = '';
        document.getElementById("url").value = '';
        document.getElementById("pages").value = '';
        modify_dialog.showModal();
    });

    $('#modify_cancel').click(function () {
        document.getElementById('name').removeAttribute("required");
        document.getElementById('author').removeAttribute("required");
        modify_dialog.close();
    });

    $('#delete_cancel').click(function () {
        delete_dialog.close();
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
