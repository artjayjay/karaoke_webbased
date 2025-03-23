// // Call a Python function from JavaScript
// async function callPython() {
//   const name = "User";
//   try {
//     // Call the exposed Python function `greet`
//     const response = await fetch(`/api/greet/${name}`);
//     const data = await response.text();
//     document.getElementById("response").innerText = data;
//   } catch (error) {
//     console.error("Error calling Python function:", error);
//   }
// }

// async function openinbrowser() {
//   try {
//     const currentUrl = window.location.origin;
//     const newPath = "/open_mp4_in_browser";
//     const newUrl = currentUrl + newPath;
//     const win = window.open(newUrl, "_blank");
//     win.focus();
//   } catch (error) {
//     console.error("Error opening browser:", error);
//   }
// }
// // Expose a JavaScript function to Python
// window.sayHello = function (name) {
//   return `Hello, ${name} from JavaScript!`;
// };
