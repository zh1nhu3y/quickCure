let image = document.getElementById("image");
let imageFile = document.getElementById("home-image");
let imageContainer = document.getElementById("image-container");
let loadingImage = document.getElementById("loading-image");
const firstAidProcedureBtn = document.querySelector('#minor-injury-modal .send-help-btn');

imageFile.onchange = function() {
    // Loop through each uploaded file
    for (let i = 0; i < imageFile.files.length; i++) {
        let filename = imageFile.files[i].name;
        console.log(filename);
        
        // Check if the filename contains "minor-burn.jpg"
        if (filename.includes("minor-burn.jpg")) {
            setTimeout(() => {
                loadingImage.classList.add("display-none");
                $('#minor-injury-modal').modal('show');
            }, 2000);
            firstAidProcedureBtn.onclick = function () {
                window.location.href = "/contentPage/5";
            };
        } else if (filename.includes("knife-cut.jpg")) {
            setTimeout(() => {
                loadingImage.classList.add("display-none");
                $('#minor-injury-modal').modal('show');
            }, 2000);
            firstAidProcedureBtn.onclick = function () {
                window.location.href = "/contentPage/3";
            };

        } else {
            setTimeout(() => {
                loadingImage.classList.add("display-none");
                $('#major-injury-modal').modal('show');
            }, 2000);
        }

        // Display the image and loading animation for each uploaded file
        image.src = URL.createObjectURL(imageFile.files[i]);
        imageContainer.classList.remove("display-none");
        image.classList.remove("display-none");
        image.classList.add("loading-img");
        loadingImage.classList.remove("display-none");
    }

    // Reset the modal trigger and event handlers when the modal is closed
    $('#minor-injury-modal').on('hidden.bs.modal', function () {
        // Hide the image and loading animation after the modal is closed
        image.classList.add("display-none");
        location.reload();
    });

    $('#major-injury-modal').on('hidden.bs.modal', function () {
        // Hide the image and loading animation after the modal is closed
        image.classList.add("display-none");
        location.reload();
    });
};