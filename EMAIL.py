from AAB import AAB,text_color
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EMAIL:

    #info. Replace with your additional email
    target_email = ''

    def __init__(self,email = None, password = None, port = None):
        self.email = email
        self.password = password
        self.port = port
        self.session = None

    # Parametrat per hyrje. Keto duhet te plotesohen!
    _config = {
        'email': "",
        'password': "",
        'smtp': "smtp.gmail.com",
        'port': 587
    }

    # Check Config
    def check_config(self):

        if (self._config.get('email').strip() == "" or self._config.get('password').strip() == ""):
            if (self.email == None or self.password == None):
                self.email = None
                self.password = None

                print(f'{text_color.FAIL}Authentication Incomplete! Try again.{text_color.ENDC}')

                while (self.email == None):
                    answer = input(f'{text_color.WARNING}Type Email username: {text_color.ENDC}')
                    self.email = answer if isinstance(answer, str) else None

                while (self.password == None):
                    answer = input(f'{text_color.WARNING}Type Email password: {text_color.ENDC}')
                    self.password = answer if isinstance(answer, str) else None

            self._config['email'] = self.email
            self._config['password'] = self.password

            #return True

        self.target_email = self._config.get('email') if self.target_email.strip() == '' else self.target_email
        #return False


    def login_email(self):

        self.check_config()

        # Create SMTP session for sending the mail
        self.session = smtplib.SMTP(self._config.get('smtp'), self._config.get('port'))

        ssl_context = ssl.create_default_context()
        self.session.starttls(context=ssl_context)

        try:
            self.session.login(self._config.get('email'), self._config.get('password'))
            print(f"{text_color.OKBLUE}[#] ----------- Email Notification -------------- [#]{text_color.ENDC}",
                  f"\n{text_color.OKBLUE}[+] Email Login Successfuly {text_color.ENDC}")
        except:
            AAB().set_ERROR('Email Error', "Can't login, incorrect email or password")
            self.session = False

    def send_email(self,subject='ooo', message = 'Regards'):

        self.login_email();

        if(self.session == False):
            return

        mail_content = message

        message = MIMEMultipart()
        message['From'] = self._config.get('email')
        message['To'] = self.target_email
        message['Subject'] = subject

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        try:
            self.session.sendmail(self._config.get('email'), self.target_email, message.as_string())
            print(f"{text_color.OKBLUE}[+] Email Sent Successfuly {text_color.ENDC}")
        except:
            AAB().set_ERROR('Email Error', "Can't sent email, message content")

        self.session.quit()

        #AAB().Have_Errors(Stop=True)
