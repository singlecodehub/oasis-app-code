const uploadImageButton = document.querySelector("#image-upload-button");
const uploadImageInput = document.querySelector("#upload-image-input");
const imageViewer = document.querySelector(".image-viewer > img");
const uploadImageText = document.querySelector(".upload-image-text");
const uploadImageTextarea = document.querySelector(".upload-image-text > textarea");

const copyUploadText = document.querySelector("#copy-upload-text");
const imageTextSpinner = document.querySelector(".image-text-spinner");


const spinnerActive = async () => {
    imageTextSpinner.style.display = "block"
}
const spinnerInActive = async () => {
    imageTextSpinner.style.display = "none"
}

const textActive = async () => {
    uploadImageText.style.display = "block";
}
const textInActive = async () => {
    uploadImageText.style.display = "none";
}


let currentFile = null;


// onclick copy extract text to clipboard
// copyUploadText.onclick = async () => {
//     navigator.permissions.query({ name: "clipboard-write" }).then((result) => {
//         if (result.state === "granted" || result.state === "prompt") {
//             /* write to the clipboard now */
//             navigator.clipboard.writeText(uploadImageTextarea.innerHTML).then(() => {
//                 // console.log(uploadImageTextarea.innerHTML);
//                 console.log("Copied");
//             }, () => {
//                 console.log("Failed to copy");
//             })
//         }
//     });
//     await spinnerInActive();   
// }


const tessaractMain = async (file) => {
    await spinnerActive();
    
    const worker = await Tesseract.createWorker('eng');
    const ret = await worker.recognize(file);
    data = ret.data.text;
    console.log(data);
    uploadImageTextarea.innerHTML = data;
    await textActive()
    
    await spinnerInActive();

    await worker.terminate();
}

uploadImageInput.addEventListener("change", async (ie) => {
    // currentFile = uploadImageInput.files[0];
    console.log(ie);
    const fr = new FileReader();
    fr.onload = async (fe) => {
        imageViewer.src = fe.target.result;
        await tessaractMain(fe.target.result);
    }
    fr.readAsDataURL(ie.target.files[0]);
})

const uploadImage = () => {
    uploadImageButton.addEventListener("click", async () => {
        uploadImageInput.click();
    })
}

uploadImage();