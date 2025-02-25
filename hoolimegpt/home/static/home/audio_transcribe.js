console.log("Testing recording")


class Record {

    recording = false;
    #recordingActive = false;
    // audioPlayBack = document.querySelector(".audio-playback");
    audioChunk = [];
    mediaRecorder = null;

    // buttons
    currentTextArea = null
    closeButton = document.querySelector("#stop-recording")

    // hold the response message;
    message = null


    // overlay
    overlay = document.querySelector("#record-overlay-container");
    openOverLay = () => {
        this.overlay.style.display = "block";
    }
    closeOverLay = () => {
        this.overlay.style.display = "none";
    }

    speechToText = function (data) {
        console.log(this.message);
        if (this.message) {
            this.currentTextArea.innerHTML = this.message;
        } else {
            alert("Error while transcribing");
        }
        // this.currentTextArea.innerText = data;
    }

    recorder = function () {
        // this.audioPlayBack.src = "";
        document.querySelectorAll(".record-box").forEach(async (e) => {
            this.currentTextArea = null;
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
                const audioBlob = new Blob(this.audioChunk, {type: "audio/wav"});
                const audioUrl = URL.createObjectURL(audioBlob);
                // this.audioPlayBack.src = audioUrl;
                var wavfromblob = new File([audioBlob], "incomingaudioclip.wav", {type: "audio/wav"});
                this.trascribe(wavfromblob);
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


    trascribe = (audioBlob) => {
        // for

        document.getElementById("loader").style.display = "block";


        const formData = new FormData();
        formData.append("audio_file", audioBlob);
        console.log(formData)

        fetch("http://localhost:8000/transcribe/", {
            method: "POST",
            cache: "no-cache",
            body: formData
        }).then(async res => {
            const responseData = await res.json()
            console.log(responseData);
            this.message = responseData.message;
        }).then(async () => {
            document.getElementById("loader").style.display = "none";
            this.speechToText();
        })
    }
}


const record = new Record();
record.recorder();
record.closeRecorder();