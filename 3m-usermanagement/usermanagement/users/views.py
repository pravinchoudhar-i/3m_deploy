from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.contrib.auth.models import User
from django.views import View
from django.core.mail import  EmailMessage, send_mail
from .models import *
from .utilities import * 
from .validate import *
# Move backends.py to main folder

from usermanagement.backends import EmailAuthBackend
from .serializers import *
import random
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.http import HttpResponse
from django.http import FileResponse



# Create your views here.

# admin login form
# Convert to login class
class AdminLogin(View):
    def get(self,request,*args, **kwargs):
        return render(request,'admin-login.html')

    def post(self,request,*args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        # print(settings.AUTHENTICATION_BACKENDS)
        # verify if user exist or not
        user = authenticate(request, username=email, password=password)   
        # print(user.email)
        if user is not None:
            login(request,user)
            return redirect('view-admins')
        else:	
            return redirect('admin-login')


@method_decorator(login_required, name='dispatch')
class ViewUsers(View):
    # Retrieve
    def get(self,request,*args, **kwargs):

        action = request.GET.get('action',None)
        instance_id = request.GET.get('id',None)
        search = request.GET.get('search',None)
        entries = request.GET.get('entries', '25')
        #to create new user
        if action == 'create':
            return render(request, 'user-register-form.html')
        # to update the data of existing user
        elif action == 'edit':
            if instance_id:
                registeredUser = UserRegistration.objects.filter(status=1).get(id=instance_id)
                # TODO: Please add comment for this logic
                # Changes in HTML value for mobile number field(remove +91)
                # phone = (str(registeredUser.mobile)[3:])
                phone = registeredUser.mobile
                context = {
                    "registeredUser":registeredUser,
                    "phone":phone
                }
                return render(request,'user-edit-form.html',context)
        # to delete the user
        elif action == 'delete':
            if instance_id:
                return self.delete(request)
        # search the user by email in user table
        # TODO: Add pagination in search
        elif action == 'search':
            try:
                registeredUser = UserRegistration.objects.filter(email__icontains=search,status=1).order_by('-id').all()
                paginator = Paginator(registeredUser, int(entries)) 
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                
                # Why do we require additional & in the end?
                # additional & for providing page number (eg. page=1)
                pagination_url = "users/?entries=" + entries + "&search=" + search + "&action=" + action + "&"
                context = {
                    "entries" : entries,
                    "page_obj" : page_obj,
                    "pagination_url" : pagination_url
                    
                }
                return render(request,'tables/user_table.html',context)
            except Exception as ex:
                page_obj = []
                context = {
                    'page_obj':page_obj
                }
                return render(request,'tables/user_table.html',context)
        # to view all the user 
        # to view user table
        else:    
            registeredUser = UserRegistration.objects.filter(status=1).order_by('-id').all()
            count = registeredUser.count()

            paginator = Paginator(registeredUser, int(entries)) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            # additional & for providing page number (eg. page=1)
            if action:
                pagination_url = "users/?entries=" + entries + "&action=" + action + "&"
            else:
                pagination_url = "users/?entries=" + entries + "&"
                
            context = {
                'entries' : entries,
                'count' : count,
                'page_obj' : page_obj,
                'pagination_url' : pagination_url

                    }
            return render(request,'tables/user_table.html', context)

    # Create
    def post(self,request,*args, **kwargs):
        if '_put' in request.POST:
            print(self.put(request))
            print("True")
            return self.put(request)

        userId = request.user.id  
        user = User.objects.get(id=userId)

        filled_data = dict(request.POST)
        filled_data.pop('csrfmiddlewaretoken')
        firstName = request.POST.get('fname')
        lastName = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        organisation = request.POST.get('organisation')
        location = request.POST.get('location')
        dial_code = request.POST.get('dial-code',"91")

        try:
            if mobile.find('-') == -1:
                mobile = "+"+dial_code+mobile.replace(" ","")
            else:
                mobile = "+"+dial_code+mobile.replace("-","")
        
            registerUser = UserRegistration.objects.create(
                firstName=firstName, lastName=lastName, email=email, mobile=mobile,
                organisation=organisation, location=location, createdAt=datetime.now(),
                createdBy=user
            )
            
        except:            
            messages.error(request, ('Mobile Number already taken, please try again with new one!'))       
            # Can we use the request.POST dictionary instead of filled data?
            context = {
                "registeredUser":filled_data
                }    
            return render(request, 'user-register-form.html',context)
        
        if registerUser:
            # save user created activity in LogEntries Table
            userCreated = 'User Created - ' + str(registerUser.email)
            masterLog(request,registerUser, ADDITION,userCreated) 
            messages.success(request, ('User successfully created!'))
            return redirect('view-users')
        else:
            messages.error(request, ('User not created, please try again!'))
            return redirect('view-users')

        # TODO: Put a condition for else

    # Update
    def put(self,request,*args,**kwargs):

        userId = request.user.id  
        user = User.objects.get(id=userId)

        firstName = request.POST.get('fname',None)
        lastName = request.POST.get('lname',None)
        email = request.POST.get('email',None)
        mobile = request.POST.get('mobile',None)
        organisation = request.POST.get('organisation',None)
        location = request.POST.get('location',None)
        id = request.POST.get('id',None)
        dial_code = request.POST.get('dial-code',"91")

        try:
            if mobile.find('-') == -1:
                mobile = "+"+dial_code+mobile.replace(" ","")
            else:
                mobile = "+"+dial_code+mobile.replace("-","")

            registerUser = UserRegistration.objects.filter(id=id).update(firstName=firstName,lastName=lastName, email=email, mobile=mobile, organisation=organisation, location=location, updatedAt=datetime.now(), updatedBy=user)  
        except Exception as ex:
            messages.error(request, (ex))     
            # Can we access request.POST disctionery here?
            edit_data = {
                "id":id, "firstName":firstName, "lastName":lastName, "email":email, "mobile":mobile,
                "organisation":organisation, "location":location
            }
            context = {
                "registeredUser":edit_data
            }
            return render(request,'user-edit-form.html',context)

        if registerUser:
            # save user updated activity in LogEntries Table
            mobileUser = UserRegistration.objects.get(id=id)
            userUpdated = 'User Updated - ' + str(mobileUser.email)
            masterLog(request,mobileUser,CHANGE,userUpdated) 
            messages.success(request, ('successfully updated!'))
            return redirect('view-users')
        else:
            messages.error(request, ('Not Updated, please try again!')) 
            return redirect('view-users')     
        
      
    # Delete
    def delete(self,request,*args,**kwargs):

        id = request.GET.get('id',None)
        registerUser = UserRegistration.objects.filter(id=id).update(status=0)
        
        if registerUser:
            # save user deleted activity in LogEntries Table
            mobileUser = UserRegistration.objects.get(id=id)
            userDeleted = 'User Deleted - ' + str(mobileUser.email)
            masterLog(request,mobileUser,CHANGE,userDeleted) 
            return JsonResponse({"status":"Deleted"})
        else:
            messages.error(request, ('Not Deleted, please try again!'))
            return JsonResponse({"status":"Not Deleted"})

@method_decorator(login_required, name='dispatch')
class ViewAdmin(View):
    # Retrieve
    def get(self,request,*args, **kwargs):

        action = request.GET.get('action',None)
        search = request.GET.get('search',None)
        entries = request.GET.get('entries', '25')
        
        if action == 'create':
            return render(request, 'admin-register-form.html')
        elif action == 'search':
            try:
                registeredUser = CustomUser.objects.filter(user__email__icontains=search, status=1).order_by('-id').all() 
                paginator = Paginator(registeredUser, int(entries))
                
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                # additional & for providing page number (eg. page=1)
                pagination_url = "view-admin/?entries=" + entries + "&search=" + search + "&action=" + action + "&"
                context = {
                    'entries' : entries,
                    'page_obj' : page_obj,
                    'pagination_url' : pagination_url
                }
                return render(request,'tables/admin_table.html',context)
            except Exception as ex:
                page_obj=[]
                context = {
                    'page_obj':page_obj
                }
                return render(request,'tables/admin_table.html',context)
        else:    
            registeredUser = CustomUser.objects.filter(status=1).order_by('-id').all()
            count = registeredUser.count()
            print(entries)
            print("__________________________")
            paginator = Paginator(registeredUser, int(entries))
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            # additional & for providing page number (eg. page=1)
            if action:
                pagination_url = "view-admin/?entries=" + entries + "&action=" + action + "&" 
            else:
                pagination_url = "view-admin/?entries=" + entries + "&"

            context = {
                'entries' : entries,
                'count' : count,
                'page_obj' : page_obj,
                'pagination_url' : pagination_url
            }

            return render(request,'tables/admin_table.html', context)

    # Create
    # Link to implement password validation: https://stackoverflow.com/questions/54547575/how-to-use-django-password-validation-in-my-existing-views
    def post(self,request,*args, **kwargs):
        validators = [MinimumLengthValidator, NumericPasswordValidator,UserAttributeSimilarityValidator]

        userId = request.user.id  
        userObj = User.objects.get(id=userId)

        filled_data = dict(request.POST)
        filled_data.pop('csrfmiddlewaretoken')
        email = request.POST.get('email')
        fName = request.POST.get('fname')
        lName = request.POST.get('lname')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        dial_code = request.POST.get('dial-code',"91")

        if mobile.find('-') == -1:
            mobile = "+"+dial_code+mobile.replace(" ","")
        else:
            mobile = "+"+dial_code+mobile.replace("-","")

        if password != password2:            
            context = {
                "registeredUser":filled_data
            }
            messages.error(request, ('Password and Confirm Password does not match'))
            return render(request, 'admin-register-form.html',context)
        else:         
            try:
                for validator in validators:
                    if validator == UserAttributeSimilarityValidator:
                        user_attributes_array = (email, fName, lName, email)
                        er = validator().validate(password, user_attributes_array)
                    else:
                        er = validator().validate(password)                         
                
            except ValidationError as e:             
                messages.error(request, str(e))
                context = {
                "registeredUser":filled_data
                    }
                return render(request, 'admin-register-form.html',context)
                
            hashed_pwd = make_password(password)
          
            mobileUser = CustomUser.objects.filter(mobile=mobile).exists()
        
            if mobileUser:
                messages.error(request, ('Admin with this mobile already exist, please try again with new one!'))
                context = {
                "registeredUser":filled_data
                    }
                return render(request, 'admin-register-form.html',context)
            else:

                try:
                    user = User.objects.create(username=email, email=email, first_name=fName,last_name=lName, password=hashed_pwd)

                    registerUser = CustomUser.objects.create(user_id=user.id, mobile=mobile, createdAt=datetime.now(), createdBy=userObj)
                except:
                    messages.error(request, ('Admin with this email address already exist, please try again with new one!'))
                    context = {
                    "registeredUser":filled_data
                        }
                    return render(request, 'admin-register-form.html',context)

                if user and registerUser:
                    # save admin created activity in LogEntries Table
                    userCreated = 'Admin Created - ' + str(user.email)
                    masterLog(request,registerUser, ADDITION,userCreated) 
                    messages.success(request, ('Successfully created'))
                    return redirect('view-admins') 
                            
                else:
                    messages.error(request, ('Admin not created, please try again!'))
                    return redirect('view-admins') 
                

@method_decorator(login_required, name='dispatch')
class FeedbackTable(View):
    # Retrieve
    def get(self,request,*args, **kwargs):
        
        action = request.GET.get('action',None)
        search = request.GET.get('search',None)
        entries = request.GET.get('entries', '25')
        print(entries)
       
        # TODO: Mention date time format for searching
        if action == 'search':
            try:
                feedbacks = Analysis.objects.filter(Q(feedback__icontains=search, status=1)|Q(time__icontains=search, status=1)|Q(predictionType__icontains=search, status=1)).order_by('-id').all()
                paginator = Paginator(feedbacks, int(entries))
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                # additional & for providing page number (eg. page=1)
                pagination_url = "feedback/?entries=" + entries + "&search=" + search + "&action=" + action + "&"
                context = {
                    'entries' : entries,
                    'page_obj':page_obj,
                    'pagination_url' : pagination_url
                }
                return render(request,'tables/feedback_table.html',context)
            except Exception as ex:
                page_obj=[]
                context = {
                    'page_obj':page_obj
                }
                return render(request,'tables/feedback_table.html',context)
        else:    
            feedbacks = Analysis.objects.filter(status=1).order_by('-id').all()
            count = feedbacks.count()

            paginator = Paginator(feedbacks, int(entries))
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            # additional & for providing page number (eg. page=1)
            if action:
                pagination_url = "feedback/?entries=" + entries + "&action=" + action + "&"
            else:
                pagination_url = "feedback/?entries=" + entries + "&"

            context = {
                'entries' : entries,
                'count' : count,
                'page_obj' : page_obj,
                'pagination_url' : pagination_url
            }

            return render(request,'tables/feedback_table.html', context)

# API view to get or post the data in Analysis model 
class FeedbackAPIView(APIView):
    def get(self, request, format=None):
        analysis = Analysis.objects.filter(status=1).all()
        serializer = AnalysisSerializer(analysis, many=True)
        return Response(serializer.data)  
    
    
    def post(self, request, format=None):
        image = request.FILES.get('image')
        feedback = request.POST.get('feedback')
        predictionType = request.POST.get('predictionType')
        predictionColor = request.POST.get('predictionColor')
        feedbackType = request.POST.get('feedbackType')
        feedbackColor = request.POST.get('feedbackColor')
        isFlash = request.POST.get('isFlash')
        createdBy = request.POST.get('createdBy')
        createdAt = request.POST.get('createdAt')
        location = request.POST.get('location')

        # TODO: Add user in analysis table    
        with image.open('rb') as img:
            data = {
                'feedback':feedback, 
                'image':img, 
                'predictionType':predictionType,
                'predictionColor':predictionColor,
                'feedbackType':feedbackType,
                'feedbackColor':feedbackColor,
                'isFlash':isFlash,
                'createdBy': int(createdBy),
                'createdAt':createdAt,
                'location':location
            }
            print(data)
            serializer = AnalysisSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                # save feedback submitted activity in MasterLog Table
                description = 'Feedback form submitted - ' + str(serializer.data['feedback'])
                master_log = MasterLog.objects.create(timeStamp=datetime.now(),
                    activity = "ADDITION", description = description, mobileUser_id = createdBy
                    )
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API view for Analysis model
class FeedbackAPIViewDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Analysis.objects.filter(status=1).get(pk=pk)
        except Analysis.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AnalysisSerializer(snippet)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        analysis_data = Analysis.objects.get(id=pk)
        createdBy_id = analysis_data.createdBy.id
        createdAt = analysis_data.createdAt
        
        image = request.FILES.get('image')
        feedback = request.POST.get('feedback')
        predictionType = request.POST.get('predictionType')
        predictionColor = request.POST.get('predictionColor')
        feedbackType = request.POST.get('feedbackType')
        feedbackColor = request.POST.get('feedbackColor')
        isFlash = request.POST.get('isFlash')
        updatedBy = request.POST.get('updatedBy')
        updatedAt = datetime.now()

        # TODO: Add user in analysis table    
        with image.open('rb') as img:
            data = {
                'feedback':feedback, 
                'image':img, 
                'predictionType':predictionType,
                'predictionColor':predictionColor,
                'feedbackType':feedbackType,
                'feedbackColor':feedbackColor,
                'createdBy':createdBy_id,
                'createdAt':createdAt,
                'updatedBy': int(updatedBy),
                'updatedAt':updatedAt,
                'isFlash':isFlash
            }
            serializer = AnalysisSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            
                # save feedback updated activity in MasterLog Table
                description = 'Feedback form updated - ' + str(serializer.data['feedback'])
                master_log = MasterLog.objects.create(timeStamp=datetime.now(),
                        activity = "CHANGE", description = description, mobileUser_id = updatedBy
                        )

                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        analysis = self.get_object(pk)
        analysis.status = False
        analysis.save()
        
        serializer = AnalysisDeleteSerializer(analysis, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # save feedback deleted activity in MasterLog Table
            description = 'Feedback form deleted'
            master_log = MasterLog.objects.create(timeStamp=datetime.now(),
                    activity = "CHANGE", description = description, mobileUser_id = analysis.user.id
                    )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import requests
from decouple import config
def sendSMS(mobile,otp):
    message = f"Congrats!{mobile},Your provisional timing at JBG Durgapur\
                10k for bib no.{otp} in RACE is 10 minutes. Team ALABSO"

    url = f"http://smsjust.com/sms/user/urlsms.php?response=Y&username={config('SMS_USERNAME')}&pass={config('SMS_PASSWORD')}&senderid={config('SMS_SENDERID')}&message={message}&dest_mobileno={mobile}&msgtype=TXT"
    print(url)
    x = requests.get(url)

    print(x.text)
    return x.text


# send Email
def sendEmail(subject,message,receipent):
    print(message)
    print(receipent)
    print("Entered mail")
    status = send_mail(
        subject,
        message,
        config("EMAIL_HOST_USER"),
        receipent
        )
    # msg.attach(files.name, files.read(), content_type)
    
    print(status)

# API to send otp
class SendOtpAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def post(self, request, format=None):
        data = request.body
        data_dict = json.loads(data.decode("utf-8"))
        mobile = data_dict['mobile']
        
        registeredAdmin = UserRegistration.objects.filter(mobile=mobile).exists()
        # Add masterlog when OTP is generated
        if registeredAdmin:
            user = UserRegistration.objects.get(mobile=mobile)
            generate_otp = random.randint(1000,9999)
            expiry = 5
            subject = "OTP for app login"
            message = f"{generate_otp} is your one time password to login to 3M sheet identification app. It is valid for {expiry} minute. Do not share your OTP with anyone."
            # sms_status = sendSMS(mobile,generate_otp)
            
            
            sendEmail(subject,message,[user.email])
            sms_status = "Sent"

            data = {
                "mobile": mobile,
                "user_id":user.id,
                "otp":generate_otp,
                "status":sms_status
            }

            sms = SMSModule.objects.get(id=1)
            sms.messageSent = sms.messageSent + 1
            sms.updatedAt = datetime.now()
            sms.save()

            # save otp sending activity in MasterLog Table
            description = f"OTP sent to mobile number {mobile}"
            master_log = MasterLog.objects.create(timeStamp=datetime.now(),
                    activity = "OTP SENT", description = description, mobileUser_id = user.id
                    )
            return Response(data,status=status.HTTP_200_OK)
            
            # return Response("OTP send successfully",status=status.HTTP_200_OK)
        else:
            return Response("Incorrect Mobile Number",status=status.HTTP_404_NOT_FOUND)




# API to send bulk data8
class BulkFeedbackAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def post(self, request, format=None):
    
        feedbacks  = request.data.getlist('feedback')
        predictions  = request.data.getlist('prediction')
        images  = request.data.getlist('image')
        user = request.POST.get('user_id')
        dataList = []
        for i in range(len(feedbacks)):
            with images[i].open('rb') as img:
                data = {
                    'feedback' : feedbacks[i],
                    'image' : img,
                    'prediction' : predictions[i],
                    'user':user
                }
                serializer = AnalysisSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                    # save feedback submitted activity in MasterLog Table
                    description = 'Feedback form submitted - ' + str(serializer.data['feedback'])
                    master_log = MasterLog.objects.create(timeStamp=datetime.now(),
                    activity = "ADDITION", description = description, mobileUser_id = user
                    )
                    dataList.append(serializer.data)
                                        
        return Response(dataList,status=status.HTTP_201_CREATED)
    #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
def masterLog(request,object,action, data):
   
    LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(object).pk,
                object_id=object.id,
                object_repr=str(data),
                action_flag=action)

    return True


class VersionLogAPIView(APIView):
    def get(self, request, format=None):
        analysis = VersionLog.objects.filter(status=1).last()
        serializer = VersionSerializer(analysis)
        return Response(serializer.data)  
   

# API to log feedbacks 
class FeedbackEntriesAPIView(View):

    def get(self,request,*args, **kwargs):
        duration = request.GET.get('duration',None)
        start_date = request.GET.get('start_date',None)
        end_date = request.GET.get('end_date',None)
        current_date = timezone.now() 
       
        if duration == 'last week':
            required_date = current_date - timedelta(days=7)
            print(required_date)
            start_date = str(required_date.date())
            end_date = str(current_date.date())
            
            events = Analysis.objects.filter(createdAt__date__range=(start_date,end_date)).all().count()
            
        elif duration == 'last month':
            required_date = current_date - timedelta(days=30)
            print(required_date)
            start_date = str(required_date.date())
            end_date = str(current_date.date())
            
            events = Analysis.objects.filter(createdAt__date__range=(start_date,end_date)).all().count()
           
        elif duration == 'last 6 month':
            required_date = current_date - timedelta(days=182)
            print(required_date)
            start_date = str(required_date.date())
            end_date = str(current_date.date())
            
            events = Analysis.objects.filter(createdAt__date__range=(start_date,end_date)).all().count()
            
        elif duration == 'last year':  
    
            required_date = current_date - timedelta(days=365)
            print(required_date)
            start_date = str(required_date.date())
            end_date = str(current_date.date())
            
            events = Analysis.objects.filter(createdAt__date__range=(start_date,end_date)).all().count()
            
        elif duration == 'custom':
            events = Analysis.objects.filter(createdAt__date__range=(start_date,end_date)).all().count()

        else:
            events = 0

        return JsonResponse({"Total Feedback" : events})


class FetchData(GenericAPIView):

    def get(self, request, *args, **kwargs):
        get_val = request.query_params

        types_of_operation = get_val.get('types_of_operation')

        if "model_name" not in get_val or get_val.get('model_name') == "":
            return JsonResponse({"message": "Please provide model_name"})
        else:
            model_name = get_val.get('model_name')

        if "list_of_fields" not in get_val:
            list_of_fields = ""
        else: 
            list_value = get_val.get('list_of_fields')

        if "filter_value" not in get_val:
            filter_value = ""
        else:
            filter_value = get_val.get('filter_value')

        if "types_of_operation" not in get_val:
            types_of_operation = ""
        else:
            types_of_operation = get_val.get('types_of_operation')

        response = HelpFetchData(model_name, list_value, filter_value, types_of_operation)

        return JsonResponse(response,safe=False)
    
    
    
    

