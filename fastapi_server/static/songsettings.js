let karaokeserver;

async function fetchSongSettings() {
  try {
    const response = await axios.get("/api/songsettings/displaysettings");
    const settings = response.data;

    // Update the form fields with the fetched settings
    if (settings.difficulty) {
      // Assuming radiobtnvalue1 is a variable tied to the selected radio button
      radiobtnvalue1 = settings.difficulty;
      document.querySelector(
        `input[name="radioname1"][value="${settings.difficulty}"]`
      ).checked = true;
    }

    if (settings.mainserver && settings.karaokeserver) {
      document.getElementById("mainservernameid").value = settings.mainserver;
      document.getElementById("karaokeservernameid").value =
        settings.karaokeserver;

      karaokeserver = settings.karaokeserver;
    }

    // Update checkboxes
    let toggle1 = document.getElementById("showpopupscoretoggleid");
    let toggle2 = document.getElementById("showscoretoggleid");
    let toggle3 = document.getElementById("shownametoggleid");

    if (settings.showpopupscore == true) {
      toggle1.checked = settings.showpopupscore;
      toggle2.disabled = false;
      toggle3.disabled = false;
      toggle2.checked = settings.showscore;
      toggle3.checked = settings.showsingersname;
    }
  } catch (error) {
    console.error("Error fetching song settings:", error);
    const errorMessage =
      error.response?.data?.detail ||
      "Failed to fetch song settings. Please try again.";
    alert(errorMessage);
  }
}

async function updatesongsettings() {
  const difficulty = radiobtnvalue1;
  const showpopupscore = document.getElementById(
    "showpopupscoretoggleid"
  ).checked;
  const showscore = document.getElementById("showscoretoggleid").checked;
  const showsingersname = document.getElementById("shownametoggleid").checked;
  const scorevidid = document.getElementById("filegetter2");
  const scoreapplauseid = document.getElementById("filegetter3");
  const mainserverid = document.getElementById("mainservernameid").value;
  const karaokeserverid = document.getElementById("karaokeservernameid").value;

  const formData = new FormData();
  formData.append("difficulty", difficulty);
  formData.append("showpopupscore", showpopupscore.toString());
  formData.append("showscore", showscore.toString());
  formData.append("showsingersname", showsingersname.toString());
  formData.append("mainserver", mainserverid);
  formData.append("karaokeserver", karaokeserverid);

  // Append files only if they are selected
  if (scorevidid.files.length > 0) {
    formData.append("scorevidid", scorevidid.files[0]);
  }
  if (scoreapplauseid.files.length > 0) {
    formData.append("scoreapplauseid", scoreapplauseid.files[0]);
  }

  try {
    const response = await axios.put(
      "/api/songsettings/updatesettings",
      formData
    );

    console.log(response.data.message);
    if (response.data.message === "SongSettings updated successfully") {
      Swal.fire({
        title: "Done!",
        text: "Song Settings Updated Successfully!",
        icon: "success",
      });
    }
  } catch (error) {
    console.error("Error updating info:", error);
    const errorMessage =
      error.response?.data?.detail ||
      "Failed to update song settings. Please try again.";
    alert(errorMessage);
  }
}
