document.getElementById("itemadd").addEventListener("click", displayDate);

function displayDate() {
    jQuery("#itemform").clone().appendTo("#bodyreceipt")
    
    // jQuery("#itemform").append(jQuery("#itemform").children().first().clone());

}

