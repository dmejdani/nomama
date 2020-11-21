document.getElementById("itemadd").addEventListener("click", displayDate);

function displayDate() {
    jQuery("#itemform").clone().appendTo("#bodyreceipt")
}

