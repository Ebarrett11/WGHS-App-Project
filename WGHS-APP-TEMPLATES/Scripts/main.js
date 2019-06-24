var account_button_open = false;



function toggle_dropdown(child, open){
    if (!open) {
        child.style.display = "block";
    }
    else {
        child.style.display = "none";
    }
}

function setup(){
    var account_button_dropdown = document.getElementById('account_button_dropdown');
    var account_icon = document.getElementById('account_button_container');

    account_icon.onclick= function(){
        toggle_dropdown(account_button_dropdown, account_button_open);
        account_button_open = !account_button_open;
    }
}


window.onload = function(){
    setup();
}
