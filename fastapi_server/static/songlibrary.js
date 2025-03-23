async function displaysongtable(limit = 10, offset = 1) {
  try {
    const response = await axios.get(
      `/api/songlibrary/displaysongs/${limit}/${offset}`
    );
    const fetchedData = response.data;

    // Update the data object with the fetched data
    data.table1 = fetchedData.songs;

    // Re-render the table with the new data
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
  } catch (error) {
    console.error("Error fetching songs:", error);
    alert("Failed to fetch songs. Please try again.");
  }
}

async function addnewsongs() {
  const fileInput = document.getElementById("filegetter1");
  const songname = document.getElementById("songnameinputid").value;
  const genre = document
    .getElementById("dropdown3")
    .querySelector("p").textContent;
  const artist = document.getElementById("artistinputid").value;
  const album = document.getElementById("albuminputid").value;

  // Validate file input
  if (!fileInput.files || fileInput.files.length !== 2) {
    alert("The folder is empty or only 1 file it must be 2 files.");
    return;
  }

  const formData = new FormData();
  formData.append("file1", fileInput.files[0]);
  formData.append("file2", fileInput.files[1]); // Ensure this file exists if required
  formData.append("songname", songname);
  formData.append("genre", genre);
  formData.append("artist", artist);
  formData.append("album", album);

  try {
    const response = await axios.post(
      "/api/songlibrary/insertsongs",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    console.log(response.data.message);
    if (response.data.message === "Song added successfully") {
      Swal.fire({
        title: "Done!",
        text: "Song Added Successfully!",
        icon: "success",
      });
      displaysongtable(); // Refresh the table
      // Clear the form (optional)
      fileInput.value = "";
      document.getElementById("songnameinputid").value = "";
      document.getElementById("artistinputid").value = "";
      document.getElementById("albuminputid").value = "";
    }
  } catch (error) {
    console.error("Error uploading info:", error);
    alert("Failed to upload song. Please try again.");
  }
}

async function updatesong() {
  const fileInput = document.getElementById("filegetter1");
  const songno = document.getElementById("songnoinputid").value;
  const songname = document.getElementById("songnameinputid").value;
  const genre = document
    .getElementById("dropdown3")
    .querySelector("p").textContent;
  const artist = document.getElementById("artistinputid").value;
  const album = document.getElementById("albuminputid").value;

  const formData = new FormData();
  formData.append("songno", songno);
  // Validate file input
  if (fileInput.files && fileInput.files.length === 2) {
    formData.append("file1", fileInput.files[0]);
    formData.append("file2", fileInput.files[1]); // Ensure this file exists if required
  }
  formData.append("songname", songname);
  formData.append("genre", genre);
  formData.append("artist", artist);
  formData.append("album", album);

  try {
    const response = await axios.put("/api/songlibrary/updatesongs", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log(response.data.message);
    if (response.data.message === "Song updated successfully") {
      Swal.fire({
        title: "Done!",
        text: "Song Updated Successfully!",
        icon: "success",
      });
      displaysongtable(); // Refresh the table
    }
  } catch (error) {
    console.error("Error updating info:", error);
    alert("Failed to update song. Please try again.");
  }
}

async function deletesong() {
  try {
    const songno = document.getElementById("songnoinputid").value;
    const response = await axios.delete(
      `/api/songlibrary/deletesongs/${songno}`
    );

    if (response.data.message === "Song deleted successfully") {
      Swal.fire({
        title: "Done!",
        text: "Song Deleted Successfully!",
        icon: "success",
      });
      displaysongtable(); // Refresh the table
    }
  } catch (error) {
    console.error("Error deleting info:", error);
    alert("Failed to delete song. Please try again.");
  }
}

/////////////// for song library edit ///////////////

function forsonglibrarytableedit(target, event) {
  if (target.tagName === "BUTTON") {
    if (target.getAttribute("data-songlibedit") != null) {
      const song = data.table1.find(
        (item) => item.songno === target.getAttribute("data-songlibedit")
      );
      document.getElementById("songnoinputid").value = song.songno;
      document.getElementById("songnameinputid").value = song.songname;
      document.getElementById("dropdown3").querySelector("p").textContent =
        song.genre;
      document.getElementById("artistinputid").value = song.artist;
      document.getElementById("albuminputid").value = song.album;
    }
  }
}
///////////////////////////////////////////////
