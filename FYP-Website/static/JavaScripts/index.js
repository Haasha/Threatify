function Switch(x){
    
    if (x===1){
        document.getElementById("SignIn").style.display="none";
        document.getElementById("Register").style.display="block";
    }else if (x===2){
        document.getElementById("Register").style.display="none";
        document.getElementById("SignIn").style.display="block";
    }
}