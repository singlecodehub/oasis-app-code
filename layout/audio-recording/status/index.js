console.log("Testing recording")

class Record {

    recording = false;
    #recordingActive = false;
    audioPlayBack = document.querySelector(".audio-playback");
    audioChunk = [];
    mediaRecorder = null;

    // buttons
    currentTextArea = null
    closeButton = document.querySelector("#stop-recording")

    // overlay
    overlay = document.querySelector("#record-overlay-container");

    openOverLay = () => {
        this.overlay.style.display = "block";
    }
    closeOverLay = () => {
        this.overlay.style.display = "none";
    }

    speechToText = function (data) {
        this.currentTextArea.innerText = data;
        // console.log(this.currentTextArea.innerText);
    }

    recorder = function () {
        document.querySelectorAll(".record").forEach(async e => {
            e.addEventListener("click", async (e) => {
                this.currentTextArea = e.target.parentNode.parentNode.children[1];
                this.initializerRecorder();
                this.recording = !this.recording;
                this.recordingActive = !this.recordingActive;

            })
        })
    }
    closeRecorder = () => {
        this.closeButton.addEventListener("click", async () => {
            this.stopRecroder();
            this.recording = !this.recording;
            this.recordingActive = !this.recordingActive;
            this.speechToText("This is test data");
            this.currentTextArea = null;
            this.closeOverLay();
        })
    }

    initializerRecorder = async () => {
        try {
            this.openOverLay();
            // request microphone access
            const stream = await navigator.mediaDevices.getUserMedia({audio: true});
            // initialize media recorder
            this.mediaRecorder = new MediaRecorder(stream);
            // collect data in chunks
            this.mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) {
                    this.audioChunk.push(e.data);
                }
            }
            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunk, {type: "audio/webm"});
                const audioUrl = URL.createObjectURL(audioBlob);
                this.audioPlayBack.src = audioUrl;
                this.audioChunk = [];
            }
            this.mediaRecorder.start();
        } catch(e) {
            alert("Unable to get microphone access");
        }
    }

    stopRecroder = () => {
        if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
            this.mediaRecorder.stop();
        }
    }
}


const record = new Record();
record.recorder();
record.closeRecorder();