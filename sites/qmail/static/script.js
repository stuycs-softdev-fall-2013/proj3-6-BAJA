var most_recent_email = -1;

var display_email = function(email) {
     var emails = document.getElementById('email-list');
     var e_block = document.createElement('li');
     e_block.setAttribute('id',"email-" + email["id"]);
     e_block.innerHTML += email["sender"][1] + " : " + email["subject"];
     emails.appendChild(e_block);
}

//Assumes the ajax response is sorted by eid, going upward

var load_emails = function() {
    $.ajax('/inbox.json').done(function(r) {
        for (var i = 0; i < r.length; i++) {
            if(most_recent_email < r[i]['id']) {
                display_email(r[i]);
                most_recent_email = r[i]['id'];
            }
        }
        setTimeout(load_emails, 5000);
    })
}

var send_email = function() {
    $.ajax('/send.json', {data: $('#send-form').serialize()});
}

load_emails();

document.getElementById("send_email").onclick = send_email;
