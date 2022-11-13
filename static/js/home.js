document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
        inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
        if (inputElement.files.length) {
            updateThumbnail(dropZoneElement, inputElement.files[0]);
        }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
        dropZoneElement.addEventListener(type, (e) => {
            dropZoneElement.classList.remove("drop-zone--over");
        });
    });

    dropZoneElement.addEventListener("drop", (e) => {
        e.preventDefault();

        if (e.dataTransfer.files.length) {
            inputElement.files = e.dataTransfer.files;
            updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
        }

        dropZoneElement.classList.remove("drop-zone--over");
    });

    const removeBtn = document.getElementById('remove-btn');
    removeBtn.addEventListener('click', (e) => {
        inputElement.value = ''
        let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
        thumbnailElement.style.backgroundImage = null;
        thumbnailElement.classList.remove("drop-zone__thumb");
    });
});

function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
        dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
        thumbnailElement = document.createElement("div");
        thumbnailElement.classList.add("drop-zone__thumb");
        dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = () => {
            thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
        };
    } else {
        thumbnailElement.style.backgroundImage = null;
    }
}

function uploadFile() {
    file = document.uploadID.file.value;
    if (file) {
        document.getElementById('uploadID').submit();
    }
}

function cropImage() {
    file = document.cropImageID.file.value;
    if (file) {
        document.getElementById('cropImageID').submit();
    }
}

function extract() {
    file = document.extractImageID.file.value;
    if (file) {
        document.getElementById('extractImageID').submit();
    }
}

function corner() {
    file = document.cornerImageID.file.value;
    if (file) {
        document.getElementById('cornerImageID').submit();
    }
}

const callToActionBtns = document.querySelectorAll(".menu-btn");

callToActionBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
        callToActionBtns.forEach(f => f.classList.remove('active'));
        e.target.classList.toggle("active");
    });
});