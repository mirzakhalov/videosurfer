(function() {
    // Initialize Firebase
     var frames = []
        var firebaseConfig = {
            apiKey: "AIzaSyA5SRwsOGxvkL6DLA1DFmL7iIUAVxrTsr0",
            authDomain: "videosurfer-bad23.firebaseapp.com",
            databaseURL: "https://videosurfer-bad23.firebaseio.com",
            projectId: "videosurfer-bad23",
            storageBucket: "videosurfer-bad23.appspot.com",
            messagingSenderId: "931651516843",
            appId: "1:931651516843:web:c5ad09b8a2a6abffeb3aee",
            measurementId: "G-RCC2W1BE68"
        };
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);    

        //google()

        $(document).on("change", ".file_multi_video", function(evt) {
            var $source = $('#video_here');
            $source[0].src = URL.createObjectURL(this.files[0]);
            $source.parent()[0].load();
        });

        var selectedTask = ''
        document.getElementById('shopping').addEventListener('click', e => {
            selectedTask = 'shopping'
        })

        document.getElementById('caption').addEventListener('click', e => {
            selectedTask = 'caption'
        })

        document.getElementById('transcript').addEventListener('click', e => {
            selectedTask = 'transcript'
        })

        document.getElementById('submit').addEventListener('click', e => {
            if(selectedTask === '') {
                const filesToUpload = document.getElementsByClassName('file_multi_video')[0].files
                let video_link = document.getElementById('url').value
                let description = document.getElementById('description').value
                if(video_link != '' && filesToUpload.length != 0)
                    alert("Please, either remove the URL or refresh the page to remove the uploaded video")
                else if(video_link == '' && filesToUpload.length == 0)
                    alert("Please, either paste the URL or upload the video to process")
                else if(filesToUpload.length != 0) {
                    var fd = new FormData();
                    fd.append('video', filesToUpload[0])
                    $.ajax({
                        url: '/other',
                        type: 'PUT',
                        data: fd,
                        contentType: false,
                        processData: false,
                        success: function(result) {
                            // Do something with the result,
                            console.log(result)
                            doCaption(result, description)
                        },
                        error: function(e) {
                            console.log(e);
                        },
                    });

                }
                else 
                {
                    var formdata = new FormData();
                    formdata.append('url', video_link)
                    getUrlVideo(formdata) 
                }
            }
            else 
                alert("Please, choose one of the actions to take in the dropdown menu")
        })

        var init = function() {
            Pagination.Init(document.getElementById('pagination'), {
                size: frames.length, // pages size
                page: 1,  // selected page
                step: 3   // pages before and after current
            });
        };
        
        document.addEventListener('DOMContentLoaded', init, false);
}());      
    
function getUrlVideo(data) {
    $.ajax({
        url:  "/other",
        type: 'POST',
        contentType: false,
        processData: false,
        data: data,
        success: function(result) {
            // Do something with the result,
            console.log(result)
        },
        error: function(e) {
            console.log(e);
        },
    });
}

function google(){
    var xhr = new XMLHttpRequest();
    let google = "https://www.google.com/searchbyimage?"
    let image_link = "https://i.ebayimg.com/images/g/mwQAAOSw1Tdb80~p/s-l500.jpg"
    let url_specify = "site=search&image_url="
    xhr.open("GET", google + url_specify + image_link, true);
    xhr.onload = function (e) {
    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            let html = xhr.responseText;
            let description = html.substring(html.indexOf('title="Search" value="') + 22, html.indexOf(' aria-label="Search"') - 1)
            getEbayDescription(google + "q=" + description + "+ebay&" + url_specify + image_link)
            console.log(description)
        } else {
            console.error(xhr.statusText);
        }
    }
    };
    xhr.onerror = function (e) {
    console.error(xhr.statusText);
    };
    xhr.send(null); 
}

function getEbayDescription(url) {
    console.log(url)
    let ebay_descriptions = ''
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onload = function (e) {
    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            let html = xhr.responseText;
            var allProducts = new Set();
            let index = 1, ebay_description;
            //console.log(html)
            while(index >= 0){
                index = html.indexOf("https://www.ebay.com/itm/", index + 1)
                //console.log(index)
                if(index >= 0){
                    ebay_description = html.substring(index + 25, html.indexOf("/", index + 26))
                    //console.log(ebay_description)
                    if(!allProducts.has(ebay_description))
                    {
                        allProducts.add(ebay_description)
                        //console.log(ebay_description)
                        ebay_description = ebay_description.split("-").join(" ");
                        ebay_descriptions = `${ebay_descriptions} - ${ebay_description} `
                    }
                }
            }

            console.log(ebay_descriptions)
            getEbayProducts(ebay_descriptions.toLowerCase())

        } else {
            console.error(xhr.statusText);
        }
    }
    };
    xhr.onerror = function (e) {
    console.error(xhr.statusText);
    };
    xhr.send(null); 
}

function getEbayProducts(data) {
    var formdata = new FormData();
    formdata.append('list', data)
    $.ajax({
        url:  "/get_ebay_products",
        type: 'POST',
        contentType: false,
        processData: false,
        data: formdata,
        success: function(result) {
            // Do something with the result,
            var allResults = Object.values(result)[0]
            console.log(allResults)
            var row = document.createElement('div')
            row.className = 'row list'
            for(var i = 0; i < allResults.length; i++)
            {
                var col = document.createElement('div')
                col.className = "col-md-3 postCover"
                var divCover = document.createElement('div')
                divCover.className = "cover"
                var image = document.createElement('img')
                image.src = allResults[i].url
                var divName = document.createElement('div')
                divName.className = "name"
                divName.innerHTML = allResults[i].title.toLowerCase()
                var divPrice = document.createElement('div')
                divPrice.className = "coverPrice"
                divPrice.innerHTML = "$ " + allResults[i].price
                divCover.appendChild(divName)
                divCover.appendChild(divPrice)
                col.appendChild(image)
                col.appendChild(divCover)
                row.appendChild(col)
            }

            document.getElementById('ebayPosts').appendChild(row)
        },
        error: function(e) {
            console.log(e);
        },
    });
}

