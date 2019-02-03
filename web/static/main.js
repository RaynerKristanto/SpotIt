// Constants
var successStatus = "Status.SUCCESS";
var errorStatus = "Status.FAILURE";

function showPage(html) {
    console.log("showPage");
    $("#main").load(html);
}

function submitRoomForm(url, formID, event) {
    let formData = $(document.getElementById(formID)).serialize();
    event.preventDefault();
    console.log(formData);
    $.ajax({
        type: 'post',
        url: url,
        data: formData,
        success: function(resultObj) {
            console.log(resultObj);
            if (resultObj.status == successStatus) {
                $("#main").remove();
                $("#mainContainer").append(createRoomLobbyHTML(resultObj.payload.users, resultObj.payload.url));    
            } else {
                $('.error').remove();
                let errorMessage = resultObj.message ? resultObj.message : 'Something went wrong. Please try again';
                let errorHTML = createErrorHTML(errorMessage);
                $("#main").prepend(errorHTML);
            }
        }
    });
}
