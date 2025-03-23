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
