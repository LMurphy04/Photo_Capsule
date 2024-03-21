// Photo Like Unlike
function like_unlike(button) {
    const xhttp = new XMLHttpRequest();	
    
    xhttp.onreadystatechange = function() {	
        if (this.readyState	== 4 &&	this.status	== 200) {
            const response = JSON.parse(this.responseText);
            
            if (response["status"] == "success") {
                const likeCount = document.getElementById("likeCount");
                if (type == "Like") {

                    // If liked, increment counter and switch to unlike button
                    likeCount.innerHTML = parseInt(likeCount.innerHTML) + 1
                    button.setAttribute("data-like-or-unlike", "Unlike")
                    button.innerHTML = "Unlike ♥"

                } else if (type == "Unlike") {

                    // If unliked, decrement counter and switch to like button
                    likeCount.innerHTML = parseInt(likeCount.innerHTML) - 1
                    button.setAttribute("data-like-or-unlike", "Like")
                    button.innerHTML = "Like ♥"

                }
            }
        }
    };

    // Get whether user is liking or unliking post
    const type = button.getAttribute("data-like-or-unlike");

    xhttp.open("POST","/photocapsule/like/",true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhttp.send("type="+type+"&photo="+photo+"&user="+user);
}

// Add Comment
function addComment() {
    const xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {	
        if (this.readyState	== 4 &&	this.status	== 200) {
            const response = JSON.parse(this.responseText);

            if (response["status"] == "success") {

                // Clear comment box
                commentBox.value = '';

                // Display new comment
                const commentContainer = document.getElementById("commentContainer");
                if (commentContainer.getAttribute("data-empty") == "True") {
                    // If there were no comments, remove 'no comments' message
                    commentContainer.innerHTML = '';
                    commentContainer.setAttribute("data-empty","False");
                }
                commentContainer.innerHTML = response['comment'] + commentContainer.innerHTML;

            }
        }
    };

    // Get user comment to add
    const commentBox = document.getElementById("comment");
    const comment = commentBox.value;

    // If comment is not empty, process request
    if (comment.trim() != '') {
        xhttp.open("POST","/photocapsule/comment/",true);
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhttp.send("comment="+comment+"&photo="+photo+"&user="+user);
    }
}


// Sort Photos
function sortPhotos(type) {
    const photoBlocks = Array.from(document.getElementsByClassName("photoBlock"));
    
    // Sort photo divs by either upload date or likes
    photoBlocks.sort((a, b) => {
        const likesA = parseFloat(a.getAttribute(type));
        const likesB = parseFloat(b.getAttribute(type));
        return likesB - likesA;
    });
    
    // Repopulate photo container in new order
    const photosContainer = document.getElementById("photosContainer");
    photosContainer.innerHTML = ''
    photoBlocks.forEach(photoBlock => {
        photosContainer.appendChild(photoBlock);
    });
}


// Browse Profiles Search Bar
function hideProfiles() {
    const substring = document.getElementById("search").value; // User search
    const profiles = Array.from(document.getElementsByClassName("profile-link")); // Profiles
    const noProfiles = document.getElementById("no-profiles"); // No profiles message
    
    // Show profiles containing user search substring, if none show no profiles message
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