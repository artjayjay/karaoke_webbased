async function initialfetchsongqueue() {
  try {
    const response = await axios.get(
      "/api/songqueue/displayplayingcurrentsong"
    );
    const song = response.data;

    if (song.queueno != "none" && song.songname) {
      document.getElementById("nameofthesongid").innerHTML =
        song.queueno + "&nbsp;" + song.songname;
    } else {
      document.getElementById("nameofthesongid").innerHTML = "";
    }
  } catch (error) {}
}

initialfetchsongqueue();

async function initialfetchsongsettings() {
  try {
    const response = await axios.get("/api/songsettings/displaysettings");
    const settings = response.data;

    if (settings.mainserver && settings.karaokeserver) {
      karaokeserver = settings.karaokeserver;
    }
  } catch (error) {
    console.error("Error fetching song settings:", error);
    const errorMessage =
      error.response?.data?.detail ||
      "Failed to fetch song settings. Please try again.";
    alert(errorMessage);
  }
}

initialfetchsongsettings();

async function displayqueuetable(limit = 10, offset = 1) {
  try {
    const response = await axios.get(
      `/api/songqueue/displaysongqueue/${limit}/${offset}`
    );
    const fetchedData = response.data;

    // Update the data object with the fetched data
    data.table2 = fetchedData.queue;

    // Re-render the table with the new data
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
  } catch (error) {
    console.error("Error fetching songs:", error);
    alert("Failed to fetch songs. Please try again.");
  }
}

async function displaysongtablesearch(limit = 10, offset = 1) {
  let value = document.getElementById("inputsearchid").value;
  if (!value) value = "";
  try {
    const response = await axios.get(`/api/songqueue/displaysongssearch/`, {
      params: {
        searchterm: value, // Pass searchterm as a query parameter
        limit: limit, // Pass limit as a query parameter
        offset: offset, // Pass offset as a query parameter
      },
    });
    const fetchedData = response.data;

    // Update the data object with the fetched data
    data.table3 = fetchedData.songs;

    // Re-render the table with the new data
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
  } catch (error) {
    console.error("Error fetching songs:", error);
    alert("Failed to fetch songs. Please try again.");
  }
}

async function addnewsongqueue() {
  const songno = document.getElementById("addqueuesongnoid").value;
  const singername = document.getElementById("addqueuesingernameid").value;

  const formData = new FormData();
  formData.append("songno", songno);
  formData.append("singername", singername);

  try {
    const response = await axios.post(
      "/api/songqueue/insertsongqueue",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    console.log(response.data.message);
    if (response.data.message === "Song Queue added successfully") {
      Swal.fire({
        title: "Done!",
        text: "Queue Added Successfully!",
        icon: "success",
      });
      displayqueuetable();
      initialfetchsongqueue();
      document.getElementById("addqueuesongnoid").value = "";
      document.getElementById("addqueuesingernameid").value = "";
    }
  } catch (error) {
    console.error("Error uploading info:", error);
    alert("Failed to upload song. Please try again.");
  }
}

async function updatesongqueue() {
  const queueno = document.getElementById("editqueuenoid").value;
  const singername = document.getElementById("editqueuesingersnameid").value;
  const formData = new FormData();
  formData.append("queueno", queueno);
  formData.append("singername", singername);

  try {
    const response = await axios.put("/api/songqueue/updatequeue", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log(response.data.message);
    if (response.data.message === "Queue updated successfully") {
      Swal.fire({
        title: "Done!",
        text: "Song Queue Updated Successfully!",
        icon: "success",
      });
      displayqueuetable(); // Refresh the table
      initialfetchsongqueue();
    }
  } catch (error) {
    console.error("Error updating info:", error);
    alert("Failed to update queue. Please try again.");
  }
}

async function deletesongqueue() {
  try {
    const queueno = document.getElementById("editqueuenoid").value;
    const response = await axios.delete(
      `/api/songqueue/deletequeue/${queueno}`
    );

    if (response.data.message === "Queue deleted successfully") {
      Swal.fire({
        title: "Done!",
        text: "Song Queue Deleted Successfully!",
        icon: "success",
      });
      displayqueuetable(); // Refresh the table
      initialfetchsongqueue();
    }
  } catch (error) {
    console.error("Error deleting info:", error);
    alert("Failed to delete queue. Please try again.");
  }
}

//////////////////// for song library edit ////////////////////

function forsongaddqueuetableedit(target, event) {
  if (target.tagName === "BUTTON") {
    if (target.getAttribute("data-songaddqueueedit") != null) {
      const song = data.table3.find(
        (item) => item.songno === target.getAttribute("data-songaddqueueedit")
      );
      document.getElementById("addqueuesongnoid").value = song.songno;
    }
  }
}

function forsongeditqueuetableedit(target, event) {
  if (target.tagName === "BUTTON") {
    if (target.getAttribute("data-songqueueedit") != null) {
      const queue = data.table2.find(
        (item) => item.queueno === target.getAttribute("data-songqueueedit")
      );
      document.getElementById("editqueuenoid").value = queue.queueno;
      document.getElementById("editqueuesingersnameid").value =
        queue.singername;
    }
  }
}
//////////////////////////////////////////////////////////////
