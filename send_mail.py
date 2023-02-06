import smtplib, os  # smtplib: 메일 전송을 위한 패키지
from email import encoders  # 파일전송을 할 때 이미지나 문서 동영상 등의 파일을 문자열로 변환할 때 사용할 패키지
from email.mime.text import MIMEText   # 본문내용을 전송할 때 사용되는 모듈
from email.mime.multipart import MIMEMultipart   # 메시지를 보낼 때 메시지에 대한 모듈
from email.mime.base import MIMEBase    # 파일을 전송할 때 사용되는 모듈
import datetime
from crud import *
from db import session
from unicodedata import normalize
class mail():
    def __init__(self,email,password):
        self._db = next(session.get_db())
        self.email = email
        self.pw = password
        self.smtp = smtplib.SMTP('smtp.cafe24.com',587)   # 587: 서버의 포트번호
        self.smtp.ehlo()
        self.smtp.starttls()   # tls방식으로 접속, 그 포트번호가 587
        self.smtp.ehlo()
        
    def login_check(self):
        try:
            self.smtp.login(self.email,self.pw)
            return True
        except:
            return False
    def send_mail(self,folder_path,email,name):
        print(email)
        msg = MIMEMultipart()
        pdf_list = os.listdir(folder_path)
        for pdf in pdf_list:
            pdf = normalize('NFC',pdf)
            if pdf.split("_")[-1] == f"{name}.pdf":
                file_name = pdf
                file = os.path.join(folder_path,file_name)
                print(file)
        if os.path.isfile(file):
            print(os.path.isfile(file))
        else:
            return False
        text = MIMEText("안녕하세요 (주)서르입니다 \n 급여명세서 발송 메일입니다 \n 고생하셨습니다.")
        msg['From'] = self.email
        msg['to'] = email
        msg['Subject']= f"(주)서르_{file_name.split('월')[0].split('_')[-1]}월 급여명세서"
        msg.attach(text)
        msg.preamble="?"
        part = MIMEBase("application","octet-stream")
        part.set_payload(open(file,"rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment',filename=file_name)
        msg.attach(part)
        self.smtp.sendmail(self.email,email,msg.as_string())
        return True
        #self.smtp.quit()
    
    
    
        
# if __name__=="__main__":
#     mail = mail()
#     #mail.email_login()
#     mail.make_report()