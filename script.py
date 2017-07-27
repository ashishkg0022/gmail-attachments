import email
import getpass
import imaplib, os , sys

curr_dir ='.'
user = input("Enter your GMail username:")
password =getpass.getpass("Enter your password: ")
search_email=input("Enter mail of which attachments has to be downloaded")

if search_email not in os.listdir(curr_dir):
    os.mkdir(search_email)

curr_dir = './'+search_email

m = imaplib.IMAP4_SSL("imap.gmail.com",port=993)
try :
    m.login(user,password)
except imaplib.IMAP4.error as e :
	print ("login failed !!" + str(e) )
	sys.exit(0)


m.select( mailbox='INBOX') 

resp, items = m.uid('search', None , 'FROM' , search_email) 
items = items[0].split() 

for emailid in items:
    resp, data = m.uid('fetch', emailid , "(RFC822)") 
    raw_email = data[0][1] 
    mail = email.message_from_bytes(raw_email) 
    #body = mail.get_body()
    #print ("["+mail["From"]+"] :" + mail["Subject"])

    if mail.get_content_maintype() != 'multipart':
        continue

    
 
    for part in mail.walk():
       
        if(part.get('Content-Disposition' ) is not None ) :
            filename = part.get_filename()

  

            final_path= os.path.join(curr_dir + filename)

            if not os.path.isfile(final_path) :
      
               fp = open(curr_dir+"/"+(filename), 'wb')
               fp.write(part.get_payload(decode=True))
               fp.close()

m.close()
m.logout()
