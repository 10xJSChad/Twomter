function showFirstThreeReplies(){
    let x = document.getElementsByClassName("twomtBox");
    let y = document.getElementsByClassName("twomtResponses");

    for(let i = 0; i < x.length; i++){
        let count = 0;
        twomtID = x[i].getAttribute("data-value");
        addListener('twomtBox' + twomtID, 'characterCountText' + twomtID, 'postTwomtButton' + twomtID)
        for(let j = 0; j < y.length; j++){
            replyID = y[j].getAttribute("data-value");
            if(twomtID == replyID){
                y[j].style.display = 'block';
                count++;
                if(count == 3){ break; }
            }
        }
    }
}

function showAllReplies(id){
    let x = document.getElementsByClassName("twomtResponses");
    let y = document.getElementsByClassName("showResponsesButton");
    for(let i = 0; i < x.length; i++){
        replyID = x[i].getAttribute("data-value");
        if(replyID == id){
            x[i].style.display = 'block';
        }
    }
    
    for(let i = 0; i < y.length; i++){
        buttonID = y[i].getAttribute("data-value");
        if(buttonID == id){
            y[i].style.display = 'none';
        }
    }
}

function showReplyBox(id){
    let x = document.getElementsByClassName("replyBox");
    let y = document.getElementsByClassName("replyBtn");

    for (let i = 0; i < x.length; i++) {
        if(x[i].id == id){
            x[i].style.display = 'block'; y[i].style.display = 'none';
        } else{ x[i].style.display = 'none'; y[i].style.display = 'block'; }
    } 
}


window.addEventListener('load', function () {
    showFirstThreeReplies();
    addListener('twomtBox', 'characterCountText', 'postTwomtButton')
  })

  function addListener(twomtBoxID, characterCountTextID, postTwomtButtonID){
    document.getElementById(twomtBoxID).onkeyup = function () {
        document.getElementById(characterCountTextID).innerHTML = "Characters left: " + (140 - this.value.length);
        if(this.value.length > 140){
            document.getElementById(characterCountTextID).style.color = "red";
            document.getElementById(postTwomtButtonID).disabled = true;
        } else {
            document.getElementById(characterCountTextID).style.color = "black";
            document.getElementById(postTwomtButtonID).disabled = false;
        }
  }
}
