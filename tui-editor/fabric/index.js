const imageInput = document.getElementById("imageInput");
const shapeSelector = document.getElementById("shapeSelector");
const canvasWrapper = document.getElementById("canvas-wrapper");
const canvas = new fabric.Canvas("canvas");

let newFileName = null;

function setFileName() {
    newFileName = `${imageInput.files[0].name}`
}

document.getElementById("uploadImage").addEventListener("click", () => {
    imageInput.click();

})


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
}

// Handle file input change
imageInput.addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        fabric.Image.fromURL(e.target.result, function(img) {
            canvas.clear();
            img.set({ 
                selectable: false,
                top: 0,
            }); // Make the image non-selectable
            canvas.setWidth(img.width);
            canvas.setHeight(img.height);

            canvas.add(img);
            canvas.renderAll();
        });
    };
    reader.readAsDataURL(file);

    // over overlay canvas
    openOverlay();
});


// Start drawing when mouse is pressed
canvas.on("mouse:down", function(event) {
    
    isDrawing = true;
    const pointer = canvas.getPointer(event.e);
    const shapeType = shapeSelector.value;

    if (shapeType === "") {
        return
    }

    // Create shape based on user selection
    if (shapeType === "rectangle") {
        shape = new fabric.Rect({
            left: pointer.x,
            top: pointer.y,
            width: 0,
            height: 0,
            stroke: "blue",
            strokeWidth: 2,
            fill: "rgba(0, 0, 0, 0)", // Transparent fill
            selectable: true
        });
    } else if (shapeType === "circle") {
        shape = new fabric.Ellipse({
            left: pointer.x,
            top: pointer.y,
            rx: 0,  // Radius X
            ry: 0,  // Radius Y
            stroke: "red",
            strokeWidth: 2,
            fill: "rgba(0, 0, 0, 0)", // Transparent fill
            selectable: true
        });
    } else if (shapeType === "text") {
        shape = new fabric.IText("Tap and Type", {
            fontFamily: 'arial black',
            left: pointer.x,
            top: pointer.y,
            fill: "red", // Transparent fill
            selectable: true
        });
    }

    canvas.add(shape);
});


// Update shape size as the user drags the mouse
canvas.on("mouse:move", function(event) {
    if (!isDrawing || !shape) return;

    const pointer = canvas.getPointer(event.e);
    const originX = shape.left;
    const originY = shape.top;

    if (shape.type === "rect") {
        shape.set({
            width: Math.abs(pointer.x - originX),
            height: Math.abs(pointer.y - originY)
        });
    } else if (shape.type === "ellipse") {
        shape.set({
            rx: Math.abs(pointer.x - originX) / 2,
            ry: Math.abs(pointer.y - originY) / 2,
            left: Math.min(pointer.x, originX),
            top: Math.min(pointer.y, originY)
        });
    } else if (shape.type === "text") {
        shape.set({
            rx: Math.abs(pointer.x - originX) / 2,
            ry: Math.abs(pointer.y - originY) / 2,
            left: Math.min(pointer.x, originX),
            top: Math.min(pointer.y, originY)
        });
    }

    canvas.renderAll();
});

// Finish drawing when the mouse is released
canvas.on("mouse:up", function() {
    isDrawing = false;
    shape = null;  // Reset the current shape

    // reset shape selection to null
    shapeSelector.value = ""
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
