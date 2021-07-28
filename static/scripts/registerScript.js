
window.addEventListener('load', function () {
    addListener('username')
    addListener('password')
  })

  function addListener(element){
    document.getElementById(element).onkeyup = function () {
        checkValid();
  }
}

function checkValid(){
    let usernameBox = document.getElementById('username')
    let passwordBox = document.getElementById('password')
    let submitButton = document.getElementById('submit')

    let usernameInvalid = document.getElementById('usernameShort')
    let passwordInvalid = document.getElementById('passwordShort')

    usernameInvalid.textContent = "Username too short";

    if(usernameBox.value.length > 3 && passwordBox.value.length > 4){
        submitButton.disabled = false;
    } else {submitButton.disabled = true;}

    if(usernameBox.value.length > 3){
        usernameInvalid.style.display = 'none';
    } else { usernameInvalid.style.display = 'block'; }

    if(passwordBox.value.length > 4){
        passwordInvalid.style.display = 'none';
    } else { passwordInvalid.style.display = 'block'; }

    if(!isAlphaNumeric(usernameBox.value)){
        usernameInvalid.textContent = "Special characters are not allowed";
        usernameInvalid.style.display = 'block';
        submitButton.disabled = true;
    }

    if(usernameBox.value.length > 13){
        usernameInvalid.textContent = "Username too long";
        usernameInvalid.style.display = 'block';
        submitButton.disabled = true;
    }
}

function isAlphaNumeric(str) {
    var code, i, len;
  
    for (i = 0, len = str.length; i < len; i++) {
      code = str.charCodeAt(i);
      if (!(code > 47 && code < 58) && // numeric (0-9)
          !(code > 64 && code < 91) && // upper alpha (A-Z)
          !(code > 96 && code < 123)) { // lower alpha (a-z)
        return false;
      }
    }
    return true;
  };