// /// for table /////
///////// mock data //////
const data = {
  table1: [
    {
      songNo: 1,
      songName: "Bohemian Rhapsody",
      songGenre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
    },
    {
      songNo: 2,
      songName: "Hotel California",
      songGenre: "Rock",
      artist: "Eagles",
      album: "Hotel California",
    },
    {
      songNo: 3,
      songName: "Stairway to Heaven",
      songGenre: "Ballad",
      artist: "Led Zeppelin",
      album: "Led Zeppelin IV",
    },
    {
      songNo: 4,
      songName: "Smells Like Teen Spirit",
      songGenre: "Rock",
      artist: "Nirvana",
      album: "Nevermind",
    },
    {
      songNo: 5,
      songName: "Imagine",
      songGenre: "Soul",
      artist: "John Lennon",
      album: "Imagine",
    },
    {
      songNo: 6,
      songName: "Hey Jude",
      songGenre: "Classic",
      artist: "The Beatles",
      album: "The Beatles (White Album)",
    },
    {
      songNo: 7,
      songName: "Thriller",
      songGenre: "Pop",
      artist: "Michael Jackson",
      album: "Thriller",
    },
    {
      songNo: 8,
      songName: "Like a Rolling Stone",
      songGenre: "Classic",
      artist: "Bob Dylan",
      album: "Highway 61 Revisited",
    },
    {
      songNo: 9,
      songName: "Purple Haze",
      songGenre: "Pop",
      artist: "Jimi Hendrix",
      album: "Are You Experienced",
    },
    {
      songNo: 10,
      songName: "Sweet Child o' Mine",
      songGenre: "Rock",
      artist: "Guns N' Roses",
      album: "Appetite for Destruction",
    },
    {
      songNo: 11,
      songName: "Billie Jean",
      songGenre: "Pop",
      artist: "Michael Jackson",
      album: "Thriller",
    },
    {
      songNo: 12,
      songName: "Let It Be",
      songGenre: "Classic",
      artist: "The Beatles",
      album: "Let It Be",
    },
  ],
  table2: [
    {
      queueNo: 1,
      songName: "Bohemian Rhapsody",
      songGenre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
      singername: "John",
    },
    {
      queueNo: 2,
      songName: "Bohemian Rhapsody",
      songGenre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
      singername: "Pedro",
    },
  ],
  table3: [
    {
      songNo: 1,
      songName: "Bohemian Rhapsody",
      songGenre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
    },
    {
      songNo: 2,
      songName: "Hotel California",
      songGenre: "Classic",
      artist: "Eagles",
      album: "Hotel California",
    },
  ],
};

// Pagination variables
const rowsPerPage = 5;
let currentPage1 = 1;
let currentPage2 = 1;

// DOM elements

function createtableRowHTML(row, tableschema) {
  //// we can put some conditional here to return different html for different data

  let tableschemadata = {
    table1: `
      <td data-label="Song No.">${row.songNo}</td>
    <td data-label="Song Name">${row.songName}</td>
    <td data-label="Genre">${row.songGenre}</td>
    <td data-label="Artist">${row.artist}</td>
    <td data-label="Album">${row.album}</td>
    <td data-label="Edit">
      <button id="${row.songNo}" class="btn btn-primary">EDIT</button>
    </td>
  `,
    table2: `
      <td data-label="Queue No.">${row.queueNo}</td>
    <td data-label="Song Name">${row.songName}</td>
    <td data-label="Genre">${row.songGenre}</td>
    <td data-label="Artist">${row.artist}</td>
    <td data-label="Album">${row.album}</td>
    <td data-label="Singer">${row.singername}</td>
    <td data-label="Edit">
      <button id="${row.queueNo}" class="btn btn-primary open-modal" data-modal="myModal2">EDIT</button>
    </td>
  `,
    table3: `
      <td data-label="Song No.">${row.songNo}</td>
    <td data-label="Song Name">${row.songName}</td>
    <td data-label="Genre">${row.songGenre}</td>
    <td data-label="Artist">${row.artist}</td>
    <td data-label="Album">${row.album}</td>
    <td data-label="Edit">
      <button id="${row.songNo}" class="btn btn-primary">EDIT</button>
    </td>
  `,
  };
  return tableschemadata[tableschema];
}

// Function to render table rows
function renderTable(
  page,
  tableschema,
  tablebdy,
  prevpgbtn,
  nextpgbtn,
  pageinfo
) {
  let tableBody = document.querySelector(tablebdy);
  let prevPageButton = document.querySelector(prevpgbtn);
  let nextPageButton = document.querySelector(nextpgbtn);
  let pageInfo = document.querySelector(pageinfo);

  tableBody.innerHTML = ""; // Clear existing rows
  const start = (page - 1) * rowsPerPage;
  const end = start + rowsPerPage;
  const paginatedData = data[tableschema].slice(start, end);

  paginatedData.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = createtableRowHTML(row, tableschema);
    tableBody.appendChild(tr);
  });

  // Update pagination info
  pageInfo.textContent = `Page ${page} of ${Math.ceil(
    data[tableschema].length / rowsPerPage
  )}`;

  // Enable/disable pagination buttons
  prevPageButton.disabled = page === 1;
  nextPageButton.disabled =
    page === Math.ceil(data[tableschema].length / rowsPerPage);
}

