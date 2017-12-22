import sys
import imaplib
import getpass
import email
import email.header
import datetime
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from form import Ui_Dialog

reload(sys)
sys.setdefaultencoding('utf8')

curr_dir ='.'

EMAIL_ACCOUNT= None

EMAIL_FOLDER = "INBOX" # or "[Gmail]/All Mail" or "[Gmail]/Sent Mail"

mailinfo = []
 
class MyDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.ui.pushButton.clicked.connect(self.OK)
		self.ui.listWidget.itemClicked.connect(self.showmessage)

	def showmessage(self, item):
		msgnumber = str(item.text()).split()[1]
		msgindex = mailinfo.index(msgnumber)
		print mailinfo[msgindex + 1]
		print mailinfo[msgindex + 2]
		print mailinfo[msgindex + 3]
		print mailinfo[msgindex + 4]

		boxy = QMessageBox()
		boxy.setText('Title : %s\nFrom : %s' %((mailinfo[msgindex + 1]), (mailinfo[msgindex + 2])))
		boxy.setInformativeText('%s\n\n%s attachment(s) on this message' % ((mailinfo[msgindex + 3]), (mailinfo[msgindex + 4])))
		boxy.setWindowTitle('Message %s' % (mailinfo[msgindex]))

		boxy.setStandardButtons(QMessageBox.Ok)
		boxy.exec_()


	def OK(self):
		EMAIL_ACCOUNT = self.ui.lineEdit.text()

		print 'OK pressed.'
		self.auth(EMAIL_ACCOUNT)

	def auth(self, EMAIL_ACCOUNT):
		M = imaplib.IMAP4_SSL('imap.gmail.com')
		try:
			rv, data = M.login(EMAIL_ACCOUNT, self.ui.lineEdit_2.text())
		except imaplib.IMAP4.error:
			choice=QtGui.QMessageBox.question(self, 'Error', "LOGIN FAILED!!!", QtGui.QMessageBox.Retry, QtGui.QMessageBox.Exit)
			if choice=QtGui.QMessageBox.Exit:
				#print "LOGIN FAILED!!! "
				sys.exit(1)
			elif choice=QtGui.QMessageBox.Retry:
				auth(self, EMAIL_ACCOUNT)

		print data
		search_email = self.ui.lineEdit_3.text()

		curr_dir = '.'

		if search_email not in os.listdir(curr_dir):
			os.mkdir(search_email)

		curr_dir = './'+search_email

		rv, mailboxes = M.list()
		if rv == 'OK':
			print "Mailboxes located."

		rv, data = M.select(EMAIL_FOLDER)

		if rv == 'OK':
			print "Now processing mailbox ...\n"
			self.process_mailbox(M, search_email, curr_dir)
			M.close()
		else:
			print "ERROR: Unable to open mailbox ", rv

		M.logout()

	def process_mailbox(self, M, search_email, curr_dir):

		rv, data = M.search(None, '(OR (TO %s) (FROM %s))' % (search_email, search_email))
		if rv != 'OK':
			print "No messages found!"
			return

		for num in data[0].split():
			rv, data = M.fetch(num, '(RFC822)')
			if rv != 'OK':
				print "ERROR getting message", num
				return

			localinfo = []

			print '-----'
			msg = email.message_from_string(data[0][1])
			decode = email.header.decode_header(msg['Subject'])[0]
			subject = unicode(decode[0])
			print 'Message %s : %s' % (num, subject)
			self.ui.listWidget.addItem(QListWidgetItem('Message %s : %s' % (num, subject)))
			localinfo.append(num)
			localinfo.append(subject)

			sender = msg['from'].split()[-1]
			sender = sender[1:]
			sender = sender[:-1]

			print 'Sender : ', sender
			localinfo.append(sender)
			#print 'Raw Date:', msg['Date']

			for part in msg.walk():
				if part.get_content_type() == 'text/plain':
					print part.get_payload()
					localinfo.append(part.get_payload())
			
			# Kepping up to local time
			date_tuple = email.utils.parsedate_tz(msg['Date'])
			if date_tuple:
				local_date = datetime.datetime.fromtimestamp(
					email.utils.mktime_tz(date_tuple))
				print "Dated : ", \
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

			localinfo.append(fcount)

			global mailinfo
			mailinfo.append(localinfo)

			print '%d attachment(s) fetched' %fcount
			print '-----\n\n'

		mailinfo = [item for sublist in mailinfo for item in sublist]
		print mailinfo
 
if __name__ == "__main__":
		app = QtGui.QApplication(sys.argv)
		myapp = MyDialog()
		myapp.show()
		sys.exit(app.exec_())

