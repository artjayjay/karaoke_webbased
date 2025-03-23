let radiobtnvalue1 = "";
/////////////// for radio button function ///////////////
function forradiobuttonfunction(target, event) {
  // Check if the clicked element is a radio button
  if (
    target.tagName === "INPUT" &&
    target.type === "radio" &&
    target.name == "radioname1"
  ) {
    // Get the value of the selected radio button
    const selectedValue = target.value;
    console.log("Selected Radio Button Value:", selectedValue);
    radiobtnvalue1 = selectedValue;

    // Call a function to handle the radio button selection
  }
}
////////////////////////////////////////////////////////
