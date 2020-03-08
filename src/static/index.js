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

        $(document).on("change", ".file_multi_video", function(evt) {
            var $source = $('#video_here');
            $source[0].src = URL.createObjectURL(this.files[0]);
            $source.parent()[0].load();

            const fileToUpload = this.files[0]
            console.log(fileToUpload)
            var fd = new FormData();
            fd.append('video', fileToUpload)
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
        });
}());      
    
function getUrlVideo(url) {
    $.ajax({
        url:  "/other",
        type: 'POST',
        contentType: false,
        processData: false,
        data: url,
        success: function(result) {
            // Do something with the result,
            console.log(result)
        },
        error: function(e) {
            console.log(e);
        },
    });
}

function getGoogleSearch() {
    let key = "AIzaSyDg8TOwxGbCQ_KiVdGHSs36VfOlU84SVqc";
    let qry = "nebulas"; 
    let cx  = "";
    let fileType = "png,jpg";
    let searchType = "image";
    let url = "https://www.googleapis.com/customsearch/v1?key=" +key+ "&amp;cx=" +cx+ "&amp;q=" +qry+"&amp;fileType="+fileType+"&amp;searchType="+searchType+"&amp;alt=json";
}