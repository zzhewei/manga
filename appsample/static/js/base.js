$(document).ready(function(){
    /*使用者下拉式選單*/
    $('.pull_down').click(function () {
        const ul_status = document.getElementById('user_detail_id');
        if (ul_status.style.display == "none" || ul_status.style.display == "") {
        	ul_status.style.display = 'block';
        }
        else {
        	ul_status.style.display = 'none';
        }
    });
})

/*使用者下拉式選單*/
$(document).mouseup(function(e){
    if (document.getElementById('user_detail_id')){
        const _con = $('#user_detail_id');
        if(!_con.is(e.target) && _con.has(e.target).length === 0){
            document.getElementById('user_detail_id').style.display = 'none';
        }
    }
});