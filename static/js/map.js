function initMap(position) {

    var lat = 3.1481978;
    var long = 101.7066028;
    // var lat = position.coords.latitude;
    // var long = position.coords.longitude;
    var coords = new google.maps.LatLng(lat, long);

    var mapOptions = {
        zoom: 18,
        center: coords,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        // mapId: '1a71b73e298251e4',
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions)

    var nMarker = new google.maps.Marker({
        map: map,
        position: coords,
        title:  "Current Location",
    });

    var markers = [
        [
            "ambulance 1",
            3.0428962392259953,
            101.70030961475776,
            "static/image/ambulance.svg",
            40,
            31
        ],
        [
            "ambulance 2",
            3.043260494316724,
            101.6968763631588,
            "static/image/ambulance.svg",
            40,
            32
        ],
        [
            "ambulance 3",
            3.043260494316724,
            101.6968763631588,
            "static/image/ambulance.svg",
            40,
            32
        ],

    ];

    for (let i = 0; i < markers.length; i++) {
        var currMarker = markers[i];

        var marker = new google.maps.Marker({
            map: map,
            position: new google.maps.LatLng(currMarker[1], currMarker[2]),
            title: currMarker[0],
            icon: {
                url: currMarker[3],
                scaledSize: new google.maps.Size(currMarker[4], currMarker[5])
            },
        });
    }


}

x = navigator.geolocation;
x.getCurrentPosition(initMap, failure);

function failure() {
    console.error('Error getting the user\'s location.');
}

// document.getElementById("send-help-btn").addEventListener("click", function () {
//     var inputBoxes = document.querySelectorAll('.required-input');

// var isEmpty = Array.from(inputBoxes).some(function (inputBox) {
//     return inputBox.value.trim() === '';
// });

// if (isEmpty) {
//         alert("Please fill in all the fields before sending help.")
//     } else {
//         $('#send-help-modal').modal('show');

//         Array.from(inputBoxes).forEach(function (inputBox) {
//             inputBox.value = '';
//         });
//     }
// });

document.getElementById("send-help-close").addEventListener("click", function () {
    window.location.href = "/majorSendHelp"
})

let image = document.getElementById("image");
let imageFile = document.getElementById("image-file");
let imageContainer = document.getElementById("image-container");
let loadingImage = document.getElementById("loading-image");
let sendHelpBtn = document.getElementById("send-help-btn");
let currentCondition = document.getElementById("current-condition");
const firstAidProcedureBtn = document.querySelector('#minor-injury-modal .send-help-btn');

imageFile.onchange = function(){
    image.src = URL.createObjectURL(imageFile.files[0]);
    imageContainer.classList.remove("display-none");
    image.classList.remove("display-none");
}

function clearInput() {
    const inputBoxes = document.querySelectorAll('.send-help-input');
    Array.from(inputBoxes).forEach((inputBox) => (inputBox.value = ''));
    imageContainer.classList.add("display-none");
    image.classList.add("display-none");
}

function loading(){
    sendHelpBtn.disabled = true;
    image.classList.add("loading-img");
    loadingImage.classList.remove("display-none");

    setTimeout(() => {
        sendHelpBtn.disabled = false;
        image.classList.remove("loading-img");
        loadingImage.classList.add("display-none");
    }, 2000);
}

function minorInjuryModal() {
    setTimeout(() => {
        $('#minor-injury-modal').modal('show');
        clearInput();
    }, 2000);
}

function sendHelpModal() {
    setTimeout(() => {
        $('#send-help-modal').modal('show');
        clearInput();
    }, 2000);
}

sendHelpBtn.onclick = function () {
    console.log("button clicked")

        var requiredInputs = document.querySelectorAll(".required-input");

        var isEmpty = false;
    
        requiredInputs.forEach(function(input) {
            if (input.value.trim() === '') {
                isEmpty = true;
            }
        });
    
        if (isEmpty) {
            window.alert("Please fill in all the fields before sending help.");
            return;
        }
    if (currentCondition.value == 'burn') {
        loading();
        minorInjuryModal();
        firstAidProcedureBtn.onclick = function () {
            window.location.href = "/contentPage/5";
        };

    } else if (currentCondition.value == 'nose bleeding') {
        loading();
        minorInjuryModal();
        firstAidProcedureBtn.onclick = function () {
            window.location.href = "/contentPage/6";
        };

    } else {
        loading();
        sendHelpModal();
    }
};
