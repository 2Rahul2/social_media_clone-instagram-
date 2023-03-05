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
// let chatid = '{{chatid}}'
let chatid = document.getElementById('chatid').value


let webUrl = `ws://${window.location.host}/ws/chat-server/${chatid}/`
let chatsocket = new WebSocket(webUrl)
// let wrapper = document.getElementById('msgpage')
let wrapper = document.getElementById('chatpage')


// let sendUser = '{{senderUser}}'
let sendUser = document.getElementById('suser').value
// let currentUser = '{{currentUser}}'
let currentUser = document.getElementById('cuser').value

let lastele = document.getElementById('chatpage')

chatsocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    let item = ''
    let newitem = ''
    console.log(data)
    if(data['type'] === 'chat'){
        let msg = data['message']
        console.log(data['senderuser'])
        console.log(sendUser)
        if (data['senderuser'] === currentUser){
            newitem = `
            <li class="clearfix">
            <div class="message-data align-right">
              <span class="message-data-time" >10:10 AM, Today</span> &nbsp; &nbsp;
              <span class="message-data-name" >${currentUser}</span> <i class="fa fa-circle me"></i>
              
            </div>
            <div style = "background: #cc0066" class="message other-message float-right">
              ${msg}
            </div>
          </li>
            `


            item = `
                <p style="color: red;" id="msgred">${msg}</p>
            `
        }else{

            newitem = `
            <li>
            <div class="message-data">
              <span class="message-data-name"><i class="fa fa-circle online"></i> ${data['senderuser']}</span>
              <span class="message-data-time">10:12 AM, Today</span>
            </div>
            <div style = "background: #ffccff;color:black" class="message my-message">
            ${msg}
            </div>
          </li>
            
            `


            item = `
                <p id="msgred">${msg}</p>
            `
        }
        wrapper.innerHTML += newitem
        // let scrolltoli = lastele.children[lastele.children.length-1]
        // scrolltoli.scrollIntoView()
        
    }
}


function buildMessage(){
    let url = "http://127.0.0.1:8000/api/getmessage/"
    fetch(url , {
        method:'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'cid':chatid
        })
    }).then((Response)=>
        Response.json()
    ).then(function(data){
        console.log(data)
        // msg_data = 
        let nwrapper = document.getElementById('chatpage')
        nwrapper.innerHTML = ""
        let item = ''
        // for(let i in data){
            for(let j in data.msg){
                if(data.msg[j].senderuser['username'] === currentUser){

                    newitem = `
                        <li class="clearfix">
                        <div class="message-data align-right">
                       
                        <span class="message-data-name" >${currentUser}</span> <i  class="fa fa-circle me"></i>
                        
                        </div>
                        <div style = "background: #cc0066" class="message other-message float-right">
                        ${data.msg[j].textmessage}
                        </div>
                    </li>
                        `


                    item = `
                    <p style="color: red;" id="msgred">${data.msg[j].textmessage}</p>
                    `
                }else{

                    newitem = `
                        <li>
                        <div class="message-data">
                        <span  class="message-data-name"><i class="fa fa-circle online"></i> ${data.msg[j].senderuser['username']}</span>
                        
                        </div>
                        <div style = "background: #ffccff;color:black" class="message my-message">
                        ${data.msg[j].textmessage}
                        </div>
                    </li>
            
                        `
                    item = `
                    <p  id="msg">${data.msg[j].textmessage}</p>
                    `
                }
                nwrapper.innerHTML += newitem
            }
        // window.scrollTo(0, document.body.scrollHeight)
        // let lastele = document.getElementById('chatpage')
        // let scrolltoli = lastele.children[lastele.children.length-1]
        // scrolltoli.scrollIntoView()
        
        // document.getElementById('chatpage').scrollIntoView()

        // }
    })
}

buildMessage()

let sendtextbtn = document.getElementById('sendmsg')
sendtextbtn.addEventListener('click' , (e)=>{
    e.preventDefault()
    let msgvalue = document.getElementById('message-to-send')

    chatsocket.send(JSON.stringify({
        'senderuser':currentUser,
        'recieveuser':sendUser,
        'textmessage':msgvalue.value,
        'chatid':chatid
    }))
    let textarea = document.getElementById('message-to-send')
    textarea.value = ' '
})






