function upperCaseF(a){
    setTimeout(function(){
        a.value = a.value.toUpperCase();
        if(!a.value.charAt(a.value.length-1).match(/[a-z]/i)){
            a.value = a.value.substring(0,a.value.length-1)
        }
    }, 1);
}

function upperCaseT(a){
    setTimeout(function(){
        a.value = a.value.toUpperCase();
        a.value = a.value.replace(/\s+/g, '')
    }, 1);
}