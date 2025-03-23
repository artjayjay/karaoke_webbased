// /// for table /////
///////// mock data //////
let data = {
  table1: [
    {
      songno: 1,
      songname: "Bohemian Rhapsody",
      genre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
    },
    {
      songno: 2,
      songname: "Hotel California",
      genre: "Rock",
      artist: "Eagles",
      album: "Hotel California",
    },
    {
      songno: 3,
      songname: "Stairway to Heaven",
      genre: "Ballad",
      artist: "Led Zeppelin",
      album: "Led Zeppelin IV",
    },
    {
      songno: 4,
      songname: "Smells Like Teen Spirit",
      genre: "Rock",
      artist: "Nirvana",
      album: "Nevermind",
    },
    {
      songno: 5,
      songname: "Imagine",
      genre: "Soul",
      artist: "John Lennon",
      album: "Imagine",
    },
    {
      songno: 6,
      songname: "Hey Jude",
      genre: "Classic",
      artist: "The Beatles",
      album: "The Beatles (White Album)",
    },
    {
      songno: 7,
      songname: "Thriller",
      genre: "Pop",
      artist: "Michael Jackson",
      album: "Thriller",
    },
    {
      songno: 8,
      songname: "Like a Rolling Stone",
      genre: "Classic",
      artist: "Bob Dylan",
      album: "Highway 61 Revisited",
    },
    {
      songno: 9,
      songname: "Purple Haze",
      genre: "Pop",
      artist: "Jimi Hendrix",
      album: "Are You Experienced",
    },
    {
      songno: 10,
      songname: "Sweet Child o' Mine",
      genre: "Rock",
      artist: "Guns N' Roses",
      album: "Appetite for Destruction",
    },
    {
      songno: 11,
      songname: "Billie Jean",
      genre: "Pop",
      artist: "Michael Jackson",
      album: "Thriller",
    },
    {
      songno: 12,
      songname: "Let It Be",
      genre: "Classic",
      artist: "The Beatles",
      album: "Let It Be",
    },
  ],
  table2: [
    {
      queueno: 1,
      songname: "Bohemian Rhapsody",
      genre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
      singername: "John",
    },
    {
      queueno: 2,
      songname: "Bohemian Rhapsody",
      genre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
      singername: "Pedro",
    },
  ],
  table3: [
    {
      songno: 1,
      songname: "Bohemian Rhapsody",
      genre: "Classic",
      artist: "Queen",
      album: "A Night at the Opera",
    },
    {
      songno: 2,
      songname: "Hotel California",
      genre: "Classic",
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
       <td data-label="Song No.">${row.songno}</td>
        <td data-label="Song Name">${row.songname}</td>
        <td data-label="Genre">${row.genre}</td>
        <td data-label="Artist">${row.artist}</td>
        <td data-label="Album">${row.album}</td>
        <td data-label="Edit">
          <button id="${row.songno}" class="btn btn-primary" data-songlibedit="${row.songno}">EDIT</button>
        </td>
    `,
    table2: `
        <td data-label="Queue No.">${row.queueno}</td>
      <td data-label="Song Name">${row.songname}</td>
      <td data-label="Genre">${row.genre}</td>
      <td data-label="Artist">${row.artist}</td>
      <td data-label="Album">${row.album}</td>
      <td data-label="Singer">${row.singername}</td>
      <td data-label="Edit">
        <button id="${row.queueno}" class="btn btn-primary open-modal" data-modal="myModal2" data-songqueueedit="${row.queueno}">EDIT</button>
      </td>
    `,
    table3: `
        <td data-label="Song No.">${row.songno}</td>
      <td data-label="Song Name">${row.songname}</td>
      <td data-label="Genre">${row.genre}</td>
      <td data-label="Artist">${row.artist}</td>
      <td data-label="Album">${row.album}</td>
      <td data-label="Edit">
        <button id="${row.songNo}" class="btn btn-primary" data-songaddqueueedit="${row.songno}">EDIT</button>
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
