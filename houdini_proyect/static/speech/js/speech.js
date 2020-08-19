let oldData = "";
let data = "";
let contenido = "";
if ("webkitSpeechRecognition" in window) {
  var reconizing;
  var speechRecognizer = new webkitSpeechRecognition();
  speechRecognizer.continuous = true;
  speechRecognizer.interimResults = true;
  speechRecognizer.lang = "en-US";
  reset();
  speechRecognizer.onend = reset;
  //contenido = document.getElementById('result').value;
  //console.log(contenido);
  speechRecognizer.onresult = function (event) {
    var interimTranscripts = "";
    var finalTranscripts = "";
    for (var i = event.resultIndex; i < event.results.length; i++) {
      var transcript = event.results[i][0].transcript;
      transcript.replace("\n", "<br>");
      if (event.results[i].isFinal) {
        finalTranscripts += transcript;
      } else {
        interimTranscripts += transcript;
      }
      data += finalTranscripts;
      result.innerHTML = data + interimTranscripts;
    }
  };
  speechRecognizer.onsoundend = function () {};
  speechRecognizer.onerror = function (event) {};
} else {
  result.innerHTML = "Your browser does not support that.";
}
function reset() {
  recognizing = false;
}
function toggleStartStop() {
  if (recognizing) {
    speechRecognizer.stop();
    recognizing = false;
    button.style.backgroundColor = "#4e73df";
    document.getElementById("icono").className = "fas fa-microphone";
  } else {
    button.style.backgroundColor = "#e02b2b";
    document.getElementById("icono").className = "fas fa-stop-circle";
    if (data.length > 0) {
      data += ".\n";
    }
    speechRecognizer.start();
    recognizing = true;
  }
}
