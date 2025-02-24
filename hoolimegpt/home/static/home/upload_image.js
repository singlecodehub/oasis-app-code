const uploadImageButton = document.querySelector("#image-upload-button");
const uploadImageInput = document.querySelector("#upload-image-input");
const imageViewer = document.querySelector(".image-viewer > img");
let currentFile = null;

uploadImageInput.addEventListener("change", async (ie) => {
    // currentFile = uploadImageInput.files[0];
    console.log(ie);
    const fr = new FileReader();
    fr.onload = async (fe) => {
        imageViewer.src = fe.target.result;
    }
    console.l
    fr.readAsDataURL(ie.target.files[0]);
})

const uploadImage = () => {
    uploadImageButton.addEventListener("click", async () => {
        uploadImageInput.click();
    })
}

uploadImage();