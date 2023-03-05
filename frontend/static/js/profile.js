function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// let u = '{{user.username}}'
let u = document.getElementById('cuser').value
// let current_user = '{{request.user}}'
let current_user = document.getElementById('requser').value
let followbtn = document.getElementById('followbtn')
let messagebtn = document.getElementById('msgme')
let postWrapper = document.querySelector('.gallery')
postWrapper.innerHTML = ""
let postitem = ""
loadProfilePost()
function loadProfilePost(){
    let posturl = `/api/profile-post/`
    console.log(posturl)
    fetch(posturl ,{
        method:"POST",
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'name':u
        })
    }).then((Response)=>
    Response.json()
    ).then((data)=>{
        // console.log(data)
    
        for(let i in data){
            // console.log(data[i].id)
            postitem = `
            <div class="gallery-item" tabindex="0">
    
                    <img src="${data[i].postimg}" class="gallery-image" alt="">
    
                    <div class="gallery-item-info">
    
                        <ul>
                            <li class="gallery-item-likes"><span class="visually-hidden">Likes:</span><i class="fas fa-heart" aria-hidden="true"></i>&#10084;   ${data[i]['like_count']}</li>
                            <li class="gallery-item-comments"><span class="visually-hidden">Comments:</span><i class="fas fa-comment" aria-hidden="true"></i> &#9783;   ${data[i]['comment_count']}</li>
                        </ul>
    
                    </div>
    
                </div>

            `
            postWrapper.innerHTML += postitem
            // console.log(data[i])
        }
    })
}


messagebtn.addEventListener('click' , messagefunction)
followbtn.addEventListener('click' , followfun)
function messagefunction(){
    console.log("creating message")
    messageUrl = `http://127.0.0.1:8000/api/create-msgroom/`
    fetch(messageUrl , {
        method:'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({
            'fromuser':current_user,
            'touser':u,

        })
    }
    ).
    then((Response)=>Response.json()).then(function (data){
        msgid = data
        window.location.href = `http://127.0.0.1:8000/text/${msgid}`
        console.log(data)
    })
}
function followfun(){
    console.log("fun")
    let url = `http://127.0.0.1:8000/api/follow/`
    fetch(url ,{
        method:'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'fromuser':current_user,
            'touser':u,
        })
    }).then((Response)=>{
        console.log("following")
    })
}