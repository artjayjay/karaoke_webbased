////////////////// For Modal Functions /////////////////////////
////////////////// Part of Legacy Modal Function ///////////////
function toggleModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = modal.style.display === "block" ? "none" : "block";
  }
}
//////////////////////////////////////////////////////

function formodalfunction(target, event) {
  // ///////////////// For Opening Both Legacy or Modern Modal //////////////////////
  if (target.tagName === "BUTTON") {
    if (
      target.getAttribute("data-modal") != null &&
      target.classList.contains("open-modal")
    ) {
      let modal = document.getElementById(target.getAttribute("data-modal"));
      if (modal.tagName == "DIALOG") {
        modal.showModal();
      }
      if (modal.tagName == "DIV") {
        toggleModal(target.getAttribute("data-modal"));
      }
    }
  }
  ///////////////////////////////////////////////////////////////////////////////
  //////////////////// For Closing Legacy Modal ////////////////////////////////
  if (target.tagName === "SPAN") {
    if (target.className == "close") {
      if (
        target.parentElement.id != null &&
        target.parentElement.tagName == "DIALOG"
      ) {
        let modal = document.getElementById(target.parentElement.id);
        modal.close();
      } else {
        toggleModal(target.parentElement.parentElement.id);
      }
    }
  }
  ///////////////////////////////////////////////////////////////////////
  ///////////// For Closing Modal Legacy By clicking Backdrop //////////////////
  if (target.tagName === "DIV" && target.classList.contains("modal1")) {
    toggleModal(target.id);
  }
  //////////////////////////////////////////////////////
  /////////////////// For Closing Dialog ///////////////////////

  if (target.tagName === "DIALOG") {
    const modal = document.getElementById(target.id);
    const dialogDimensions = modal.getBoundingClientRect();
    if (
      event.clientX < dialogDimensions.left ||
      event.clientX > dialogDimensions.right ||
      event.clientY < dialogDimensions.top ||
      event.clientY > dialogDimensions.bottom
    ) {
      modal.close();
    }
  }
  //////////////////////////////////////////////////////
}
