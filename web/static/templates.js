
var templates_compiled = {}

var ERROR_TEMPLATE = 
       `
       <div id="main"class="inner cover">
              <h1 class="cover-heading">Something went wrong!</h1>
              <h2> {{errorMessage}}
       </div>
       `

var INVITE_JOIN_TEMPLATE = 
       `
       <div id="main"class="inner cover">
            <h1 class="cover-heading">Join Room {{roomID}}</h1>
            <form id="roomForm"  enctype="multipart/form-data" onsubmit="return false">
              <div class="small-container">
                <label for="hostID" class="sr-only">Username</label>
                <input type="text" id="userID" name="userID" class="form-control" placeholder="Username" required autofocus>
                <br>
              </div>
              <button class="btn btn-default" onclick="{{joinRoom}}">Join</button>
            </form>
       </div>
       `
var LOBBY_TEMPLATE =
       `
       <div id='main'> 
              <h4>Invite link: <a href='{{inviteLink}}'> {{inviteLink}} </a></h4>
              <div id='userList'>
                     {{#userList availableUsers}}{{userID}}{{/userList}}
              </div>
       </div>
       `;

var INITIAL_CREATE_TEMPLATE = 
       `
       <div id="main"class="inner cover">
            <h1 class="cover-heading">KPOP Spot It</h1>
            <form id="roomForm"  enctype="multipart/form-data" onsubmit="return false">
              <div class="small-container">
                <label for="hostID" class="sr-only">Username</label>
                <input type="text" id="userID" name="userID" class="form-control" placeholder="Username" required autofocus>
                <label for="roomID"  class="sr-only">RoomName</label>
                <input type="text" id="roomID" name="roomID" class="form-control" placeholder="Room Name" required>
                <br>
              </div>
              <button class="btn btn-default"  onclick="{{createRoom}}">Create Room</button>
              <button class="btn btn-default" onclick="{{joinRoom}}">Join Room</button>
            </form>
       </div>
       `

var template_html = {
       "LOBBY_TEMPLATE" : LOBBY_TEMPLATE,
       "INITIAL_CREATE_TEMPLATE" : INITIAL_CREATE_TEMPLATE,
       "ERROR_TEMPLATE" : ERROR_TEMPLATE,
       "INVITE_JOIN_TEMPLATE" : INVITE_JOIN_TEMPLATE
};

function initialize_templates() {
       
       for (var i = 0; i < Object.keys(template_html).length; i++) {
              var cur_key = Object.keys(template_html)[i];
              var cur_val = template_html[cur_key];
              templates_compiled[cur_key] = Handlebars.compile(cur_val);
       }
}

initialize_templates();
