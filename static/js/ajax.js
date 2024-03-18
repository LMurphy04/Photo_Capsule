function getProfiles() {
    var xhttp = new	XMLHttpRequest();	
    xhttp.onreadystatechange = function() {	
        if (this.readyState	== 4 &&	this.status	== 200) {	
            document.getElementById("profile-list").innerHTML = this.responseText;
        }
    };
    var search = document.getElementById("search").value;
    xhttp.open("POST","",true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhttp.send("profile="+search);
}

function sortPhotos(type) {
    alert("Feature Coming Soon!")
}