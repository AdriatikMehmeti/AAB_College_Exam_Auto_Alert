# Start
from AAB import AAB,text_color
import EMAIL
from datetime import datetime


def main():
    aab = AAB()
    aab._aab_connect()
    exams = aab._aab_exam_results()

    data = []

    if exams and len(exams) > 0:
        for i in exams: data.append(f"Landa: {i.get('subjectName')} - Nota: {i.get('grade')} - Data: {i.get('data')}")
        data = aab.update_data(data)

    if data and len(data) > 0:

        message = ''

        for i in data: message += f"{i}\n"

        EMAIL.EMAIL().send_email(f'Exam Results Updated{datetime.now().strftime(aab._date_format)}', message)
        print(f"\n{text_color.OKBLUE}[+] AAB eservice new exam results found {text_color.ENDC}")
        
    elif(exams == False):

        EMAIL.EMAIL().send_email(f'Eservice Auth Error {datetime.now().strftime(aab._date_format)}')
        print(f"\n{text_color.FAIL}[!] AAB eservice Auth Error {text_color.ENDC}")
        
    else:
        EMAIL.EMAIL().send_email(f'Not found new results {datetime.now().strftime(aab._date_format)}')
        print(f"\n{text_color.OKGREEN}[-] AAB eservice no change was found {text_color.ENDC}")

    aab.Have_Errors()

if __name__ == "__main__":
    main()