/* * * * * * * * * * * * * * * * *
 * Pagination
 * javascript page navigation
 * * * * * * * * * * * * * * * * */

var Pagination = {

    code: '',

    // --------------------
    // Utility
    // --------------------

    // converting initialize data
    Extend: function(data) {
        data = data || {};
        Pagination.size = data.size || 300;
        Pagination.page = data.page || 1;
        Pagination.step = data.step || 3;
    },

    // add pages by number (from [s] to [f])
    Add: function(s, f) {
        for (var i = s; i < f; i++) {
            Pagination.code += '<a>' + i + '</a>';
        }
    },

    // add last page with separator
    Last: function() {
        Pagination.code += '<i>...</i><a>' + Pagination.size + '</a>';
    },

    // add first page with separator
    First: function() {
        Pagination.code += '<a>1</a><i>...</i>';
    },



    // --------------------
    // Handlers
    // --------------------

    // change page
    Click: function() {
        Pagination.page = +this.innerHTML;
        Pagination.Start();
        var video = document.getElementById('video')
        video.currentTime = frames[Pagination.page - 1]
        video.play()
    },

    // previous page
    Prev: function() {
        Pagination.page--;
        if (Pagination.page < 1) {
            Pagination.page = 1;
        }
        Pagination.Start();
    },

    // next page
    Next: function() {
        Pagination.page++;
        if (Pagination.page > Pagination.size) {
            Pagination.page = Pagination.size;
        }
        Pagination.Start();
    },



    // --------------------
    // Script
    // --------------------

    // binding pages
    Bind: function() {
        var a = Pagination.e.getElementsByTagName('a');
        for (var i = 0; i < a.length; i++) {
            if (+a[i].innerHTML === Pagination.page) a[i].className = 'current';
            a[i].addEventListener('click', Pagination.Click, false);
        }
    },

    // write pagination
    Finish: function() {
        Pagination.e.innerHTML = Pagination.code;
        Pagination.code = '';
        Pagination.Bind();
    },

    // find pagination type
    Start: function() {
        if (Pagination.size < Pagination.step * 2 + 6) {
            Pagination.Add(1, Pagination.size + 1);
        }
        else if (Pagination.page < Pagination.step * 2 + 1) {
            Pagination.Add(1, Pagination.step * 2 + 4);
            Pagination.Last();
        }
        else if (Pagination.page > Pagination.size - Pagination.step * 2) {
            Pagination.First();
            Pagination.Add(Pagination.size - Pagination.step * 2 - 2, Pagination.size + 1);
        }
        else {
            Pagination.First();
            Pagination.Add(Pagination.page - Pagination.step, Pagination.page + Pagination.step + 1);
            Pagination.Last();
        }
        Pagination.Finish();
    },



    // --------------------
    // Initialization
    // --------------------

    // binding buttons
    Buttons: function(e) {
        var nav = e.getElementsByTagName('a');
        nav[0].addEventListener('click', Pagination.Prev, false);
        nav[1].addEventListener('click', Pagination.Next, false);
    },

    // create skeleton
    Create: function(e) {

        var html = [
            '<a>&#9668;</a>', // previous button
            '<span></span>',  // pagination container
            '<a>&#9658;</a>'  // next button
        ];

        e.innerHTML = html.join('');
        Pagination.e = e.getElementsByTagName('span')[0];
        Pagination.Buttons(e);
    },

    // init
    Init: function(e, data) {
        Pagination.Extend(data);
        Pagination.Create(e);
        Pagination.Start();
    }
};



/* * * * * * * * * * * * * * * * *
* Initialization
* * * * * * * * * * * * * * * * */


function doCaption(filename, description) {
    var data = new FormData()
    data.append('filename', filename)
    data.append('inp', description)
    $.ajax({
        url:  "/search/caption",
        type: 'POST',
        contentType: false,
        processData: false,
        data: data,
        success: function(result) {
            // Do something with the result,
            console.log(result)
        },
        error: function(e) {
            console.log(e);
        },
    });
}

function dropdown() {
    var x, i, j, selElmnt, a, b, c;
/* Look for any elements with the class "custom-select": */
x = document.getElementsByClassName("custom-select");
for (i = 0; i < x.length; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  /* For each element, create a new DIV that will act as the selected item: */
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /* For each element, create a new DIV that will contain the option list: */
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < selElmnt.length; j++) {
    /* For each option in the original select element,
    create a new DIV that will act as an option item: */
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /* When an item is clicked, update the original select box,
        and the selected item: */
        var y, i, k, s, h;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        h = this.parentNode.previousSibling;
        for (i = 0; i < s.length; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            for (k = 0; k < y.length; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
    /* When the select box is clicked, close any other select boxes,
    and open/close the current select box: */
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("select-hide");
    this.classList.toggle("select-arrow-active");
  });
}

function closeAllSelect(elmnt) {
  /* A function that will close all select boxes in the document,
  except the current select box: */
  var x, y, i, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  for (i = 0; i < y.length; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < x.length; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);
}