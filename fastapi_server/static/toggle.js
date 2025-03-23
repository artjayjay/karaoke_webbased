function fortogglefunction(target, event) {
  // Check if the clicked element is a radio button
  if (target.tagName === "INPUT" && target.type === "checkbox") {
    // Get the value of the selected radio button
    const isChecked = target.checked;
    console.log("Checkbox is checked:", isChecked);

    // Call a function to handle the radio button selection
  }
}
////////// disable 2 toggle ////////////
document.addEventListener("DOMContentLoaded", function () {
  const mainToggle = document.getElementById("showpopupscoretoggleid");
  const toggle2 = document.getElementById("showscoretoggleid");
  const toggle3 = document.getElementById("shownametoggleid");
  const toggle2Fill = toggle2.nextElementSibling; // .toggle__fill
  const toggle3Fill = toggle3.nextElementSibling; // .toggle__fill

  // Function to disable/enable other toggles based on the main toggle state
  function updateToggleStates() {
    if (!mainToggle.checked) {
      toggle2.disabled = true;
      toggle2.checked = false;
      toggle3.disabled = true;
      toggle3.checked = false;

      // Add the disabled class to .toggle__fill
      toggle2Fill.classList.add("disabled");
      toggle3Fill.classList.add("disabled");
    } else {
      toggle2.disabled = false;
      toggle3.disabled = false;

      // Remove the disabled class from .toggle__fill
      toggle2Fill.classList.remove("disabled");
      toggle3Fill.classList.remove("disabled");
    }
  }

  // Run the function on page load
  updateToggleStates();

  // Add event listener to the main toggle
  mainToggle.addEventListener("change", updateToggleStates);
});
////////////////////////////////////////
