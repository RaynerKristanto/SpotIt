base_endpoint = "http://127.0.0.1:5000/";

async function post_api_data(command, payload) {
    var result_data = null;
    try {
        var result = await $.ajax({
            type:"POST",
            url: base_endpoint + command,
            data: payload,
            success: function (data) {
               result_data = data;
            }
        });

    } catch (e) {
        console.log("ERRORs");
        console.log(e);
    }
    console.log(result_data);
    return result_data;
}

var router = new Router({
    mode: 'history',
    page404: function (path) {
        console.log('"/' + path + '" Page not found');
    }
});

Handlebars.registerHelper('userList', function(context, options) {
    var ret = "<ul class='list-group'>";
    for(var i=0; i<context.length; i++) {
      ret += "<li class='list-group-item'>" + options.fn(context[i]) + "</li>";
    }
    ret += "</ul>";
    return ret;
});

/**
 * Helper to POST room join event
 * Expects arguments for userID and roomID
 * @param {} payload 
 */
async function joinRoom(payload){
    
    var result = await post_api_data("join", payload);
    console.log(result);

    if (result.status == "Status.SUCCESS") {
        router.navigateTo(result.payload.url)
    }

}

async function createRoom(payload){
    var result = await post_api_data("create", payload);
    console.log(result);

    if (result.status == "Status.SUCCESS") {
        router.navigateTo(result.payload.url)
    }

}

async function joinRoomFromForm(formID){
    var payload = {
        "userID" : $("#" + formID + " #userID").val(),
        "roomID" : $("#" + formID + " #roomID").val()
    }
    await joinRoom(payload);
}


// async function joinRoomFromInvite(formID){
//     var urlArgs = window.location.split("/");
//     var roomID = urlArgs[urlArgs.length - 1];
//     var payload = {
//         "userID" : $("#" + formID + " #userID").val(),
//         "roomID" : roomID
//     };
//     await joinRoom(payload);

async function createRoomFromForm(formID){
    var payload = {
        "userID" : $("#" + formID + " #userID").val(),
        "roomID" : $("#" + formID + " #roomID").val()
    }
    await createRoom(payload);
}

async function createRoomFromForm(formID) {
    var formData = $("#" + formID).serialize();
    var result = await post_api_data("create", formData)
    console.log(result);

    if (result.status === "Status.SUCCESS") {
        console.log("navigating now" + result.payload.url)
        router.navigateTo(result.payload.url)
    }
}


router.add('/', function()  {

    template_context = {
        "joinRoom" : "joinRoomFromForm('roomForm')",
        "createRoom" : "createRoomFromForm('roomForm')"
    }
    $("#mainContainer").html(templates_compiled["INITIAL_CREATE_TEMPLATE"](template_context));
});


router.add('room/{room}', async function(room){

    // Check to see if they belong to the room, otherwise reroute to /
    var result = await post_api_data('status', {});
    if (result.payload.roomID != room) {
        alert("You don't belong to this room!");
        router.navigateTo("/")
        return;
    }

    var result = await post_api_data("room_status", {});
    console.log("RESULT " + result);
    var userList = result.payload.users;
    // Convert the list of users from ["usera", "userb"] --> [{"userID" : "usera"}, {"userID" : "userb"}]
    userListContext = []
    for (var i = 0; i < userList.length; i++) {
        userListContext.push({"userID": userList[i]})
    }
    template_context = {
        "inviteLink" : base_endpoint + "invite/" + room,
        "availableUsers" : userListContext
    }
    $("#mainContainer").html(templates_compiled["LOBBY_TEMPLATE"](template_context));
});

router.add('invite/{room}', async function(room){
    template_context = {
        "joinRoom" : "joinRoom({userID:$('#userID').val(), roomID:"+ room +"})"
    };
    $("#mainContainer").html(templates_compiled["INVITE_JOIN_TEMPLATE"](template_context));
});



// router.addUriListener();

// Need to officially "route" to current path to execute behavior when url loaded from the url bar
function initRouter() {
    router.navigateTo(window.location.pathname);
}


$(document).ready(function() {
    initRouter();
});
