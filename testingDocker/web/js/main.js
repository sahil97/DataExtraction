$(document).ready(() => {

  let url = "http://0.0.0.0:5005/";

  let wordList = [];
  let wordObject = [];
  let tag_classes = null;
  const colorKeys = {
    'Type': 'red-tag',
    'Wood/Material': 'purple-tag',
    'sorting': 'green-tag',
    'colour': 'aqua-tag',
    'subfloor': 'peach-tag',
    'uderlay': 'lightblue-tag',
    'others': 'other-tag'
  }
  // Printing for table of keywords

  $('.tag-editor').empty();
  showWords();

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
        $("tbody tr").remove();
        showData(data);
        highlight();
      }
    });
  });

  $('#add-word').on('click', e => {
    e.preventDefault();
    let word = $('#word').val();
    let category = $('#category').val();
    wordObject[category].push(word);

    var req = {
      "async": true,
      "crossDomain": true,
      "url": "http://localhost:5005/wordlist",
      "method": "POST",
      "headers": {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "cache-control": "no-cache"
      },
      "processData": false,
      "data": JSON.stringify({
        "wordObject": wordObject[category],
        "category": category
      })
    };

    $.ajax(req).done(function(response) {});

    $('.tag-editor').empty();
    showWords();
  })


  function showWords() {
    wordObject = [];
    wordList = [];
    $.get(url + "wordlist", function(data, status) {
      wordObject = JSON.parse(data['words']);
      for (let key in wordObject) {
        for (let i = 0; i < wordObject[key].length; i++) {
          wordList.push(wordObject[key][i])
        }
      }
      $('#tags').removeAttr('value');
      $('#tags').tagEditor({
        initialTags: wordList,
        delimiter: ',',
        placeholder: 'Enter tags ...',
        onChange: tag_classes,
        clickDelete: false,
        allowClickEvent: false,
        forceLowercase: true,
        removeDuplicates: true,
        beforeTagSave: function() {},
        beforeTagDelete: function() {}
      });
      tag_classes(null, $('#tags').tagEditor('getTags')[0].editor);
      $('#tags').prop('readonly', 'true');
    });
  }

  function highlighter(word, element, addclass) {
    var rgxp = new RegExp(word, 'g');
    var repl = '<span class="highlightWord ' + addclass + '-text">' + word + '</span>';
    element.html(element.html().replace(rgxp, repl));
  }

  function highlight() {
    $("tbody").find("tr").each(function() {
      for (let key in wordObject) {
        for (let i = 0; i < wordObject[key].length; i++) {
          highlighter(String(wordObject[key][i]), $(this).find('td.displayPara'), colorKeys[key]);
        }
      }
      wordList.forEach(word => {

      });
    })
  }

  tag_classes = (field, editor, tags) => {
    $('li', editor).each(function() {
      var li = $(this);
      for (let key in wordObject) {
        colorClass = colorKeys[key];
        for (let i = 0; i < wordObject[key].length; i++) {
          if (li.find('.tag-editor-tag').html() == wordObject[key][i]) li.addClass(colorClass);
        }
      }
    });
  }

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
        Post + "</td><td class='displayPara'>" +
        Beskrivelse + "</td><td>" +
        Enh + "</td><td>" +
        Mengde + "</td><td>" +
        Enhetspris + "</td><td>" +
        Sum + "</td></tr>";

      $("#tableBody").append(markup);
    });


  };

});