async function paginationbtnfunc(
  page,
  tableschema,
  tablebdy,
  prevpgbtn,
  nextpgbtn,
  pageinfo
) {
  // Event listeners for pagination buttons
  document.querySelector(prevpgbtn).addEventListener("click", () => {
    if (page > 1) {
      page--;
      renderTable(page, tableschema, tablebdy, prevpgbtn, nextpgbtn, pageinfo);
    }
  });

  document.querySelector(nextpgbtn).addEventListener("click", () => {
    if (page < Math.ceil(data[tableschema].length / rowsPerPage)) {
      page++;
      renderTable(page, tableschema, tablebdy, prevpgbtn, nextpgbtn, pageinfo);
    }
  });
}

// Initial render
renderTable(
  currentPage1,
  "table2",
  "#data-table1 tbody",
  "#paginationbtns1 .prev-page",
  "#paginationbtns1 .next-page",
  "#paginationbtns1 .page-info"
);
paginationbtnfunc(
  currentPage1,
  "table2",
  "#data-table1 tbody",
  "#paginationbtns1 .prev-page",
  "#paginationbtns1 .next-page",
  "#paginationbtns1 .page-info"
);

//////////////////////

document.querySelector(`#searchbtn`).addEventListener("click", () => {
  renderTable(
    currentPage2,
    "table3",
    "#data-table3 tbody",
    "#paginationbtns3 .prev-page",
    "#paginationbtns3 .next-page",
    "#paginationbtns3 .page-info"
  );
  paginationbtnfunc(
    currentPage2,
    "table3",
    "#data-table3 tbody",
    "#paginationbtns3 .prev-page",
    "#paginationbtns3 .next-page",
    "#paginationbtns3 .page-info"
  );
});

document.querySelector(`#tabnavid2`).addEventListener("click", () => {
  renderTable(
    currentPage2,
    "table1",
    "#data-table2 tbody",
    "#paginationbtns2 .prev-page",
    "#paginationbtns2 .next-page",
    "#paginationbtns2 .page-info"
  );
  paginationbtnfunc(
    currentPage2,
    "table1",
    "#data-table2 tbody",
    "#paginationbtns2 .prev-page",
    "#paginationbtns2 .next-page",
    "#paginationbtns2 .page-info"
  );
});

async function contentswitchfunc(name, ...getarray) {
  const elements = document.querySelectorAll("[HTMLINCLUDE]");

  elements.forEach((element) => {
    const attributeValue = element.getAttribute("HTMLINCLUDE");
    if (getarray.includes(attributeValue)) {
      if (name === attributeValue) {
        element.classList.remove("displaynone");
      } else {
        element.classList.add("displaynone");
      }
    }
  });
}
//////////////////
//// for tab function

let contentarray = [
  "dashboardtabdesignid",
  "songlibmanagertabdesignid",
  "settingstabdesignid",
];

/////////////// for tab navigations ///////////////

document.querySelectorAll(".tabnavid1").forEach((button) => {
  button.addEventListener("click", () => {
    contentswitchfunc("dashboardtabdesignid", ...contentarray);
    document.querySelector(`#tabnavid1`).click();
  });
});

document.querySelectorAll(".tabnavid2").forEach((button) => {
  button.addEventListener("click", () => {
    contentswitchfunc("songlibmanagertabdesignid", ...contentarray);
    document.querySelector(`#tabnavid2`).click();
  });
});

document.querySelectorAll(".tabnavid3").forEach((button) => {
  button.addEventListener("click", () => {
    contentswitchfunc("settingstabdesignid", ...contentarray);
    document.querySelector(`#tabnavid3`).click();
  });
});

////////////////////////////////////////////////

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

function forpopupfunction(target, event) {
  ////////////// for popup confirmation ////////////
  if (target.tagName === "BUTTON") {
    if (target.getAttribute("popupconfirm") != null) {
      Swal.fire({
        title: "Do you want to save the changes?",
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: "Save",
        denyButtonText: `Don't save`,
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
          console.log(
            "go to confirm function for ",
            target.getAttribute("popupconfirm")
          );
          Swal.fire("Saved!", "", "success");
        } else if (result.isDenied) {
          Swal.fire("Changes are not saved", "", "info");
        }
      });
    }
  }
  //////////////////////////////////////////////////
}

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

document.addEventListener("click", (event) => {
  const target = event.target;

  formodalfunction(target, event);
  forfilegetterfunction(target, event);
  forpopupfunction(target, event);
  fordropdownfunction(target, event);

  //// for another function like GET POST
  ////  or for CRUD
});

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
