$(document).ready(() => {
  console.log('JS working');

  let url = "http://0.0.0.0:5005/";

  $('#submit').on('click', e => {
    e.preventDefault();

    let fileSelect = document.getElementById('file-upload');
    let files = fileSelect.files;

    let form = new FormData();
    for (const file of files) {
      form.append('file', file);
    }

    $.ajax({
      "async": true,
      "crossDomain": true,
      "url": url + "upload",
      "method": "POST",
      "headers": {
        "cache-control": "no-cache",
        "Access-Control-Allow-Origin": "*"
      },
      "processData": false,
      "contentType": false,
      "mimeType": "multipart/form-data",
      "data": form,
      "success": function(data) {
        resetTable();
        showData(data);
      }
    });
  });

  function resetTable() {
    $('#tableBody').innerHTML = '';
  }

  function showData(dataToShow) {
    let print = JSON.parse(dataToShow);
    print['Result'].forEach((dataElement) => {
      let Post = dataElement['Post'];
      let Beskrivelse = dataElement['Beskrivelse'];
      let Enh = dataElement['Enh.'];
      let Mengde = dataElement['Mengde'];
      let Enhetspris = dataElement['Enhetspris'];
      let Sum = dataElement['Sum'];

      let markup = "<tr><td>" +
        Post + "</td><td>" +
        Beskrivelse + "</td><td>" +
        Enh + "</td><td>" +
        Mengde + "</td><td>" +
        Enhetspris + "</td><td>" +
        Sum + "</td></tr>";

      $("#tableBody").append(markup);
    });


  };

});