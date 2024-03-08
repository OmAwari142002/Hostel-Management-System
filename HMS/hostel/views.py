from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import StudentDetails,Attendance,Complaint
from django.contrib.auth.decorators import login_required
import random
import uuid
from datetime import date,time
from django.db import transaction
from datetime import datetime, timedelta
from django.contrib.auth import logout as django_logout
from django.views.decorators.cache import never_cache
from .models import Complaint  # Assuming your model is named 'Complaint'

# Create your views here.
def index(request):
    return render(request,'index.html')

def Login(request):
    if request.user.is_authenticated:
        if(request.user.is_superuser):
            return redirect('/admin-dashboard')
        elif(request.user.is_staff):
            return redirect('/rector-dashboard')
        else:
            return redirect('/student-dashboard')
    
    else:
        return render(request,'login.html')

def Signup(request):
    return render(request,'signup.html')
@login_required
def logout(request):
    django_logout(request)
    
    request.session.pop('user', None)
    response = render(request, 'login.html', {'message': 'Logged Out Successfully'})
    
    return response
@never_cache
def verify_login(request):
    global username
    username = ''
    
    first_name = ''  # Initialize with default values
    last_name = ''
    user = None
    if request.method == "POST":
        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # secret_key = '6Le0RJgoAAAAAGVPLP8z_zbyuQn-Kwyo4frr_t41'
        # data = {
        #     'secret': secret_key,
        #     'response': recaptcha_response
        # }
        # response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        # result = response.json()

        # if not result['success']:
        #     return render(request, 'login.html', {'message': 'Captcha Verification Failed'})


        username = request.POST.get('username')
        password = request.POST.get('password')
        identity = request.POST.get('identity')
      
        try:
            if identity == "student" : 
                print("INSIDE STUDENT")
                user = authenticate(request, username=username, password=password)
                print(user)
                if user is not None:
                    print("Inside if")
                    login(request, user)
                    first_name = user.first_name
                    last_name = user.last_name
                    request.session['user']={
                        'username':username,
                    }
                    return redirect('/student-dashboard')
                else:
                    return render(request, 'login.html', {'error': 'Invalid UserName or Password.',"first_name":first_name,"last_name":last_name})
            if identity == "admin" : 
                
                    user = authenticate(request, username=username, password=password)
                    if(user.is_staff):
                        if user is not None:
                            login(request, user)
                            first_name = user.first_name
                            request.session['user']={
                        'username':username,
                    }
                            return redirect('/admin-dashboard')
                    else:
                        return render(request, 'login.html', {'error': 'Wrong Admin Credentials.'})
                
            if identity == "rector" : 
                
               
                    user = authenticate(request, username=username, password=password)
                    if(user.is_superuser):
                        if user is not None:
                            login(request, user)
                            first_name = user.first_name
                            request.session['user']={
                        'username':username,
                    }
                            return redirect('/rector-dashboard')
                    else:
                        return render(request, 'login.html', {'error': 'Wrong SuperAdmin Credentials'})
            
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid UserName or Password.'})
    return render(request, 'login.html')
# @login_required
# def student_dashboard(request):
#     if not request.user.is_authenticated :
#         return render(request, 'login.html')
#     else:
#         username = request.session.get('user', {}).get('username', '')
#         print(request.session.get('user', {}))
    
#     # Get the student details
#         try:
#             student_details = StudentDetails.objects.get(email=username)
#         except StudentDetails.DoesNotExist:
#             return render(request, 'login.html', {'error': 'Student Details Not Found'})

#     # Get the user object
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return render(request, 'login.html', {'error': 'User not found'})

#     # Get the attendance records for the user
#         attendance = Attendance.objects.filter(user=user)
#         print(attendance)

#         if attendance:
#         # Fetching dates from each Attendance object
#             present_dates = [record.date for record in attendance if record.attendance in ['Present']]
#             print(present_dates)
#             leave_dates = [record.date for record in attendance if record.attendance in ['Leave']]
    



# # Exclude the dates already marked as "Present" or "Leave"
#         # Convert datetime.datetime objects to datetime.date objects
#             absent_dates = [record.date for record in attendance if record.attendance in ['Absent']]
           


#             print(absent_dates)
#             message = request.GET.get('message', None)
#             print(message)

