// Global Variables
var menu_open = false;
var nav_width = "30vw";

// Helper functions
function toggle_menu(open){
    var links = document.getElementById("nav_links");
    var content = document.getElementsByClassName('content')[0];
    if(!open){
        links.style.width = "0";
        content.style.marginLeft = "0";
    }
    else{
        links.style.width = nav_width;
        content.style.marginLeft = nav_width;
    }
    menu_open = open;
}

function setup(){
    menu_button = document.getElementById('nav_open_button');
    menu_button.onclick = function(){toggle_menu(!menu_open)};
}


// Wait for window to load then execute
window.onload = function(){
    setup();
}
