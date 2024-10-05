var debug = 0;
var socket = io();


var radarWindow = new Radar();
radarWindow.mapCanvas.update(null);

$(document).ready(() => {


    let radarElement = document.querySelector("#radar");
    makeDraggable(radarElement);

    radarElement.style.left = (window.innerWidth / 2 - (radarElement.offsetWidth / 2)) + "px";
    radarElement.style.top = (window.innerHeight / 2 - (radarElement.offsetHeight / 2)) + "px";

//    setInterval(() => {
//        radarWindow.rotation = Math.sin((new Date().getTime()) / 1000 * 0.6) * 360;
//        radarWindow.mapCanvas.draw();
//    }, 1 / 64)

    console.log("loaded");
});


socket.on("connect", function() {
    console.log('Connected to server');
    socket.send('Hello, server!');
});

socket.on("map_sync", function(data) {
//    if (debug || true) {
//        console.log("map_sync: " + data);
//    }
    radarWindow.mapCanvas.update(data);
});

socket.on("players_dot", function(data) {
//    radarWindow.config.rotation = Math.cos((new Date().getTime()) / 1000 * .4) * 360;
//    radarWindow.config.scale = 0.5 + Math.sin((new Date().getTime()) / 1000 * 1.2) * 0.5;

    radarWindow.mapCanvas.draw();
    radarWindow.playersDot.drawPlayersDot(data);
    radarWindow.aaa();

    radarWindow.players = data;
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


function Radar() {
    this.config = {
        x: 512,
        y: 512,
        scale: 1,
        rotation: 0
    };

    this.players = {};

    this.boundPlayerId = 0;
    this.bindPlayer = function(steamId) {
//        this.players["t"].concat(this.players["ct"]).forEach((playerEntity) => {
//        });
        this.boundPlayerId = steamId;
    };

    this.aaa = function() {
        if (this.boundPlayerId == 0) {
            this.config.x = 512;
            this.config.y = 512;
            this.config.rotation = 0;

            this.playersDot.tColor = this.playersDot.T_COLOR;
            this.playersDot.ctColor = this.playersDot.CT_COLOR;
        } else {
            this.players["t"].concat(this.players["ct"]).forEach((playerEntity) => {
                if (playerEntity["id"] == this.boundPlayerId) {
                    this.config.x = playerEntity["x"];
                    this.config.y = playerEntity["y"];
                    this.config.rotation = playerEntity["d"] - 90;

                    this.playersDot.tColor = (this.players["t"].indexOf(playerEntity) != -1) ? this.playersDot.TEAMMATE_COLOR : this.playersDot.ENEMY_COLOR;
                    this.playersDot.ctColor = (this.players["ct"].indexOf(playerEntity) != -1) ? this.playersDot.TEAMMATE_COLOR : this.playersDot.ENEMY_COLOR;
                };
            });
        };
    };

    this.mapCanvas = new (function(parent) {
        this.radar = parent
        this.canvas = document.querySelector("#mapCanvas");
        this.ctx = this.canvas.getContext('2d');

        this.mapImage = new Image();
        this.loadedImage = false;

        this.update = function(mapLocation) {
            this.loadedImage = false;
            this.mapImage.src = (mapLocation == null) ? "static/no_map.png" : (location.href + mapLocation);
            this.mapImage.onload = () => {
                this.loadedImage = true;
                this.draw();
            };
        };

        this.draw = function() {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            if (this.loadedImage == false) {return;}

            this.ctx.save();
            this.ctx.translate(this.canvas.width /2, this.canvas.height / 2);
            this.ctx.rotate(this.radar.config.rotation * Math.PI / 180);

            this.ctx.drawImage(
                this.mapImage,
                -this.canvas.width / (1024 / this.radar.config.x) * this.radar.config.scale,
                -this.canvas.height / (1024 / this.radar.config.y) * this.radar.config.scale,
                this.canvas.width * this.radar.config.scale,
                this.canvas.height * this.radar.config.scale
            );

            this.ctx.restore();
        }
    })(this);

    this.playersDot = new (function(parent) {
        this.T_COLOR = "#EAD28B";
        this.CT_COLOR = "#B6D4EE";
        this.TEAMMATE_COLOR = "#FFFFFF";
        this.ENEMY_COLOR = "#FF0000";

        this.radar = parent;
        this.canvas = document.querySelector("#playersDot");
        this.ctx = this.canvas.getContext('2d');

        this.tColor = this.T_COLOR;
        this.ctColor = this.CT_COLOR;

        this.drawPlayersDot = (socketData) => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

            // T
            socketData["t"].forEach((playerEntity) => {
                this.drawDot(playerEntity["x"], playerEntity["y"], this.tColor);
            });

            // CT
            socketData["ct"].forEach((playerEntity) => {
                this.drawDot(playerEntity["x"], playerEntity["y"], this.ctColor);
//                console.log(playerEntity["id"]);
            });
        };

        this.drawDot = (x, y, color) => {
            radianRotation = (this.radar.config.rotation + 180) * Math.PI / -180

            oppoX = (x - this.canvas.width / (1024 / this.radar.config.x)) * this.radar.config.scale
            oppoY = (y - this.canvas.height / (1024 / this.radar.config.y)) * this.radar.config.scale
            x = this.canvas.width / 2 - oppoX * Math.cos(radianRotation) - oppoY * Math.sin(radianRotation);
            y = this.canvas.height / 2 + oppoX * Math.sin(radianRotation) - oppoY * Math.cos(radianRotation);

            this.ctx.beginPath();
            this.ctx.arc(x, y, 8, 0, 2 * Math.PI);
            this.ctx.fillStyle = color;
            this.ctx.fill();
        };
    })(this);
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
//    document.querySelector("#player_status").classList.add("fade-in");
//    document.querySelector("#bomb_status").classList.add("fade-in");
};
setTimeout(function() {showInfoPop()}, 0);





// https://codepen.io/marcusparsons/pen/NMyzgR
function makeDraggable(element) {
    element.onmousedown = function(mouseEventDown) {
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


//    (() => {
//        let playerStatusElement = document.querySelector("#player_status");
//        makeDraggable(playerStatusElement);
//
//        playerStatusElement.style.left = (window.innerWidth / 1.3 - (playerStatusElement.offsetWidth / 2)) + "px";
//        playerStatusElement.style.top = (window.innerHeight / 2 - (playerStatusElement.offsetHeight / 2)) + "px";
//    })();
//
//    (() => {
//        let bombStatusElement = document.querySelector("#bomb_status");
//        makeDraggable(bombStatusElement);
//
//        bombStatusElement.style.left = (window.innerWidth / 2 - (bombStatusElement.offsetWidth / 2)) + "px";
//    })();


//window.ontouchstart = function(event){
//        alert("This is from the touch event");
//    }


