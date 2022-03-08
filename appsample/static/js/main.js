$(document).ready(function(){
    $('#main_content').on('click', 'button', function() {
        const btn_name = $(this).attr('class')
        const id = $(this).closest('div').attr('id');
        if (btn_name == 'modify'){
            document.getElementById('light').style.display='block';
            document.getElementById('fade').style.display='block';
            $.ajax({
                url: "/modify/"+id,
                type: "get",
                dataType: 'json',
                success: function(response) {
                    console.log(response);
                    document.getElementById("mid").value = id;
                    document.getElementById("name").value = response['data'][0]['name'];
                    document.getElementById("author").value = response['data'][0]['author'];
                    document.getElementById("group").value = response['data'][0]['author_group'];
                    document.getElementById("url").value = response['data'][0]['url'];
                    document.getElementById("pages").value = response['data'][0]['page'];
                },
                error: function(xhr) {
                //Do Something to handle error
                }
            });
        }
    })

    $('#sort_button').click(function (e) {
        $.ajax({
            url: "/sort",
            type: "get",
            success: function(response) {
                console.log(response);
                const ul = document.getElementById('main_content');
                ul.innerHTML = '';
                $.each(response['data'], function (i, member) {
                    const li = document.createElement("li");
                    const a = document.createElement('a');
                    a.setAttribute('href',member.url);
                    a.textContent= member.name;
                    const div = document.createElement('div');
                    div.setAttribute("id", member.mid);
                    const btn1 = document.createElement("button")
                    btn1.innerText = "修改";
                    btn1.className = "modify";
                    const btn2 = document.createElement("button")
                    btn2.innerText = "刪除";
                    btn2.className = "delete";
                    div.appendChild(btn1)
                    div.appendChild(btn2)
                    li.appendChild(a);
                    li.appendChild(div);
                    ul.appendChild(li);
                });
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        });
    });

    $('#add_button').click(function (e) {
        document.getElementById('light').style.display='block';
        document.getElementById('fade').style.display='block';
        document.getElementById("mid").value = '';
        document.getElementById("name").value = '';
        document.getElementById("author").value = '';
        document.getElementById("group").value = '';
        document.getElementById("url").value = '';
        document.getElementById("pages").value = '';
    });

    $('#modify_cancel').click(function (e) {
        document.getElementById('name').removeAttribute("required");
        document.getElementById('author').removeAttribute("required");
        document.getElementById('light').style.display='none';
        document.getElementById('fade').style.display='none';
    });

    $('.delete').click(function (e) {
        const id = $(this).closest('div').attr('id');
        document.getElementById("delete_mid").value = id;
        delete_dialog.showModal();
    });

    $('#delete_cancel').click(function (e) {
        delete_dialog.close();
    });

    $('#delete_confirm').click(function (e) {
        const id = $("#delete_mid").val();
        $.ajax({
            url: "/del/"+id,
            type: "get",
            dataType: 'json',
            success: function(response) {
                alert(response['data']);
                location.reload(true);
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        });
        favDialog.close();
    });
})
