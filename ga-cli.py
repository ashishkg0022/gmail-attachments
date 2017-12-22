import sys
import imaplib
import getpass
import email
import email.header
import datetime
import os

reload(sys)
sys.setdefaultencoding('utf8')

curr_dir ='.'

EMAIL_ACCOUNT= raw_input("Enter your email: ")
#EMAIL_ACCOUNT = "spotifyrounak@gmail.com"
EMAIL_FOLDER = "INBOX" # or "[Gmail]/All Mail" or "[Gmail]/Sent Mail"

#search_email = "rounakdatta12@gmail.com"

def process_mailbox(M):

    rv, data = M.search(None, '(OR (TO %s) (FROM %s))' % (search_email, search_email))
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        print '-----'
        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print 'Message %s: %s' % (num, subject)

        sender = msg['from'].split()[-1]
        sender = sender[1:]
        sender = sender[:-1]

        print 'Sender: ', sender
        #print 'Raw Date:', msg['Date']

        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                print part.get_payload() 
        
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Dated: ", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")

        fcount = 0
        for part in msg.walk():
       
            if(part.get('Content-Disposition' ) is not None ) :
                filename = part.get_filename()
                print filename

      

                final_path= os.path.join(curr_dir + filename)

                if not os.path.isfile(final_path) :
          
                   fp = open(curr_dir+"/"+(filename), 'wb')
                   fp.write(part.get_payload(decode=True))
                   fcount += 1
                   fp.close()

        print '%d attachment(s) fetched' %fcount
        print '-----\n\n'


M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(1)

print data
search_email = raw_input("Enter search email: ")
if search_email not in os.listdir(curr_dir):
    os.mkdir(search_email)

curr_dir = './'+search_email

rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes located."
    #print mailboxes

rv, data = M.select(EMAIL_FOLDER)

if rv == 'OK':
    print "Now processing mailbox ...\n"
    process_mailbox(M)
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv

M.logout()