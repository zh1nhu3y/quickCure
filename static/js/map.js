function initMap(position) {
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    var coords = new google.maps.LatLng(lat, long);

    var mapOptions = {
        zoom: 18,
        center: coords,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    var marker = new google.maps.Marker({
        map: map,
        position: coords
    });
}

x = navigator.geolocation;
x.getCurrentPosition(initMap, failure);

function failure() {
    console.error('Error getting the user\'s location.');
}

document.getElementById("send-help-btn").addEventListener("click", function () {
    var inputBoxes = document.querySelectorAll('.send-help-input');

    var isEmpty = Array.from(inputBoxes).some(function (inputBox) {
        return inputBox.value.trim() === '';
    });

    if (isEmpty) {
        alert("Please fill in all the fields before sending help.");
    } else {
        alert("Help Sent Successfully. Please Wait for Our Contact");
        Array.from(inputBoxes).forEach(function (inputBox) {
            inputBox.value = '';
        });
    }
});