#             return render(request, 'student_dashboard.html', {'student_details': student_details, 'attendance_dates': present_dates,'leave_dates': leave_dates,'absent_dates': absent_dates,"message":message})
    
#     return render(request, 'login.html', {'error': 'Attendance records not found'})

@login_required
def student_dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    username = request.session.get('user', {}).get('username', '')
    print(request.session.get('user', {}))

    # Get the student details
    try:
        student_details = StudentDetails.objects.get(email=username)
    except StudentDetails.DoesNotExist:
        return render(request, 'login.html', {'error': 'Student Details Not Found'})

    # Get the user object
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'login.html', {'error': 'User not found'})

    # Get the attendance records for the user
    attendance = Attendance.objects.filter(user=user)
    print(attendance)

    present_dates, leave_dates, absent_dates = [], [], []

    if attendance:
        # Fetching dates from each Attendance object
        present_dates = [record.date for record in attendance if record.attendance == 'Present']
        print(present_dates)
        leave_dates = [record.date for record in attendance if record.attendance == 'Leave']
        # Exclude the dates already marked as "Present" or "Leave"
        absent_dates = [record.date for record in attendance if record.attendance == 'Absent']

    message = request.GET.get('message', None)
    print(message)

    return render(request, 'student_dashboard.html', {
        'student_details': student_details,
        'attendance_dates': present_dates,
        'leave_dates': leave_dates,
        'absent_dates': absent_dates,
        'message': message
    })


@login_required
def complaints(request):
    if(request.user.is_authenticated):
        username = request.session.get('user', {}).get('username', '')
        user = User.objects.filter(username=username)
        student = User.objects.get(email=username)
        
        
        
        return render(request,'complaints.html',{'user':user,'student':student})   
    else:
        return render(request,'login.html')
from django.urls import reverse
@login_required
def complaints_submit(request):
    if request.method == 'POST':
        username = request.session.get('user', {}).get('username', '')
        user = User.objects.get(username=username)
        print(user)
        
        name = request.POST.get('fullName')
        print(name)
        roomNo = request.POST.get('roomNo')
        print(roomNo)
        issueType=request.POST.get('issueType')
        print(issueType)
        complaint = None
        UploadedImage =None
        if(issueType=='6'):
            complaint=request.POST.get('complaint')
            
            UploadedImage=request.POST.get('UploadedImage')
            print('UploadedImage',UploadedImage)
        if(issueType=='8'):
            complaint=request.POST.get('complaint')
      
            
        
        
        optionIssue=request.POST.get('selectedOption')
        new_complaint = Complaint.objects.create(
            user=user,
            name=name,
            roomNo=roomNo,
            complaint=complaint,
            uploaded_image=UploadedImage,
            issue_type=issueType,
            selected_option=optionIssue,
            forwared_to="Rector",
            status="Pending",
            
        )
        new_complaint.save()
        return redirect(reverse('student-dashboard') + '?message=Complaint%20Registered%20Successfully')
def mark_users_as_absent():
    now = datetime.now()
    current_time = now.time()

    if current_time >= time(23, 45):
        # Get all users
        all_users = User.objects.all()

        for user in all_users:
            # Check if the user has attendance records for today
            if not Attendance.objects.filter(user=user, date=now.date(),attendance="Present").exists():
                # Mark the user as absent
                attendance = Attendance(user=user, attendance='Absent')
                attendance.save()


    

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')
def rector_dashboard(request):
    return render(request,'rector_dashboard.html')
