from django.shortcuts import render,redirect
from .models import Member
from .serializers import MemberSerializer
from rest_framework import viewsets
from django.http import HttpResponse
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (permissions.AllowAny,)



def index(request):  
    
    title = "會員管理"

    #todo 讀取會員資料傳給index.html
    members = Member.objects.all()
    # print(list(member))

    return render(request,'member/index.html',locals())

def create(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        useremail = request.POST["useremail"]
        userbirth = request.POST["userbirth"]

        EMAIL_USE_TLS = True 
        EMAIL_HOST = "smtp.gmail.com"
        EMAIL_PORT = 587
        EMAIL_HOST_USER = "a11118825@gmail.com"
        EMAIL_HOST_PASSWORD = "a63475566"
        from_email = EMAIL_HOST_USER
        to_list = useremail

        # email_conn即為SMTP物件，建立SMTP連線
        email_conn=smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
        email_conn.ehlo()
        #TTLS安全認證機制，必須使用TTLS protocol來進行連結傳輸,故叫喚starttls這個函式
        email_conn.starttls()
        email_conn.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        email_conn.sendmail(from_email, to_list, "Hi Welcome, now you are one of us!")
        email_conn.quit()

        #todo 接收到的會員資料寫進資料庫
        Member.objects.create(username=username,password=password,useremail=useremail,userbirth=userbirth)
        
        #todo 新增完成後轉到http://localhost:8000/member
        return redirect("/member")
       
    title = "會員新增" 
    return render(request,'member/create.html',locals())

def update(request,id):
    if request.method == 'POST':        
        username = request.POST["username"]      
        useremail = request.POST["useremail"]
        userbirth = request.POST["userbirth"]
        password=request.POST["password"]

        #todo 修改資料庫中的會員資料
        member = Member.objects.get(id=int(id))
        member.username = username
        member.useremail  = useremail
        member.userbirth = userbirth
        member.password = password
        member.save()
        
        #todo 修改完成後轉到http://localhost:8000/member
        return redirect('/member')

    title = "會員修改"

    #todo 根據會員編號取得會員資料傳給update.html
    member = Member.objects.get(id=int(id))
    return render(request,'member/update.html',locals())

def delete(request,id):
    #todo 根據會員編號刪除會員資料
    member = Member.objects.get(id=int(id))
    member.delete()

    #todo 刪除完成後轉到http://localhost:8000/member
    return redirect('/member')

def login(request):
    if request.method == "POST":
        useremail = request.POST['useremail']
        pwd = request.POST['userpassword']
        member = Member.objects.filter(useremail=useremail,password=pwd).values('username')
        if member:
            response = HttpResponse("<script>alert('登入成功');location.href='/'</script>")
            if 'rememberme' in request.POST:
                expiresdate = datetime.datetime.now() + datetime.timedelta(days=7)
                response.set_cookie("name",member[0]['username'],expires=expiresdate)
            else:
                response.set_cookie("name",member[0]['username'])
        else:
            response = HttpResponse("<script>alert('密碼錯誤');location.href='/member/login'</script>")
        return response
    title = "會員登入"
    return render(request,'member/login.html',locals())
def logout(request):
   response = HttpResponse("<script>alert('登出成功');location.href='/member/login'</script>")
   response.delete_cookie('name')
   return response

def forget(request):
    if request.method == 'POST':      
        useremail=request.POST['useremail']
        member = Member.objects.get(useremail=str(useremail))
        link = str('http://127.0.0.1:8000/member/update/%s'%(member.id))

        EMAIL_USE_TLS = True 
        EMAIL_HOST = "smtp.gmail.com"
        EMAIL_PORT = 587
        EMAIL_HOST_USER = "a11118825@gmail.com"
        EMAIL_HOST_PASSWORD = "a63475566"
        msg=MIMEMultipart('alternative') 
        msg['Subject'] = "Link"  
        msg['From'] = EMAIL_HOST_USER 
        msg['To'] = useremail  
        html="""/ 
            <html> 
            <head></head> 
            <body> 
                <p>Hi!<br> 
                Here is the  <a href="""+ link +""">link</a>  
                </p> 
            </body> 
            </html> 
            """   
        part2 = MIMEText(html, 'html')  
        msg.attach(part2)  
        from_email = EMAIL_HOST_USER
        # email_conn即為SMTP物件，建立SMTP連線
        email_conn=smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
        email_conn.ehlo()
        #TTLS安全認證機制，必須使用TTLS protocol來進行連結傳輸,故叫喚starttls這個函式
        email_conn.starttls()
        email_conn.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        email_conn.sendmail(from_email, useremail, msg.as_string())
        email_conn.quit()
        return render(request,'member/index.html',locals())
    
    else:
        return render(request,'member/forget.html',locals())
