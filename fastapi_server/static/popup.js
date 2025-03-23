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
          // go to confirm function
          getallbtntransactionfunc(target.getAttribute("popupconfirm"));
        } else if (result.isDenied) {
          Swal.fire("Changes are not saved", "", "info");
        }
      });
    }
  }
  //////////////////////////////////////////////////
}