def verify_otp(request):

    if request.method == 'POST':
        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # secret_key = '6Le0RJgoAAAAAGVPLP8z_zbyuQn-Kwyo4frr_t41'
        # data = {
        #     'secret': secret_key,
        #     'response': recaptcha_response
        # }
        # response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        # result = response.json()

        # if not result['success']:
        #     return render(request, 'signup.html', {'error': 'Captcha Verification Failed'})
        college =request.POST.get('college')
        branch = request.POST.get('branch')
        year = request.POST.get('year')

        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        student_mobile = request.POST.get('student_mob')
        parent_mobile = request.POST.get('parent_mob')
        address = request.POST.get('address')
        parent_name = request.POST.get('parent_name')

        password = request.POST.get('password')
        confpassword = request.POST.get('confirm_password')
       
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email Already Taken'})
        if StudentDetails.objects.filter(student_mobile=student_mobile).exists():
            return render(request, 'signup.html', {'error': 'Mobile Number Already Taken'})
            

        if password == confpassword:
            otp = generate_otp()
            send_otp_email(email, otp)

        # Add OTP to session for verification
            request.session['otp'] = otp
            request.session['user_data'] = {
                'password': password,
                'confpassword': confpassword,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'gender': gender,
                'student_mobile': student_mobile,
                'parent_mobile': parent_mobile,
                'address': address,
                'parent_name': parent_name,
                'college': college,
                'branch': branch,
                'year': year

            }

            return render(request, 'verify_otp.html', {'email': email})

        else:
            return render(request,'signup.html',{'error':'Password and Confirm Password Fields Must Match'})
    return redirect('signup')
def verify(request):
    user_data = request.session.get('user_data', {})
    email = user_data.get('email', '')
    stored_otp = request.session.get('otp')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if stored_otp == entered_otp:
            password = user_data.get('password', '')
            firstname = user_data.get('firstname', '')
            lastname = user_data.get('lastname', '')
            email = user_data.get('email', '')
            gender = user_data.get('gender', '')
            student_mobile = user_data.get('student_mobile', '')
            parent_mobile = user_data.get('parent_mobile', '')
            address = user_data.get('address', '')
            parent_name = user_data.get('parent_name', '')
            college = user_data.get('college', '')
            branch = user_data.get('branch', '')
            year = user_data.get('year', '')

            try:
                with transaction.atomic():
                    # Generate UUID for the student
                    student_uuid = uuid.uuid4()

                    # Create User instance
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.is_active = False
                    user.save()

                    # Create StudentDetails instance with student UUID and linked User instance
                    student_details = StudentDetails.objects.create(
                        user=user,
                        uuid=student_uuid,
                        first_name=firstname,
                        last_name=lastname,
                        email=email,
                        branch=branch,
                        year=year,
                        college=college,
                        student_mobile=student_mobile,
                        parent_mobile=parent_mobile,
                        address=address,
                        gender=gender,
                        parent_name=parent_name
                    )
                    student_details.save()
            except Exception as e:
                # If an exception occurs, delete the created User instance
                user.delete()
                raise e

            # Clear the session data
            request.session.pop('user_data', None)
            request.session.pop('otp', None)

            return render(request, 'login.html', {'message': 'User Created Successfully'})

        else:
            return render(request, 'verify_otp.html', {'email': email, 'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html', {'email': email})
def generate_otp():
    return str(random.randint(100000, 999999))
def send_otp_email(email, otp):
    subject = 'KJEI Hostel Mangement System OTP Verification'
    message = f'Your OTP for account verification on KJEI Hostel Mangement System is: {otp}  Do not share it with anyone.'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
def mark_attendance(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        attendance = request.POST.get('attendance')
        
        user = User.objects.get(username=username)
        today = date.today()
        existing_attendance = Attendance.objects.filter(user=user,date=today).exists()
        print(existing_attendance)

        if existing_attendance:
           
            return JsonResponse({'error': 'Attendance already marked for today'}, status=400)
        attendance_obj = Attendance.objects.create(user=user, attendance=attendance)
        attendance_obj.save()
        return HttpResponse('Attendance Marked Successfully')
    return HttpResponse('Invalid Request')

from django.shortcuts import render
from .models import Complaint

def check_complaint_status(request):
    # Get complaints for the current user (adjust the condition based on your actual model)
    complaints = Complaint.objects.filter(user=request.user)

    # Map issue type IDs to names
    issue_type_mapping = {
        '1': 'Electrical',
        '2': 'Plumbing',
        '3': 'Internet',
        '4': 'Accommodation',
        '5': 'Cleaning Related',
        '6': 'Fees Related',
        '7': 'Common Area Issues',
        '8': 'Miscellaneous',
    }

    # Define the get_complaint_issue_type function
    def get_complaint_issue_type(value):
        return issue_type_mapping.get(value, value)

    return render(request, 'check_complaint_status.html', {'complaints': complaints, 'get_complaint_issue_type': get_complaint_issue_type})
