function Switch(x){
    
    if (x===1){
        document.getElementById("motion").style.display="none";
        document.getElementById("general").style.display="block";
        document.getElementById("crime").style.display="none";
        document.getElementById("general").getElementsByTagName('td')[0].style.width="40%";
        document.getElementById("general").getElementsByTagName('td')[1].style.width="40%";
        document.getElementById("general").getElementsByTagName('td')[2].style.width="20%";

    }else if (x===2){
        document.getElementById("general").style.display="none";
        document.getElementById("motion").style.display="block";
        document.getElementById("crime").style.display="none";
        document.getElementById("motion").getElementsByTagName('td')[0].style.width="40%";
        document.getElementById("motion").getElementsByTagName('td')[1].style.width="40%";
        document.getElementById("motion").getElementsByTagName('td')[2].style.width="20%";

    }
else if (x===3){
    document.getElementById("general").style.display="none";
    document.getElementById("motion").style.display="none";
    document.getElementById("crime").style.display="block";
    document.getElementById("crime").getElementsByTagName('td')[0].style.width="40%";
    document.getElementById("crime").getElementsByTagName('td')[1].style.width="40%";
    document.getElementById("crime").getElementsByTagName('td')[2].style.width="20%";

}

}
function inverse (x){
    if (x=="name"){
        if (document.getElementById("nameInput").style.display!="none") {
            document.getElementById("nameInput").style.display="none";
            document.getElementById("nameText").style.display="block";
            document.getElementById("nameText").innerText=document.getElementById("nameInput1").value;

        }
        else{
            document.getElementById("nameInput").style.display="block";
            document.getElementById("nameText").style.display="none";
        }
        
        Switch(1);

    }
    if (x=="phone"){
        if (document.getElementById("phoneInput").style.display!="none") {
            document.getElementById("phoneInput").style.display="none";
            document.getElementById("phoneText").style.display="block";
            document.getElementById("phoneText").innerText=document.getElementById("phoneInput1").value;
        }
        else{
            document.getElementById("phoneInput").style.display="block";
            document.getElementById("phoneText").style.display="none";
        }
        
        Switch(1);

    }
    if (x=="ssn"){
        if (document.getElementById("ssnInput").style.display!="none") {
            document.getElementById("ssnInput").style.display="none";
            document.getElementById("ssnText").style.display="block";
            document.getElementById("ssnText").innerText=document.getElementById("ssnInput1").value;
        }
        else{
            document.getElementById("ssnInput").style.display="block";
            document.getElementById("ssnText").style.display="none";
        }
        
        Switch(1);

    }
    if (x=="address"){
        if (document.getElementById("addressInput").style.display!="none") {
            document.getElementById("addressInput").style.display="none";
            document.getElementById("addressText").style.display="block";
            document.getElementById("addressText").innerText=document.getElementById("addressInput1").value;
        }
        else{
            document.getElementById("addressInput").style.display="block";
            document.getElementById("addressText").style.display="none";
        }
        
        Switch(1);

    }
    if (x=="city"){
        if (document.getElementById("cityInput").style.display!="none") {
            document.getElementById("cityInput").style.display="none";
            document.getElementById("cityText").style.display="block";
            document.getElementById("cityText").innerText=document.getElementById("cityInput1").value;
        }
        else{
            document.getElementById("cityInput").style.display="block";
            document.getElementById("cityText").style.display="none";
        }
        
        Switch(1);

    }
    if (x=="country"){
        if (document.getElementById("countryInput").style.display!="none") {
            document.getElementById("countryInput").style.display="none";
            document.getElementById("countryText").style.display="block";
            document.getElementById("countryText").innerText=document.getElementById("countryInput1").value;
        }
        else{
            document.getElementById("countryInput").style.display="block";
            document.getElementById("countryText").style.display="none";
        }
        
        Switch(1);

    }    if (x=="longitude"){
        if (document.getElementById("longitudeInput").style.display!="none") {
            document.getElementById("longitudeInput").style.display="none";
            document.getElementById("longitudeText").style.display="block";
            document.getElementById("longitudeText").innerText=document.getElementById("longitudeInput1").value;
        }
        else{
            document.getElementById("longitudeInput").style.display="block";
            document.getElementById("longitudeText").style.display="none";
        }
        
        Switch(1);

    }    if (x=="lattitude"){
        if (document.getElementById("lattitudeInput").style.display!="none") {
            document.getElementById("lattitudeInput").style.display="none";
            document.getElementById("lattitudeText").style.display="block";
            document.getElementById("lattitudeText").innerText=document.getElementById("lattitudeInput1").value;
        }
        else{
            document.getElementById("lattitudeInput").style.display="block";
            document.getElementById("lattitudeText").style.display="none";
        }
        
        Switch(1);

    }    if (x=="timezone"){
        if (document.getElementById("timezoneInput").style.display!="none") {
            document.getElementById("timezoneInput").style.display="none";
            document.getElementById("timezoneText").style.display="block";
            document.getElementById("timezoneText").innerText=document.getElementById("timezoneInput1").value;
        }
        else{
            document.getElementById("timezoneInput").style.display="block";
            document.getElementById("timezoneText").style.display="none";
        }
        
        Switch(1);

    }
    if (x=="m_detection"){
        if (document.getElementById("m_detectionInput").style.display!="none") {
            document.getElementById("m_detectionInput").style.display="none";
            document.getElementById("m_detectionText").style.display="block";
            document.getElementById("m_detectionText").innerText=document.getElementById("m_detectionInput1").value;
        }
        else{
            document.getElementById("m_detectionInput").style.display="block";
            document.getElementById("m_detectionText").style.display="none";
        }
        
        Switch(2);

    }
    if (x=="m_alert"){
        if (document.getElementById("m_alertInput").style.display!="none") {
            document.getElementById("m_alertInput").style.display="none";
            document.getElementById("m_alertText").style.display="block";
            document.getElementById("m_alertText").innerText=document.getElementById("m_alertInput1").value;
        }
        else{
            document.getElementById("m_alertInput").style.display="block";
            document.getElementById("m_alertText").style.display="none";
        }
        
        Switch(2);

    }
    if (x=="m_sensitivity"){
        if (document.getElementById("m_sensitivityInput").style.display!="none") {
            document.getElementById("m_sensitivityInput").style.display="none";
            document.getElementById("m_sensitivityText").style.display="block";
            document.getElementById("m_sensitivityText").innerText=document.getElementById("m_sensitivityInput1").value;
        }
        else{
            document.getElementById("m_sensitivityInput").style.display="block";
            document.getElementById("m_sensitivityText").style.display="none";
        }
        
        Switch(2);

    }
    if (x=="c_detection"){
        if (document.getElementById("c_detectionInput").style.display!="none") {
            document.getElementById("c_detectionInput").style.display="none";
            document.getElementById("c_detectionText").style.display="block";
            document.getElementById("c_detectionText").innerText=document.getElementById("c_detectionInput1").value;
        }
        else{
            document.getElementById("c_detectionInput").style.display="block";
            document.getElementById("c_detectionText").style.display="none";
        }
        
        Switch(3);

    }
    if (x=="c_alert"){
        if (document.getElementById("c_alertInput").style.display!="none") {
            document.getElementById("c_alertInput").style.display="none";
            document.getElementById("c_alertText").style.display="block";
            document.getElementById("c_alertText").innerText=document.getElementById("c_alertInput1").value;
        }
        else{
            document.getElementById("c_alertInput").style.display="block";
            document.getElementById("c_alertText").style.display="none";
        }
        
        Switch(3);

    }
    if (x=="c_sensitivity"){
        if (document.getElementById("c_sensitivityInput").style.display!="none") {
            document.getElementById("c_sensitivityInput").style.display="none";
            document.getElementById("c_sensitivityText").style.display="block";
            document.getElementById("c_sensitivityText").innerText=document.getElementById("c_sensitivityInput1").value;
        }
        else{
            document.getElementById("c_sensitivityInput").style.display="block";
            document.getElementById("c_sensitivityText").style.display="none";
        }
        
        Switch(3);
    }

}

function change (x){
    alert(x);
    document.getElementsByID(x).style.display="block";

}
