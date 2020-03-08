(function() {
    // Initialize Firebase
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

        google()

        $(document).on("change", ".file_multi_video", function(evt) {
            var $source = $('#video_here');
            $source[0].src = URL.createObjectURL(this.files[0]);
            $source.parent()[0].load();
        });

        document.getElementById('submit').addEventListener('click', e => {
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
                fd.append('description', description)
                $.ajax({
                    url: '/other',
                    type: 'PUT',
                    data: fd,
                    contentType: false,
                    processData: false,
                    success: function(result) {
                        // Do something with the result,
                        console.log(result)
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
                formdata.append('description', description)
                getUrlVideo(formdata) 
            }
        })
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