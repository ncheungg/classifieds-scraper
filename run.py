from kijiji import initiate


# this script searches the first 5 pages of Kijiji, and compares it to existing listings previously seen by this script
# run.py is made to run on a server that automatically updates every 5 minutes
# use Send_email.py to send emails of the new listings of your desired time interval

# initiate("search item", "pages to scan", "floor price", "ceiling price")
initiate("apple pencil", 5, 0, 100)
initiate("ipad 6th generation", 5, 0, 100)
