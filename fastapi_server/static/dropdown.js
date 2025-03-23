// Function to handle dropdown functionality
function fordropdownfunction(target, event) {
  // Close all dropdowns
  function closeAllDropdowns() {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
      menu.style.display = "none";
    });
    document.querySelectorAll(".dropdown-toggle").forEach((toggle) => {
      toggle.style.backgroundColor = "transparent";
    });
  }

  // If the clicked element is a dropdown toggle
  if (target.closest(".dropdown-toggle")) {
    const dropdown = target.closest(".dropdown");
    const toggle = dropdown.querySelector(".dropdown-toggle");
    const menu = dropdown.querySelector(".dropdown-menu");

    // Toggle the dropdown menu
    if (menu.style.display === "block") {
      closeAllDropdowns();
    } else {
      closeAllDropdowns();
      menu.style.display = "block";
      toggle.style.backgroundColor = "#eee";
    }
  }
  // If the clicked element is a dropdown menu option
  else if (target.closest(".dropdown-menu div")) {
    const dropdown = target.closest(".dropdown");
    const menu = dropdown.querySelector(".dropdown-menu");
    const toggle = dropdown.querySelector(".dropdown-toggle");

    // Update the selected option for select-dropdown
    if (dropdown.classList.contains("select-dropdown")) {
      const label = toggle.querySelector("p");
      label.textContent = target.textContent;
    }

    // Log the selected option
    console.log(dropdown.id, target.textContent);

    // Close the dropdown
    closeAllDropdowns();
  }
  // If clicked outside any dropdown
  else {
    closeAllDropdowns();
  }
}
