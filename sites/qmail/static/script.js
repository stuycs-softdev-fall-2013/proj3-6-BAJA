var most_recent_email = ;
var uid;
var get_uid = function() {
    $.ajax({url:'uid',
            success: function(r) {
                uid = r['uid'];
            }
    });
}
var display_email = function(email) {
     var emails = document.getElementById('emails');
     var e_block = document.createElement('div');
     e_block.setAttribute('id',"email");
     var from = document.createElement('div');
     from.innerHTML = email['from'];
     e_block.appendChild(from);
     e_block.innerHTML = email['subject'];
     emails.appendChild(e_block);
}

//Assumes the ajax response is sorted by eid, going upward
var load_emails = function() {
    $.ajax({url:'get',
            success: function(r) {
                for(int i = 0; i < r['emails'].length; i++) {
                    if(most_recent_email < r['emails'][i]['eid']) {
                        display_email(r['emails'][i]);
                        most_recent_email = r['emails'][i]['eid'];
                    }
                }
            }
    })
    setTimeout(load_emails, 5000);
}

get_uid();
load_emails();
