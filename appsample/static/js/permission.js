$(document).ready(function(){
    $("li").on("click",function() {
        showLoader();
        $("#loading-content").load("dataSearch.php?"+this.id, hideLoader);
    });
})