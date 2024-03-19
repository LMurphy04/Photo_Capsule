// CODE IS REDUNDANT FOR NOW, KEEPING AS MIGHT REUSE POST LATER FOR LIKES AND COMMENTS
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
    const photoBlocks = Array.from(document.getElementsByClassName("photoBlock"));
    
    photoBlocks.sort((a, b) => {
        const likesA = parseFloat(a.getAttribute(type));
        const likesB = parseFloat(b.getAttribute(type));
        return likesB - likesA;
    });
    
    const photosContainer = document.getElementById("photosContainer");

    photosContainer.innerHTML = ''
    photoBlocks.forEach(photoBlock => {
        photosContainer.appendChild(photoBlock);
    });
}

function hideProfiles() {
    const substring = document.getElementById("search").value;
    const profiles = Array.from(document.getElementsByClassName("profile-link"));
    const noProfiles = document.getElementById("no-profiles");
    noProfiles.removeAttribute("hidden")
    profiles.forEach(profile => {
        const username = profile.firstChild.innerHTML;
        if (username.toLowerCase().includes(substring.toLowerCase())) {
            profile.removeAttribute("hidden");
            noProfiles.setAttribute("hidden", true)
        } else {
            profile.setAttribute("hidden", true);
        }
    });
}