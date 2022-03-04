function sort(){
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

function modify(){
    document.getElementById('light').style.display='block';
    document.getElementById('fade').style.display='block';
}