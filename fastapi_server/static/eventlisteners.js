document.addEventListener("click", (event) => {
  const target = event.target;

  formodalfunction(target, event);
  forfilegetterfunction(target, event);
  forpopupfunction(target, event);
  fordropdownfunction(target, event);
  forradiobuttonfunction(target, event);
  fortogglefunction(target, event);

  ///////// CRUD ////////////
  //// for songlibrary table edit ////
  forsonglibrarytableedit(target, event);
  //// for dashboard table edit //////
  forsongaddqueuetableedit(target, event);
  forsongeditqueuetableedit(target, event);
});
