$(document).ready(() => {

  let url = "http://0.0.0.0:5005/";

  let wordList = [];

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
      "url": url + "upload2",
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
    dataToShow = dataToShow.replace("NaN", "0");
    let printData = JSON.parse(dataToShow);
    printData['Result'].forEach((arrayItem, index) => {
      let key = Object.keys(arrayItem)[0];
      let printIndex = index + 1;
      if (key != 'Goods Table') {
        let markup = "<tr><td>" +
          printIndex + "</td><td>" +
          key + "</td><td>" +
          arrayItem[key] + "</td></tr>";
        $("#tableBody").append(markup);
      } else if (key == 'Goods Table') {
        let objToPrint = arrayItem[key];
        let keys = Object.keys(objToPrint);
        let sentence = '<p>';
        keys.forEach((tempKey) => {
          sentence = sentence + tempKey + " : " + objToPrint[tempKey] + "<br/>";
        });
        let markup = "<tr><td>" +
          printIndex + "</td><td>" +
          key + "</td><td>" +
          sentence + "</p></td></tr>";
        $("#tableBody").append(markup);
      }

    });
  };
});