from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import StudentDetails,Attendance,Complaint,Rooms
from django.contrib.auth.decorators import login_required
import random
import uuid
from datetime import date,time
from django.db import transaction
from datetime import datetime, timedelta
from django.contrib.auth import logout as django_logout
from django.views.decorators.cache import never_cache
from .models import Complaint  # Assuming your model is named 'Complaint'
from django.utils.cache import add_never_cache_headers
# Create your views here.
def index(request):
    return render(request,'index.html')

def Login(request):
    if request.user.is_authenticated:
        if(request.user.is_superuser):
            return redirect('/rector-dashboard')
        elif(request.user.is_staff):
            return redirect('/admin-dashboard')
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
    add_never_cache_headers(response)
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


    
@login_required
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')
@login_required 
def rector_dashboard(request):
    student_count=0
    print(request.user)
    if not request.user.is_authenticated :
        return render(request, 'login.html')
    else:
        username = request.session.get('user', {}).get('username', '')
        print(request.session.get('user', {}))
        try:
            student_count = StudentDetails.objects.count()
        except StudentDetails.DoesNotExist:
            return render(request, 'login.html', {'error': 'Student Details Not Found'})

        
    return render(request,'rector_dashboard.html',{'student_count':student_count})
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def get_student_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not authenticated"}, status=404)
    else:
        pending_students = User.objects.filter(is_active=False)
        # Serialize queryset to a list of dictionaries
        serialized_students = list(pending_students.values())
        return JsonResponse({"pending_students": serialized_students}, status=200)
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
@login_required
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
def studentInfo(request,id):
    student_info = StudentDetails.objects.filter(user=id)
    user_info = User.objects.filter(id = id)
    serialized_student_info = list(student_info.values())
    serialized_user_info =list(user_info.values())
    return JsonResponse({'studentInfo':serialized_student_info,'user_info':serialized_user_info},status=200)
def autoAllocate(request, id):
    # Fetch student information
    student_info = StudentDetails.objects.filter(user=id).first()
    if not student_info:
        return JsonResponse({'error': 'Student not found'}, status=404)
    
    # Fetch user information
    user_info = User.objects.filter(id=id).first()
    if not user_info:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Determine the gender of the student
    gender = student_info.gender

    # Determine the floor range based on gender
    if gender == 'female':
        floor_range = range(3)  # Floors 0, 1, and 2 for females
    else:
        floor_range = range(3, 9)  # Floors 3 to 8 for males

    # Iterate over the floor range to find a suitable room
    for floor_number in floor_range:
        # Query rooms on the current floor with the same branch, year, and department
        rooms_on_floor = Rooms.objects.filter(
            floorNo=floor_number,
            Availability=True,
            NoOfOccupents__lt=3, 
        )
        # Iterate over rooms to find an available room
        for room in rooms_on_floor:
            occupants_uuids = room.occupants_uuid
            occupants_details = StudentDetails.objects.filter(uuid__in=occupants_uuids)
            branch_match = all([occupant.branch == student_info.branch for occupant in occupants_details])
            department_match = all([occupant.department == student_info.department for occupant in occupants_details])
            if branch_match and department_match:
                # Room found, allocate the room
                return JsonResponse({
                    'status': 'Room allocated successfully',
                    'room_no': room.roomNo,
                    'floor': floor_number,
                }, status=200)
    vacant_rooms = Rooms.objects.filter(Availability=True, NoOfOccupents=0)
    if vacant_rooms.exists():
        # Allocate the first vacant room found
        vacant_room = vacant_rooms.first()
        vacant_room.NoOfOccupents = 1
        vacant_room.save()
        return JsonResponse({
            'status': 'Room allocated successfully',
            'room_no': vacant_room.roomNo,
            'floor': vacant_room.floorNo,
        }, status=200)

    # No suitable room found, return an error response
    return JsonResponse({'error': 'No suitable room available'}, status=404)

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

@login_required
def pending_approval(request):
    try:
        pending_students = User.objects.filter(is_active=False)
        print(pending_students)
        return render(request,"pending-approval.html",{"pending_students":pending_students})
    except:
        return render(request,"pending-approval.html",{"pending_students":None})
        
        
def populate_rooms(request):
    for floor in range(10):  # Floors 0 to 9
        if floor == 0:
            for room_number in range(1, 41):  # Room numbers 1 to 40 for floor 0
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==1:
            for room_number in range(101, 141):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==2:
            for room_number in range(201, 241):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==3:
            for room_number in range(301, 341):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==4:
            for room_number in range(401, 441):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==5:
            for room_number in range(501, 541):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==6:
            for room_number in range(601, 641):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==7:
            for room_number in range(701, 741):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==8:
            for room_number in range(801, 841):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
        elif floor ==9:
            for room_number in range(901, 941):  # Room numbers 101 to 140 for other floors
                room = Rooms.objects.create(roomNo=room_number, floorNo=floor)
                room.save()
    
    return render(request,"login.html")

# Call the function to populate the rooms when needed

def notices_page(request):
    # Add any necessary context data
    return render(request, 'notices.html')


def student_profile_page(request):
    # Retrieve the currently logged-in user's student details
    student = request.user.student_details

    return render(request, 'student_profile.html', {'student': student})

def attendance_records(request):
    # Add any necessary context data
    return render(request, 'attendance_records.html')

def pending_fees(request):
    # Add any necessary context data
    return render(request, 'pending_fees.html')

def complaints(request):
    # Add any necessary context data
    return render(request, 'complaints.html')

