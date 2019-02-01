// Constants
var successStatus = "Status.SUCCESS";
var errorStatus = "Status.FAILURE";

function showPage(html) {
    console.log("showPage");
    $("#main").load(html);
}

function submitForm(url, formID, event) {
    let formData = $(document.getElementById(formID)).serialize();
    event.preventDefault();
    $.ajax({
        type: 'post',
        url: url,
        data: formData,
        success: function(resultObj) {
            if (resultObj.status == successStatus) {
                $("#main").remove();
                $("#mainContainer").append("<h4>Invite link: " + resultObj.payload.url + "</h4>");    
            } else {
                $('#error').remove();
                let errorHTML = roomNameTakenHTML.replace("?", document.getElementById("roomID").value);
                $("#main").prepend(errorHTML);
            }
        }
    });
    
}