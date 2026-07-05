const element = document.getElementById("name");

let dragging = false;
let offsetX = 0;
let offsetY = 0;

element.addEventListener("mousedown", function(e){

    dragging = true;

    offsetX = e.clientX - element.offsetLeft;
    offsetY = e.clientY - element.offsetTop;

});

document.addEventListener("mousemove", function(e){

    if(!dragging) return;

    element.style.left = (e.clientX - offsetX) + "px";
    element.style.top = (e.clientY - offsetY) + "px"; 

});

document.addEventListener("mouseup", function(){

    dragging = false;

});
function savePosition(){

    const x = document.getElementById("name").offsetLeft;
    const y = document.getElementById("name").offsetTop;

    fetch("/save_position",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            x:x,
            y:y

        })

    })

    .then(response=>response.text())

    .then(data=>{

        alert(data);

    });

}