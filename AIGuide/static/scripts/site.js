function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        .replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
}

var client_id = uuidv4()

$(document).ready(function () {

    $("#btnSpeak").click(function () {
        var isStopped = true;
        var url = "/home/speak/start";
        //$("#hdnKeeprun").val("YES");
        //keepRunWhile();
        if (!$(this).hasClass("speak")) {
            url = "/home/speak/stop";
            $(this).css("color", "#428bca");
            $("#icnSpeak").attr("class", "bi bi-mic")
            isStopped = true;
        }
        else {
            //$(this).text("Stop");
            $(this).css("color", "#99062d");
            $("#icnSpeak").attr("class", "bi bi-stop-circle")
        }

        $(this).toggleClass("speak");

        $.get(url,
            function (data, status) {
                console.log(data.airesp);
                if (isStopped === true) {
                    //$("#hdnKeeprun").val("NO");
                    console.log(data.airesp);
                    //$("#txtPrompt").val(data.airesp);
                }
            }
        );
    });

    $("#btnMore").click(function () {
        var isSpeech = true;// document.getElementById("icnSpeaker").classList.contains("bi-volume-up");
        var url = "/home/askmore?isSpeech=" + isSpeech;
        $.get(url,
            function (data, status) {
                console.log(data.airesp);
            }
        );
    });

    $("#btnhtmlSave").click(function () {
        /*var url = "/home/save/html";
        $.get(url,
            function (data, status) {
                console.log(data.airesp);
            }
        );*/
        const downloadableContent = document.getElementById("hdnHistory");
        const content = downloadableContent.value;
        if (content) {
            const blob = new Blob([content], { type: "text/html" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "iguide_exp.md";
            a.click();
        }
    });

    $("#btnhtmlImport").click(function () {
        const fileInput = document.getElementById('fileInput');
        fileInput.click();
    });
});

////function keepRunWhile() {
////    setInterval(null, 5000);
//    while ($("#hdnKeeprun").val() == "YES") {
//        setTimeout(function () {
//            keepread();
//        }, 2000);
//    }
////}

//function keepread() {
//    url = "/home/read";
//    $.get(url,
//        function (data, status) {
//            $("#txtPrompt").val(data.airesp);
//        }
//    );
//}



document.addEventListener('DOMContentLoaded', (event) => {

    //Set ClientId
    $.get("/home/setclient/" + client_id,
        function (data, status) {
            console.log(data.airesp);
        }
    );

    var socket = io();
    socket.on('connect', function () {
        console.log('Connected to server');
    });
    socket.on('message', function (msg) {
        console.log('Message received: ' + msg);
        $("#txtPrompt").val($("#txtPrompt").val() + msg + ". ");
    });
    socket.on('disconnect', function () {
        console.log('Disconnected from server');
    });
    socket.on('Cust_resp' + client_id, function (data, from) {
        //console.log('Cust_resp Message received: ' + data.data);
        $("#txtPrompt").val($("#txtPrompt").val() + data.data + ". ");
    });
    socket.on('Cust_resp_audio' + client_id, function (data, from) {
        console.log('Cust_resp audio Message received: ' + data.data);
    });
    socket.on('Cust_resp_AI' + client_id, function (data, from) {
        //console.log('Cust_resp_AI Message received: ' + data.data);
        $("#txtResp").append(data.data);
        if ($("#hdnHistory").val()) {
            $("#hdnHistory").val($("#hdnHistory").val() + "\n\n" + data.history);
        }
        else {
            $("#hdnHistory").val(data.history);
        }
        renderMarkdown();
        setCopyBtn();
        setImages();
        playAudio();
        //$("#txtResp").find("SVG").attr("fill", "#fff");
    });
    socket.on('Cust_resp_select' + client_id, function (data, from) {
        console.log('Cust_resp_select Message received: ' + data.data);
        //var srcWords = data.data.trim().split(' ');
        //var twoWords = srcWords[0] + " " + srcWords[1]
        /*$("h1").css("color", "#fff");
        $("h2").css("color", "#fff");
        $("p").css("color", "#fff");
        $("li").css("color", "#fff");

        $("h1:contains('" + data.data.trim() + "')").focus();
        $("h2:contains('" + data.data.trim() + "')").focus();
        $("p:contains('" + data.data.trim() + "')").focus();
        $("li:contains('" + data.data.trim() + "')").focus();*/

        /*$("h1:contains('" + data.data.trim() + "')").css("color", "#f00");
        $("h2:contains('" + data.data.trim() + "')").css("color", "#f00");
        $("p:contains('" + data.data.trim() + "')").css("color", "#f00");
        $("li:contains('" + data.data.trim() + "')").css("color", "#f00");*/

        $("*").removeClass("read-highlight");

        //$('*').each(function () {
        $("*:contains('" + data.data.trim() + "')").addClass("read-highlight");
        //});

    });
    function sendMessage(message) {
        //var msg = document.getElementById('message').value;
        socket.send(message);
    }

    //Dom Events
    document.getElementById("btnAsk").addEventListener('click', (event) => {
        document.getElementById("audSrc").src = "";
        //$("#btnSpeak").text("Speak");
        $("#txtResp").val("");
        $("#btnSpeak").addClass("speak");
        //$("#hdnKeeprun").val("NO");
        /*$.get("/home/ask/" + $("#txtPrompt").val(),
            function (data, status) {
                //$("#txtResp").val(data.airesp)
            }
        );*/

        var isSpeech = true;// document.getElementById("icnSpeaker").classList.contains("bi-volume-up");

        var prmpt = $("#txtPrompt").val();
        var reqst = { "prompt": prmpt, isSpeech: isSpeech, "history": $("#hdnHistory").val() };
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/home/ask',
            dataType: 'json',
            data: JSON.stringify(reqst),
            success: (data) => {
                //console.log('isChat response: ' + data)
                document.getElementById("audSrc").src = "static/audio/" + client_id + ".wav";
                playAudio();
                $("#txtPrompt").val("");
            },
            error: (data) => {
                console.log(data)
            }
        });
    });

    document.getElementById("btnClrResult").addEventListener("click", (event) => {
        document.getElementById("txtResp").innerHTML = "";
    });

    /*document.getElementById("icnSpeaker").addEventListener("click", (event) => {
        if (document.getElementById("icnPlay").classList.contains("bi-play") && event.target.classList.contains("bi-volume-up")) {
            playAudio();
        }
        else {
            pauseAudio();
        }
        event.target.classList.toggle("bi-volume-up");
        //event.target.classList.toggle("bi-volume-mute");
    });

    document.getElementById("icnPlay").addEventListener("click", (event) => {
        if (event.target.classList.contains("bi-play") && document.getElementById("icnSpeaker").classList.contains("bi-volume-up")) {
            playAudio();
        }
        else {
            pauseAudio();
        }
        //event.target.classList.toggle("bi-play");
        //event.target.classList.toggle("bi-pause");
    });*/    

    const fileInput = document.getElementById('fileInput');
    const fileContentDiv = document.getElementById('hdnHistory');
    console.log("fileInput", fileInput);
    fileInput.addEventListener('change', (e) => {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = (event) => {
            const fileText = event.target.result;
            fileContentDiv.value = fileText;
            $("#txtResp").html(fileText);
            renderMarkdown();
            setCopyBtn();
            //setImages();
            //playAudio();
        };

        reader.readAsText(file);
    });

});

