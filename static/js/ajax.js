function like_unlike(button) {
    var xhttp = new	XMLHttpRequest();	
    xhttp.onreadystatechange = function() {	
        if (this.readyState	== 4 &&	this.status	== 200) {
            const response = JSON.parse(this.responseText);
            if (response["status"] == "success") {
                const likeCount = document.getElementById("likeCount");
                if (type == "Like") {
                    likeCount.innerHTML = parseInt(likeCount.innerHTML) + 1
                    button.setAttribute("data-like-or-unlike", "Unlike")
                    button.innerHTML = "Unlike ♥"
                } else if (type == "Unlike") {
                    likeCount.innerHTML = parseInt(likeCount.innerHTML) - 1
                    button.setAttribute("data-like-or-unlike", "Like")
                    button.innerHTML = "Like ♥"
                }
            }
        }
    };
    const type = button.getAttribute("data-like-or-unlike");
    const photo = button.getAttribute("data-photo");
    const user = button.getAttribute("data-current-user");
    xhttp.open("POST","/photocapsule/like/",true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhttp.send("type="+type+"&photo="+photo+"&user="+user);
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

// Add comments
$('#comment-form').submit(function(e) {
    e.preventDefault(); 
    $.ajax({
        type: $(this).attr('method'), 
        url: $(this).attr('action'), 
        data: $(this).serialize(), 
        success: function(response) {
            $('#comments-section').append(response.comment_html);
            $('#id_comment_text').val('');
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});

// Search profile
// $('#search-input').keyup(function() {
//     $.ajax({
//         type: 'GET',
//         url: '/search_profiles/', 
//         data: {
//             'search_term': $(this).val() 
//         },
//         success: function(response) {
//             $('#profiles-list').html(response.profiles_html);
//         }
//     });
// });

//Add sorting function
// $('#sort-options').change(function() {
//     $.ajax({
//         type: 'GET',
//         url: '/sort_results/', 
//         data: {
//             'sort_by': $(this).val() 
//         },
//         success: function(response) {
//             $('#results-list').html(response.results_html);
//         }
//     });
// });

// Userlike
//<button class="like-btn" data-id="{{ photo.id }}">like</button>
document.addEventListener('DOMContentLoaded', function () {
    var likeBtns = document.querySelectorAll('.like-btn');
    likeBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var photoId = this.getAttribute('data-id');
            var action = this.textContent.trim().toLowerCase() === 'like' ? 'like' : 'unlike';
            fetch("{% url 'like_photo' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-CSRFToken': csrf_token,
                },
                body: 'photo_id=' + photoId + '&action=' + action
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    
                    this.textContent = action === 'like' ? 'unlike' : 'like';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
