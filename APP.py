# Start
from AAB import AAB,text_color
import EMAIL
from datetime import datetime


def main():
    aab = AAB()
    aab._config_check()
    aab._aab_connect()

    exams = aab._aab_exam_results()
    if exams and len(exams) > 0:

        message = ''
        data = []

        for i in exams: data.append(i.get('lenda'))

        for i in AAB().update_data(data): message += f"Lenda: {i} \n"

        EMAIL.EMAIL().send_email(f'Exam Results Updated{datetime.now().strftime(AAB()._date_format)}', message)
        print(f"\n{text_color.OKBLUE}[+] AAB eservice new exam results found {text_color.ENDC}")
        aab.Have_Errors()
    elif(exams == False):

        EMAIL.EMAIL().send_email(f'Eservice Auth Error {datetime.now().strftime(AAB()._date_format)}')
        print(f"\n{text_color.FAIL}[!] AAB eservice Auth Error {text_color.ENDC}")
        aab.Have_Errors()
    else:
        EMAIL.EMAIL().send_email(f'Not found new results {datetime.now().strftime(AAB()._date_format)}')
        print(f"\n{text_color.OKGREEN}[-] AAB eservice no change was found {text_color.ENDC}")
        aab.Have_Errors()

if __name__ == "__main__":
    main()