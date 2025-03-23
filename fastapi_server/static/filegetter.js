/////////////// for file getter function ///////////////
function forfilegetterfunction(target, event) {
  if (target.tagName === "BUTTON") {
    if (target.getAttribute("filegetterbtn") != null) {
      let fileinput = document.getElementById(
        target.getAttribute("filegetterbtn")
      );
      fileinput.click();
      if (!fileinput.onchange) {
        fileinput.onchange = function () {
          displayFileName(fileinput.id, fileinput.getAttribute("displayvalue"));
        };
      }
    }
  }
}
////////////////////////////////////////////////////////

///////////// file getter function ////////////
function getfilefuncid(id) {
  document.getElementById(id).click();
}

function displayFileName(inputId, displayId) {
  const fileInput = document.getElementById(inputId);
  const fileNameDisplay = document.getElementById(displayId);

  if (fileInput.files.length > 0) {
    //const file = fileInput.files[0];
    fileNameDisplay.textContent = `Selected files: ${fileInput.files.length}`;
  } else {
    fileNameDisplay.textContent = "No file selected.";
  }
}
////////////////////////////////////////////////
