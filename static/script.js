var debug = 0;
var socket = io();

socket.on("connect", function() {
    console.log('Connected to server');
    socket.send('Hello, server!');
});

socket.on("map_sync", function(data) {
    if (debug && false) {
//        console.log("map_sync: " + data);
    }
    map_sync(data);
});

socket.on("players_pos", function(data) {
    if (debug && false) {
//        console.log("players_pos: " + data);
    }
    draw(data);
});

socket.on("bomb_status", function(data) {
    if (debug) {
        console.log("[bomb_status] bomb_planted: " + data["planted"] + ", time_left: " + data["time_left"] + ", defusing: " + data["defusing"] + ", defuse_time_left: " + data["defuse_time_left"]);
    };
});

socket.on("bomb_beep", function(data) {
    if (debug) {
        console.log("[bomb_beep] Beep: " + data["beep_span"]);
    };
});


function map_sync(map_location) {
    source_url = location.href + map_location;

    map_object = document.querySelector("#map_image");
    if (map_object.src != source_url) {
        map_object.src = source_url;
    };
};


var canvas = document.querySelector("#overlay");
var ctx = canvas.getContext('2d');

function drawCircle(x, y, color) {
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
};

function draw(socketData) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // T
    socketData["t"].forEach(function(playerEntity) {
        drawCircle(playerEntity["x"], playerEntity["y"], '#EAD28B');
    });

    // CT
    socketData["ct"].forEach(function(playerEntity) {
        drawCircle(playerEntity["x"], playerEntity["y"], '#B6D4EE');
    });
};

function showInfoPop() {
    infoPop = document.getElementById("info_pop");

    infoPop.classList.remove("fade-out");
    infoPop.classList.add("fade-in");
};

function hideInfoPop() {
    infoPop = document.getElementById("info_pop");

    infoPop.classList.remove("fade-in");
    infoPop.classList.add("fade-out");

    document.querySelector("#radar").classList.add("fade-in");
    document.querySelector("#bomb_status").classList.add("fade-in");
};
setTimeout(function() {showInfoPop()}, 0);





// https://codepen.io/marcusparsons/pen/NMyzgR
function makeDraggable(element) {
    element.onmousedown = function(mouseEventDown) {
        console.log("ayo");

        let elementStartX = mouseEventDown.clientX - element.offsetLeft;
        let elementStartY = mouseEventDown.clientY - element.offsetTop;

        onmousemove = function(mouseEventMove) {
            let targetX = mouseEventMove.clientX - elementStartX;
            let targetY = mouseEventMove.clientY - elementStartY;

            if (targetX < 0) {
                targetX = 0;
            }
            if ((targetX + element.offsetWidth) > window.innerWidth) {
                targetX = window.innerWidth - element.offsetWidth;
            }
            if (targetY < 0) {
                targetY = 0;
            }
            if ((targetY + element.offsetHeight) > window.innerHeight) {
                targetY = window.innerHeight - element.offsetHeight;
            }

            element.style.left = targetX + 'px';
            element.style.top = targetY + 'px';
        };

        element.onmouseup = function(mouseEventUp) {
            onmousemove = null;
            element.ontouchmove = null;
        };
    };
};


window.onload = function() {
    (() => {
        let radarElement = document.querySelector("#radar");
        makeDraggable(radarElement);

        radarElement.style.left = (window.innerWidth / 2 - (radarElement.offsetWidth / 2)) + "px";
        radarElement.style.top = (window.innerHeight / 2 - (radarElement.offsetHeight / 2)) + "px";
    })();


    (() => {
        let bombStatusElement = document.querySelector("#bomb_status");
        makeDraggable(bombStatusElement);

        bombStatusElement.style.left = (window.innerWidth / 2 - (bombStatusElement.offsetWidth / 2)) + "px";
    })();

    console.log("loaded");
};

//window.ontouchstart = function(event){
//        alert("This is from the touch event");
//    }


