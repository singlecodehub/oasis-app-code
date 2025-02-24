const $ = (id) => {
    return document.getElementById(id);
}

const colorEl = $("color-select");
const strokeEidth = $('stroke-width');
const imageInput = document.getElementById("imageInput");
const shapeSelector = document.getElementById("shapeSelector");
const canvasWrapper = document.getElementById("canvas-wrapper");
const canvas = new fabric.Canvas(document.getElementById("canvas"), {
    isDrawingMode: true,
});
canvas.freeDrawingBrush = new fabric.PencilBrush(canvas)
let canvasJsonState = []; 
let canvasInitialState = []

let currentImageId = null;
let currentInput = null;
let currentAddMoreBtnId = null;
let currentReaderOnLoadEvent = null;

let newFileName = null;
function setFileName() {
    newFileName = `${currentInput.files[0].name}`
}

colorEl.onchange = (e) => {
    canvas.freeDrawingBrush.color = e.target.value;
}
strokeEidth.onchange = (e) => {
    canvas.freeDrawingBrush.width = e.target.value;
}

let overLay = false;
let isDrawing = false;
let shape = null;  // The current shape being drawn


// open overlay
const openOverlay = () => {
    overLay = true;
    canvasWrapper.style.display = "flex";
}
// close overlay
const closeOverlay = () => {
    overLay = false;
    canvasWrapper.style.display = "none";

    currentImageId = null;
    currentInput = null;
    currentAddMoreBtnId = null;
    currentReaderOnLoadEvent = null;

}



// Download Image
function downloadImage() {
    if (!newFileName) {
        alert("Save the image first");
        return
    }

    let a = document.createElement('a');
    a.href = URL.createObjectURL(currentInput.files[0]);
    a.download = newFileName;
    a.click()
}

// Change editor image to input
function changeInput(file) {
    const imgUrl = URL.createObjectURL(file);

    let fileName = newFileName
    let fileObject = new File([file], fileName,{type:"image/jpeg", lastModified:new Date().getTime()}, 'utf-8');
    let container = new DataTransfer(); 
    container.items.add(fileObject);
    currentInput.files = container.files;
    
    // change image view
    let currentImage = document.getElementById(currentImageId);
    currentImage.setAttribute('src', imgUrl);
    // const imgElement = document.getElementById(currentImageId);
    // imgElement.src = currentReaderOnLoadEvent.target.result;
    currentImage.style.display = 'block';
    console.log(currentAddMoreBtnId);
    document.getElementById(currentAddMoreBtnId).style.display = 'block';
}

// Save the edited image
function saveImage() {
    const dataURL = canvas.toDataURL("image/png");

    // set name of the new file
    setFileName();

    // Convert Data URL to Blob and simulate file upload
    fetch(dataURL)
        .then(res => res.blob())
        .then(blob => {
            const file = new File([blob], newFileName, { type: "image/png" });

            // Create a new DataTransfer object and assign it to the input
            const dataTransfer = new DataTransfer();
            changeInput(file);

            alert("Image with highlights saved!");
        });
    canvas.renderAll();
}



// Clear and undo canvas
const clearCanvas = () => {
    canvas.loadFromJSON(canvasInitialState[0]);
}

const undoCanvas = () => {
    if (canvasJsonState.length === 0) {
        return
    }
    const lastState = canvasJsonState.pop();
    canvas.loadFromJSON(lastState);
}

canvas.on("mouse:down", (event) => {
    if (canvasInitialState.length === 0)
        canvasInitialState.push(canvas.toJSON());
    canvasJsonState.push(canvas.toJSON());
}) 



function editImage() {
    canvas.isDrawingMode = !canvas.isDrawingMode;
    console.log(canvas.isDrawingMode);
}

