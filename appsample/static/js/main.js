function sort(){
    var myList = document.getElementById('main_content');
    myList.innerHTML = '';
    var li = document.createElement("li");
    var aTag = document.createElement('a');
    aTag.setAttribute('href',"https://stackoverflow.com/questions/45193524/how-to-add-a-tag-and-href-using-javascript");
    aTag.textContent= "link text";
    var iDiv = document.createElement('div');
    li.appendChild(aTag);
    myList.appendChild(li);
    $.ajax({
      url: "/sort",
      type: "get",
      data: {"ajax": "test"},
      success: function(response) {
        alert("success");

      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

function modify(rev){
    document.getElementById('light').style.display='block';
    document.getElementById('fade').style.display='block';
    $.ajax({
      url: "/"+rev.id,
      type: "get",
      dataType: 'json',
      success: function(response) {
        console.log(response);
        document.getElementById("mid").value = rev.id;
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

function cancel(){
    document.getElementById('light').style.display='none';
    document.getElementById('fade').style.display='none';
}

function cancel(){
    document.getElementById('light').style.display='none';
    document.getElementById('fade').style.display='none';
}