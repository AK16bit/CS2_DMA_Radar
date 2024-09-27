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
    map_sync(data)
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
    }
})

socket.on("bomb_beep", function(data) {
    if (debug) {
        console.log("[bomb_beep] Beep: " + data["beep_span"]);
    }
})




function map_sync(map_location) {
    source_url = location.href + map_location

    map_object = document.querySelector("#map_image")
    if (map_object.src != source_url) {
        map_object.src = source_url
    }
}


var canvas = document.getElementById("overlay");
var ctx = canvas.getContext('2d');

function drawCircle(x, y, color) {
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
}

function draw(socketData) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // T
    socketData["t"].forEach(function(playerEntity) {
        drawCircle(playerEntity["x"], playerEntity["y"], '#EAD28B')
    })

    // CT
    socketData["ct"].forEach(function(playerEntity) {
        drawCircle(playerEntity["x"], playerEntity["y"], '#B6D4EE')
    })
}

function showInfoPop() {
    infoPop = document.getElementById("info_pop")

    infoPop.classList.remove("fade-out");
    infoPop.classList.add("fade-in");
}

function hideInfoPop() {
    infoPop = document.getElementById("info_pop")

    infoPop.classList.remove("fade-in");
    infoPop.classList.add("fade-out");

    document.getElementById("radar").classList.add("fade-in")
}
setTimeout(function() {showInfoPop()}, 0)

