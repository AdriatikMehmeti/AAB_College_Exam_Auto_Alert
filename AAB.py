import requests, tempfile

class text_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AAB:

    # Important Params
    _obj = None
    _access_token = None
    _token_type = None
    _date_format = "%d/%m/%Y %H:%M:%S"
    _filename = "AAB_EXAM_LOG.txt"
    _referer = 'https://eservice.aab-edu.net/'
    _url_api = 'https://testapieservice.uniaab.com:443/Token'
    _url_api_exam = 'https://testapieservice.uniaab.com:443/api/refusedexamstudent/list'
    _temp_path = tempfile.gettempdir()

    def __init__(self,username = None,password = None,charset = None):
        self.username = username
        self.password = password
        self.charset = charset

    # Parametrat per hyrje. Keto duhet te plotesohen!
    _config = {
        'username': "",
        'password': "",
        'charset': "UTF-8"
    }

    # ERROR RECORDS
    _error = {}

    # Controll duplicate
    def update_data(self,data,mode = None):

        if(mode == 'w'):
            file = open(f'{self._temp_path}/Config_{self._filename}', 'a+')
            file.write(f'{data}\n')
            file.close()
            return True

        # Compare, update difference and return difference
        diff = set(data).difference(set([line.rstrip('\n') for line in open(f'{self._temp_path}/Config_{self._filename}', 'r+')]))
        for i in diff: self.update_data(i,mode='w')
        return diff

    #write Log to file  - Default path file
    def write_log(self,Log):

        from datetime import datetime
        date = datetime.now()

        file = open(f'{self._temp_path}/{self._filename}','a+')
        file.write(f"{text_color.FAIL}[#] Timestamp: {date.strftime(self._date_format)} - {Log} {text_color.ENDC}\n")
        file.close()

    # ERROR RECORDS SET
    def set_ERROR(self,key,error):

        from datetime import datetime
        date = datetime.now()

        key = key if isinstance(key, str) else 'Error_key'
        error = error if isinstance(error, str) else 'Incorrect error reporting'

        self._error[key] = f"{error} - Time: {date.strftime(self._date_format)}"
        self.write_log(f'{key} - {error}')

    # Show Error if exist exit
    def Have_Errors(self,Stop = False, validate = False):

        if (validate == True and len(self._error) > 0):
            return False

        if (validate == False and len(self._error) > 0):
            print(f"{text_color.WARNING}[#] ----------- ERROR Found --------------------- [#]{text_color.ENDC}\n")
            for i in self._error:
                print(f"{text_color.FAIL}[!] Key: {i} - Message: {self._error.get(i)} {text_color.ENDC}\n")

            if(Stop): exit(0)  # In case we have an error it should be stopped

        return True

    # CHECK CONFIG
    def _config_check(self):

        # Nese nuk jan vendosur i merr nga imputi
        if(self._config.get('username').strip() == '' or self._config.get('password').strip() == ''):

            if (self.username == None or self.password == None):
                self.set_ERROR('Auth <Config>','Incomplete Authentication parameters!')

                print(f'{text_color.FAIL}Authentication Incomplete! Try again.{text_color.ENDC}')
                while (self.username == None):
                    answer = input(f'{text_color.WARNING}Type eservice username: {text_color.ENDC}')
                    self.username = answer if isinstance(answer, str) else None

                while (self.password == None):
                    answer = input(f'{text_color.WARNING}Type eservice password: {text_color.ENDC}')
                    self.password = answer if isinstance(answer, str) else None

                self.charset = "UTF-8"

            self._config['username'] = self.username
            self._config['password'] = self.password
            self._config['charset'] = self.charset

            #return True

        #return False


    def _aab_connect(self):

        # Kontrolli i parametrave te konfigurimit
        self._config_check()

        if (self._obj == None):

            headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"",
                       "Accept": "*/*",
                       "Content-Type": f"application/x-www-form-urlencoded; charset={self._config.get('charset')}",
                       "Sec-Ch-Ua-Mobile": "?0",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                       "Sec-Ch-Ua-Platform": "\"Linux\"",
                       "Origin": f"{self._referer[:-1]}",
                       "Sec-Fetch-Site": "cross-site",
                       "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                       "Referer": f"{self._referer}",
                       "Accept-Encoding": "gzip, deflate",
                       "Accept-Language": "en-US,en;q=0.9"}

            data = {"grant_type": "password",
                    "username": f"{self._config.get('username')}",
                    "password": f"{self._config.get('password')}"}

            self.obj = requests.post(self._url_api, headers=headers, data=data)

            if(self.obj.status_code == 200):

                print(f"{text_color.OKBLUE}[#] ----------- Eservice Notification ----------- [#]{text_color.ENDC}",
                      f"\n{text_color.OKBLUE}[+] AAB eservice Login Successfuly {text_color.ENDC}")
                self._access_token = self.obj.json()['access_token']
                self._token_type = self.obj.json()['token_type']

                return self._obj

            else:
                self.set_ERROR('Eservice Auth Error',f"{self.obj.json()['error_description']} Status code - {self.obj.status_code}")
                self._obj = False

        #self.Have_Errors(Stop=True);
        return False


    def _aab_exam_results(self):

        if(self._obj == False):
            return False

        headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"",
                   "Accept": "application/json, text/javascript, */*; q=0.01",
                   "Authorization": f"{self._token_type} {self._access_token}",
                   "Sec-Ch-Ua-Mobile": "?0",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                   "Sec-Ch-Ua-Platform": "\"Linux\"",
                   "Origin": f"{self._referer[:-1]}",
                   "Sec-Fetch-Site": "cross-site",
                   "Sec-Fetch-Mode": "cors",
                   "Sec-Fetch-Dest": "empty",
                   "Referer": f"{self._referer}",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "en-US,en;q=0.9"}

        response = requests.get(self._url_api_exam, headers=headers)

        if response.status_code == 200:
            print(f"{text_color.OKBLUE}[+] AAB eservice exams fetch Successfuly {text_color.ENDC}")

            return response.json()

        self.set_ERROR('Eservice Exams Error', f"{response.json()} Status code - {response.status_code}")

        return False
