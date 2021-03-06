proj3-6-BAJA
============

Background
----------

You are a programmer. This morning you signed up for an email account and soon
after received a job offer; you're excited to get started. But be careful,
because you're about to get sucked into a deadly world of trickery and
espionage.

Plot
----

* You recieve a simple job offer that you quickly complete.
* You do a couple of follow up jobs.
* You discover that you hav hacked the government! You want out.
* They blackmail you; you have no choice. You have to keep working for them.
* Eventually you hack them, and escape the world of danger.

So every mission you have will fit into the plot above, but will also be a
coding and hacking puzzle. This is a game of danger, deceit, and learning.

Puzzle Ideas
------------

1. Someone emails you saying that he's friends with Mike Zamansky; Z referred
   you to him as a capable programmer, and he wants to hire you for a job. You
   are to hack into his son's school's grade server so he can pass a failing
   class needed to graduate. The login password is hidden in the HTML source
   (it's pretty easy). You update the grade, email him back, the server checks
   the update happened, and then replies with thanks and a new offer.

2. "I think my wife is cheating on me. Can you crack her email and get me some
   information?" You hack into her email, which is another account on the same
   email server, and find emails from a suspicious individual that are
   encrypted with a relatively simple cypher. You reply with the encrypted
   code - he thanks you, but gives you no further job offers.

3. You are stumped, so you try to decrypt the code yourself. It's a simple
   substitution cypher. It turns out that his "wife" is actually a government
   agent and you have stumbled on potentially illegal information. You reply
   saying that you have discovered the true meaning of the code and that you
   are confused/upset he gave you a malicious task. He replies saying that you
   passed the "test", which was to see if you could decrypt the code on your
   own - and now that you have hacked into a government agent's email, he
   blackmails you into completing further missions for him (lest you be
   reported to the authorities for hacking).

4. He needs some money to buy new hardware, so he asks you to hack into an
   online banking site and transfer $5,000 to him (he gives you the bank
   routing number and his account but not enough to log in). He doesn't have
   another account to steal the money from, so you are responsible for finding
   one yourself. When browsing the site, you find a news story similar to the
   urban legend (http://www.snopes.com/katrina/photos/debitcard.asp) which
   gives you an account number to steal from. You log in and transfer the funds
   over. Your agent warns you that the FBI might be tracing suspicious
   transfers, and you should delete the transaction logs. He gives you the
   email account of a random employee (jsmith@randombank.com) and tells you
   about XSS and how you can do this to get into his account, find the email of
   someone who can audit transaction history, and then repeat it to get his
   bank login info. You log in to the auditor's dashboard, delete the
   transaction logs, and complete the mission.

Other Elements
--------------

It is possible to lose the game. "Overhacking" -- doing things you are not
supposed to -- or failing to cover your tracks in later missions, will lead to
the FBI following your trail and arresting you. When you lose the game all
pages on the server while you are logged in will redirect to a page that gives
you a game over message (with an explanation of what happened, and your
progress) and an option to log out. You cannot "save" or "revert" your progress
at any point to avoid this; you must start over. The same "game over" message
is displayed upon winning the game, but it is more congratulatory than "lol you
failed".

Running
-------

You will need Flask, Gunicorn, PyYAML, and
[Faker](https://github.com/joke2k/faker) (`fake-factory` in pip). Start the
project with `python main.py` and then navigate to http://localhost:6680.
