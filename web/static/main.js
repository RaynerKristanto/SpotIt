function showPage(html) {
    console.log("showPage");
    $("#main").load(html);
}

function submitForm(url, formID, event) {
    console.log("submitForm");
    console.log(document.getElementById(formID));
    console.log(document.getElementById(formID).length);
    event.preventDefault();
    $.ajax({
        type: 'post',
        url: url,
        data: $(document.getElementById(formID)).serialize(),
        success: function() {
            alert("submit successful");
        }
    });
    
}