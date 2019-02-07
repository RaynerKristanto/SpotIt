function createErrorHTML(errorMessage) {
    return "<h4 class='error'>" + errorMessage + "</h4>";
}

function createRoomLobbyHTML(users, url) {

    let html = "" +
        "<div id='main'>" +
        "<h4>Invite link: http://" + document.domain + ":" + location.port + url + "</h4>" +
        createUserListHTML(users) +
        "</div>";
    return html;
}

function createUserListHTML(users) {
    let userList = "<ul id='userList' class='list-group'>";
    users.forEach(user => {
        userList = userList + createUserListItemHTML(user) + "\n";
    });
    userlist = userList + "</ul>"
    return userList;
}

function createUserListItemHTML(userName) {
    return "<li class='list-group-item'>" + userName + "</li>";
}