# snapchat-groupme
A bot that posts each snap it receives to a GroupMe group.

Depends on [SnapchatBot](https://github.com/agermanidis/SnapchatBot). 

Usage: <code>python2 groupme.py -u snapchatusername -p snapchatpassword -b groupmebotid -t groupmeaccesstoken</code>

While running, snapchatusername will add everyone who adds it and delete everyone who deletes it, and whenever it receives an image snap from othersnapchatuser, it will upload it to GroupMe's image service and post it to the group with the text "snap from othersnapchatuser".
