
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;

const $ = (id) => {
    return document.getElementById(id);
}

const colorEl = $("color-select");
const imageInput = document.getElementById("imageInput");
const canvasWrapper = document.getElementById("canvas-wrapper");
const canvasContainer = document.getElementById("canvas-container");

const canvas = document.getElementById("drawingCanvas");
const ctx = canvas.getContext("2d");
let isDrawing = false;
let canDraw = true;
let lastX = 0, lastY = 0;

// image size
let imgWidth = null;
let imgHeight = null;

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
    ctx.strokeStyle = e.target.value;
}

let overLay = false;
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
imageInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const img = new Image();
        img.onload = function () {
            // Clear canvas
            ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            // Get aspect ratio fit
            const imgRatio = img.width / img.height;
            const canvasRatio = CANVAS_WIDTH / CANVAS_HEIGHT;

            let drawWidth, drawHeight;
            if (imgRatio > canvasRatio) {
                // Image is wider than canvas
                drawWidth = CANVAS_WIDTH;
                drawHeight = CANVAS_WIDTH / imgRatio;
            } else {
                // Image is taller than canvas
                drawHeight = CANVAS_HEIGHT;
                drawWidth = CANVAS_HEIGHT * imgRatio;
            }

            // Center the image in the canvas
            const offsetX = (CANVAS_WIDTH - drawWidth) / 2;
            const offsetY = (CANVAS_HEIGHT - drawHeight) / 2;

            imgWidth = drawWidth;
            imgHeight = drawHeight;

            ctx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
        };
        img.src = e.target.result;
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
    let fileObject = new File([file], fileName, { type: "image/jpeg", lastModified: new Date().getTime() }, 'utf-8');
    let container = new DataTransfer();
    container.items.add(fileObject);
    imageInput.files = container.files;
}

// Save the edited image
function saveImage() {
    console.log(imgWidth, imgHeight)

    // Calculate scaling and positioning (already applied in your draw logic)
    const scale = Math.min(CANVAS_WIDTH / imgWidth, CANVAS_HEIGHT / imgHeight);
    const scaledWidth = imgWidth * scale;
    const scaledHeight = imgHeight * scale;
    const offsetX = (CANVAS_WIDTH - scaledWidth) / 2;
    const offsetY = (CANVAS_HEIGHT - scaledHeight) / 2;

    // Create a new temporary canvas for cropping
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = scaledWidth;
    tempCanvas.height = scaledHeight;

    let tempCtx = tempCanvas.getContext("2d");

    // Copy only the image part
    tempCtx.drawImage(canvas, offsetX, offsetY, scaledWidth, scaledHeight, 0, 0, scaledWidth, scaledHeight);

    // Convert to data URL (or you can save it as a file)
    const dataURL = tempCanvas.toDataURL("image/png");

    // const dataURL = canvas.toDataURL("image/png");

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

// Start drawing
function startDrawing(e) {
    if (!canDraw) return; // Allow scrolling when drawing is disabled
    if (e.touches && e.touches.length > 1) return; // Ignore multi-touch for scrolling
    isDrawing = true;
    const rect = canvas.getBoundingClientRect();
    [lastX, lastY] = [
        (e.offsetX || e.touches[0].clientX - rect.left),
        (e.offsetY || e.touches[0].clientY - rect.top)
    ];
    e.preventDefault(); // Prevent unwanted page scroll when drawing
}

// Draw function
function draw(e) {
    if (!isDrawing || !canDraw) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.offsetX || e.touches[0].clientX - rect.left;
    const y = e.offsetY || e.touches[0].clientY - rect.top;

    ctx.strokeStyle = colorEl.value;
    ctx.lineWidth = 10;
    ctx.lineCap = "round";

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();
    [lastX, lastY] = [x, y];

    e.preventDefault(); // Prevent unwanted page scrolling when drawing
}

function stopDrawing() {
    isDrawing = false;
}

function editImage() {
    canDraw = !canDraw
    canvasContainer.style.touchAction = canDraw ? "none" : "auto";

    if (canDraw) {
        alert("Edit enabled");
    } else {
        alert("Edit disabled");
    }
}


// Attach events for mouse & touch
canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseleave", stopDrawing);
canvas.addEventListener("touchstart", startDrawing, { passive: false });
canvas.addEventListener("touchmove", draw, { passive: false });
canvas.addEventListener("touchend", stopDrawing);

