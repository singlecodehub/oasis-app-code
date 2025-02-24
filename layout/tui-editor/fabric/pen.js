
const MAX_WIDTH = 800;
const MAX_HEIGHT = 600;

const $ = (id) => {
    return document.getElementById(id);
}

const colorEl = $("color-select");
const imageInput = document.getElementById("imageInput");
const shapeSelector = document.getElementById("shapeSelector");
const canvasWrapper = document.getElementById("canvas-wrapper");
const canvas = new fabric.Canvas("drawingCanvas", {
    isDrawingMode: true,
});
canvas.selection = false;
canvas.freeDrawingBrush = new fabric.PencilBrush(canvas)
canvas.freeDrawingBrush.width = "10";

let canvasJsonState = []; 
let canvasInitialState = []

let newFileName = null;
function setFileName() {
    newFileName = `${imageInput.files[0].name}`
}

document.getElementById("uploadImage").addEventListener("click", () => {
    imageInput.click();

})

colorEl.onchange = (e) => {
    canvas.freeDrawingBrush.color = e.target.value;
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
    imageInput.value = "";
    canvasWrapper.style.display = "none";
}

// Handle file input change
imageInput.addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        fabric.Image.fromURL(e.target.result, function(img) {
            canvas.clear();
            const scale = Math.min(MAX_WIDTH / img.width, MAX_HEIGHT / img.height);
                    
            img.set({
                scaleX: scale,
                scaleY: scale,
                selectable: false,
                evented: false,
            }); // Make the image non-selectable
            // canvas.setWidth(img.width);
            // canvas.setHeight(img.height);

            canvas.add(img);
            canvas.sendToBack(img);
        });
    };
    reader.readAsDataURL(file);

    // over overlay canvas
    openOverlay();
});



// remove active Fabric js object
function removeObject() {
    canvas.remove(canvas.getActiveObject());
}


// Download Image
function downloadImage() {
    if (!newFileName) {
        alert("Save the image first");
        return
    }

    let a = document.createElement('a');
    a.href = URL.createObjectURL(imageInput.files[0]);
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
    imageInput.files = container.files;
}

// Save the edited image
function saveImage() {
    canvas.renderAll();

    const dataURL = canvas.toDataURL("image/png");

    // set name of the new file
    setFileName(imageInput);

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
}


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

// canvas.setZoom();


function editImage() {
    canvas.isDrawingMode = !canvas.isDrawingMode;
    if (canvas.isDrawingMode) {
        canvas.forEachObject(function (obj) {
            console.log("unlock canvas")
            obj.selectable = true; // Prevent objects from being selected
            obj.evented = false; // Disable interactions (drag, rotate, scale)
        });
    } else {
        canvas.forEachObject(function (obj) {
            console.log("lock canvas")
            obj.selectable = true; // Prevent objects from being selected
            obj.evented = false; // Disable interactions (drag, rotate, scale)
        });
    }
}