function setCopyBtn() {
    const copyButtonLabel = "Copy Code";

    // use a class selector if available
    let blocks = document.querySelectorAll("pre");

    blocks.forEach((block) => {
        // only add button if browser supports Clipboard API
        const extBtn = block.getElementsByTagName('button')
        if (extBtn.length <= 0) {
            if (navigator.clipboard) {
                let button = document.createElement("button");
                button.style.color = "#000"; // set text color to white
                //button.style.width = "30px";
                //button.style.height = "30px";
                button.style.margin = "2em auto";
                button.style.textAlign = "right";
                button.innerText = 'Copy';
                block.appendChild(button);

                button.addEventListener("click", async () => {
                    button.value = "Copied";
                    await copyCode(block);
                });
            }
        }
    });
}

async function copyCode(block) {
    let code = block.querySelector("code");
    let text = code.innerText;

    await navigator.clipboard.writeText(text);
}

var audio = document.getElementById("myAudio");

function playAudio(src) {
    if (audio && document.getElementById("audSrc")) {
        audio.src = document.getElementById("audSrc").src;
        audio.play();
        //document.getElementById("icnPlay").classList.remove("bi-play");
        //document.getElementById("icnPlay").classList.add("bi-pause");
    }
}

function pauseAudio() {
    audio.pause();
    document.getElementById("icnPlay").classList.add("bi-play");
    document.getElementById("icnPlay").classList.remove("bi-pause");
}

function stopAudio() {
    audio.pause();
    audio.currentTime = 0;
    document.getElementById("icnPlay").classList.add("bi-play");
    document.getElementById("icnPlay").classList.remove("bi-pause");
}

function setImages() {
    event.preventDefault();
    const respTag = document.getElementById("txtResp");
    let images = respTag.getElementsByTagName('img');
    for (var idx = 0; idx < images.length; idx++) {
        const alttext = image.alt;
        const slider = document.createElement("div");
        slider.className = "iguide-slider";
        slider.id = "iguide-slider" + idx;
        image.parentNode.replaceChild(slider, image);
        iguideslider("iguide-slider" + idx, "/searchimage/" + alttext);
    }
}

//Loader Scripts
const message1 = document.getElementById('message-1')
const tip1 = document.getElementById('tip-1')

const messages = [
    'Now Loading',
    'Now Loading.',
    'Now Loading..',
    'Now Loading...'
]

let i = 0

function showMessage_1() {
    if (i == 4) { i = 0 }
    message1.textContent = messages[i]
    i++
}

setInterval(showMessage_1, 500)