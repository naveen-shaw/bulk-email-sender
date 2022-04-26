import csv
import os
from smtplib import SMTP
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def get_msg(csv_file_path, template):
    with open(csv_file_path, 'r') as file:
        headers = file.readline().split(',')
        headers[len(headers) - 1] = headers[len(headers) - 1][:-1]
    # i am opening the csv file two times above and below INTENTIONALLY, changing will cause error
    with open(csv_file_path, 'r') as file:
        data = csv.DictReader(file)
        for row in data:
            required_string = template
            for header in headers:
                value = row[header]
                required_string = required_string.replace(f'${header}', value)
            yield row['EMAIL'], required_string


def confirm_attachments():
    file_contents = []
    file_names = []
    try:
        for filename in os.listdir('ATTACH'):

            #entry = input(f"""TYPE IN 'Y' AND PRESS ENTER IF YOU CONFIRM T0 ATTACH {filename} 
             #                       TO SKIP PRESS ENTER: """)
            entry='Y'
            confirmed = True if entry == 'Y' else False
            if confirmed:
                file_names.append(filename)
                with open(f'{os.getcwd()}/ATTACH/{filename}', "rb") as f:
                    content = f.read()
                file_contents.append(content)

        return {'names': file_names, 'contents': file_contents}
    except FileNotFoundError:
        print('No ATTACH directory found...')

#manual
sub='test subject'

#manual
def test_send_emails(server: SMTP, template, l, lr, counter,l_len, lr_len, sent_count):

    attachments = confirm_attachments()
    
    
    multipart_msg = MIMEMultipart("alternative")

    #multipart_msg["Subject"] = message.splitlines()[0]
    #added manually
    multipart_msg["Subject"] = sub
    #multipart_msg["From"] = DISPLAY_NAME + f' <{SENDER_EMAIL}>'
    #added manually
    #multipart_msg["From"] = l[counter % l_len][2] + f' <{SENDER_EMAIL}>'
    #added manually
    multipart_msg["From"] = l[counter % l_len][2] + f' <{l[counter % l_len][0]}>'
    #multipart_msg["To"] = receiver
    multipart_msg["To"] =  lr[counter][0]
    print('Receiver abc@123 : ', lr[counter][0])

    text = template
    print('text = ',text)
    html = markdown.markdown(text)
    print('html = ',html)
    part1 = MIMEText(text, "plain")
    print('part1 = ',part1)
    part2 = MIMEText(html, "html")
    print('part2 = ',part2)
    multipart_msg.attach(part1)
    multipart_msg.attach(part2)
    print('multipart_msg = ',multipart_msg)
    print('multipart_msg.as_string = ',multipart_msg.as_string())

    if attachments:
        for content, name in zip(attachments['contents'], attachments['names']):
            attach_part = MIMEBase('application', 'octet-stream')
            attach_part.set_payload(content)
            encoders.encode_base64(attach_part)
            attach_part.add_header('Content-Disposition',
                                   f"attachment; filename={name}")
            multipart_msg.attach(attach_part)

    try:
        #server.sendmail(SENDER_EMAIL, receiver,
                        #multipart_msg.as_string())
        server.sendmail(l[counter % l_len][0], lr[counter][0],
                        multipart_msg.as_string())
    
    except Exception as err:
        print(f'Problem occurend while sending to {receiver} ')
        print(err)
        input("PRESS ENTER TO CONTINUE")
    else:
        sent_count += 1


    
#l=[['fake@gmail.com','password','disp_name']]
l=[]
with open('fetch_data.csv') as f:
    r=f.readlines()
    data=r[1:]
    #print(data)
    sender_list=[]
    for l in data:
        l=l.split(',')
        temp=[]
        temp.append(l[0])
        temp.append(l[1])
        temp.append(l[2])
        #print('temp ',temp)
        sender_list.append(temp)
    l=sender_list

print('l : ',l)
l_len=len(l)
lr=[]
with open('data.csv') as rf:
    rr=rf.readlines()
    rdata=rr[1:]
    print(rdata)
    rcvr_list=[]
    for lr in rdata:
        lr=lr.split(',')
        rtemp=[]
        rtemp.append(lr[0])
        #temp.append(l[1])
        #temp.append(l[2])
        #print('temp ',temp)
        rcvr_list.append(rtemp)
    lr=rcvr_list

print('lr : ',lr)
lr_len=len(lr)
counter=0
sent_count=0
for i in range(lr_len):
    if __name__ == "__main__":
        host = "smtp.gmail.com"
        port = 587  # TLS replaced SSL in 1999

        with open('compose.md') as f:
            template = f.read()

        server = SMTP(host=host, port=port)
        server.connect(host=host, port=port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        print(i+1)
        #server.login(user=SENDER_EMAIL, password=PASSWORD)
        #Atlernate manually

        server.login(user=l[i%l_len][0], password=l[i%l_len][1])  

        senr_count=test_send_emails(server, template, l , lr, counter, l_len, lr_len,sent_count)
        counter+=1
        sent_count=i+1
        server.quit()


print('Total Emails Sent = ',sent_count)
