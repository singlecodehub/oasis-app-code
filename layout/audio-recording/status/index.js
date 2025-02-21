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
    }

    recorder = function () {
        this.audioPlayBack.src = "";
        document.querySelectorAll(".record-box").forEach(async (e) => {
            const button = e.firstElementChild;
            button.addEventListener("click", async () => {
                this.currentTextArea = e.lastElementChild;
                this.initializerRecorder();
                this.recording = !this.recording;
                this.recordingActive = !this.recordingActive;

            })
        })
        document.querySelectorAll(".record").forEach(async e => {
            
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
                const audioBlob = new Blob(this.audioChunk, {type: "audio/mp3"});
                const audioUrl = URL.createObjectURL(audioBlob);
                this.audioPlayBack.src = audioUrl;
                this.audioChunk = [];
            }
            this.mediaRecorder.start();


            this.openOverLay();
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