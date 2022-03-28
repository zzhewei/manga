function ChangeMainView(response){
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
        btn1.className = "modify";
        btn1.innerHTML = "<i class='fas fa-pen'></i>";
        const btn2 = document.createElement("button")
        btn2.className = "delete";
        btn2.innerHTML = "<i class='far fa-trash-alt'></i>";
        div.appendChild(btn1);
        div.appendChild(btn2);
        li.appendChild(a);
        li.appendChild(div);
        ul.appendChild(li);
    });
}

$(document).ready(function(){
    $('#search_input').on('input', function() {
        text = $('#search_input').val();
        csrf_token = $('#csrf_token').val();
        $.ajax({
            url: "/zh/fuzzy",
            headers: {'X-CSRF-TOKEN': csrf_token},
            type: "post",
            contentType: 'application/json; charset=UTF-8',
            data: JSON.stringify({"input": text}),
            success: function(response) {
                /*ChangeMainView(response);*/
                $("#main_content").html(response);
            },
            error: function(xhr) {
                alert("Search error");
            }
        });
    });

    $('.pull_down').click(function () {
        const ul_status = document.getElementById('user_detail_id');
        if (ul_status.style.display == "none" || ul_status.style.display == "") {
        	ul_status.style.display = 'block';
        }
        else {
        	ul_status.style.display = 'none';
        }
    });

    $('#main_content').on('click', 'button', function() {
        const btn_name = $(this).attr('class')
        const id = $(this).closest('div').attr('id');
        if (btn_name == 'modify'){
            document.getElementById('form_content').style.display='block';
            document.getElementById('overlay').style.display='block';
            $.ajax({
                url: "/zh/modify/"+id,
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
                    alert("Modify error");
                }
            });
        }
        else if (btn_name == 'delete'){
            document.getElementById("delete_mid").value = id;
            console.log(id);
            delete_dialog.showModal();
        }
    })

    $('#sort_button').click(function () {
        $.ajax({
            url: "/zh/sort",
            type: "get",
            success: function(response) {
                /*ChangeMainView(response);*/
                $("#main_content").html(response);
            },
            error: function(xhr) {
                alert("Sort error");
            }
        });
    });

    $('#add_button').click(function () {
        document.getElementById('form_content').style.display='block';
        document.getElementById('overlay').style.display='block';
        document.getElementById("mid").value = '';
        document.getElementById("name").value = '';
        document.getElementById("author").value = '';
        document.getElementById("group").value = '';
        document.getElementById("url").value = '';
        document.getElementById("pages").value = '';
    });

    $('#modify_cancel').click(function () {
        document.getElementById('name').removeAttribute("required");
        document.getElementById('author').removeAttribute("required");
        document.getElementById('form_content').style.display='none';
        document.getElementById('overlay').style.display='none';
    });

    $("#overlay").click(function(){
        document.getElementById('form_content').style.display='none';
        document.getElementById('overlay').style.display='none';
    });


    $('#delete_cancel').click(function () {
        delete_dialog.close();
    });

    $('#delete_confirm').click(function () {
        const id = $("#delete_mid").val();
        $.ajax({
            url: "/zh/del/"+id,
            type: "get",
            success: function(response) {
                $("#main_content").html(response);
            },
            error: function(xhr) {
                alert("Del error");
            }
        });
        delete_dialog.close();
    });

    delete_dialog.addEventListener('click', function (e) {
        const rect = delete_dialog.getBoundingClientRect();
        const isInDialog=(rect.top <= e.clientY && e.clientY <= rect.top + rect.height
          && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
        if (!isInDialog) {
            delete_dialog.close();
        }
    });
})


$(document).mouseup(function(e){
    const _con = $('#user_detail_id');
    if(!_con.is(e.target) && _con.has(e.target).length === 0){
        document.getElementById('user_detail_id').style.display = 'none';
    }
});