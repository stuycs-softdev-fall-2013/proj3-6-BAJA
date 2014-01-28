var most_recent_email = -1;
var email_data = {};
var selected = 0;

var display_email = function(email) {
    email_data[email["id"]] = email;
    var emails = document.getElementById('email-list');
    var e_block = document.createElement('li');
    e_block.setAttribute('id', "email-" + email["id"]);
    var d = new Date(0);
    d.setUTCSeconds(email["time"]);
    var etime = moment(d).fromNow();
    e_block.innerHTML += '<a onclick="show_email(' + email["id"] + ')"><b>' + email["sender"][1] + (new Array(9).join("&nbsp;")) + "</b>" + email["subject"] + (new Array(9).join("&nbsp;")) + "<i>" + etime + "</i></a>";
    emails.insertBefore(e_block, document.getElementById("email-label").nextSibling);
}

var show_email = function(email_id) {
    var email = email_data[email_id];
    if (!selected)
        $("#email-data").show();
    selected = email_id;
    $("#email-sender-address").text(email["sender"][0]);
    $("#email-sender-address").click(function() { $("#to").val(email["sender"][0]) });
    $("#email-sender-name").text(email["sender"][1]);
    var addrs = email["to"];
    var elem = $("#email-to");
    elem.html("");
    for (var i = 0; i < addrs.length; i++) {
        n = Math.floor(Math.random() * 100000)
        elem.html(elem.html() + addrs[i][1] + " (<a href='#' id='email-send-to-" + n + "'>" + addrs[i][0] + "</a>)");
        $("#email-send-to-" + n).click(function(res) { return function() { $("#to").val(res) } }(addrs[i][0]) );
    }
    addrs = email["cc"];
    elem = $("#email-cc");
    elem.html("");
    if (addrs.length == 0)
        $("#cc-row").hide();
    else
        $("#cc-row").show();
    for (var i = 0; i < addrs.length; i++) {
        n = Math.floor(Math.random() * 100000)
        elem.html(elem.html() + addrs[i][1] + " (<a href='#' id='email-send-to-" + n + "'>" + addrs[i][0] + "</a>)");
        $("#email-send-to-" + n).click(function(res) { return function() { $("#to").val(res) } }(addrs[i][0]) );
    }
    addrs = email["bcc"];
    elem = $("#email-bcc");
    elem.html("");
    if (addrs.length == 0)
        $("#bcc-row").hide();
    else
        $("#bcc-row").show();
    for (var i = 0; i < addrs.length; i++) {
        n = Math.floor(Math.random() * 100000)
        elem.html(elem.html() + addrs[i][1] + " (<a href='#' id='email-send-to-" + n + "'>" + addrs[i][0] + "</a>)");
        $("#email-send-to-" + n).click(function(res) { return function() { $("#to").val(res) } }(addrs[i][0]) );
    }
    var d = new Date(0);
    d.setUTCSeconds(email["time"]);
    var etime = moment(d).format('MMMM Do YYYY, h:mm:ss a');
    $("#email-time").text(etime);
    $("#email-subject").text(email["subject"]);
    $("#email-body").html("<p>" + email["body"].split("\n").join("</p><p>") + "</p>");
    if (email["subject"].indexOf("Re: ") == 0)
        $("#subject").val(email["subject"]);
    else
        $("#subject").val("Re: " + email["subject"]);
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
        if (!selected && r.length > 0)
            show_email(r[r.length - 1]['id']);
        setTimeout(load_emails, 5000);
    })
}

var send_email = function() {
    $.post('/send.json', $('#send-form').serialize());
}

$("#email-data").hide();
load_emails();

document.getElementById("send_email").onclick = send_email;
