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

displayqueuetable();

//////////////////////

document.querySelector(`#tabnavid1`).addEventListener("click", () => {
  setTimeout(displayqueuetable, 500);
});

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
  displaysongtablesearch();
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

  /////// for transaction ////////
  displaysongtable();
});

document.querySelector("#tabnavid3").addEventListener("click", () => {
  fetchSongSettings();
});

async function getallbtntransactionfunc(popupid) {
  if (popupid == "addnewsong") {
    addnewsongs();
  }
  if (popupid == "updatesong") {
    updatesong();
  }
  if (popupid == "deletesong") {
    deletesong();
  }
  if (popupid == "addsongtoqueue") {
    addnewsongqueue();
  }
  if (popupid == "savesongqueue") {
    updatesongqueue();
  }
  if (popupid == "deletesongqueue") {
    deletesongqueue();
  }
  if (popupid == "updatesongsettings") {
    updatesongsettings();
  }
}
