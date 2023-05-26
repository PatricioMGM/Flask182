function onEmailBlur(e) {
    activeElement = null;
    setTimeout(function() {
        if(activeElement == "email"){
        }else{
            if(e.target.value == ""){
                e.target.parentElement.classList.remove("focusWithText");
            }
            //start blinking
            resetFace();
        }
    }, 100);
}

function onEmailLabelClick(e) {
    activeElement = "email";
}

function onPasswordFocus(e) {
    activeElement = "password";
    if(!eyeCovered){
        coverEyes();
    }
}

function stopBlinking(){
    stopBlinking.kill();
    blinking = null;
    TweenMax.set([eyeL, eyeR], {scalev: eyeScale});
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}