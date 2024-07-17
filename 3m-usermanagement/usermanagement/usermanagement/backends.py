from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from users.models import *

class EmailAuthBackend():
    def authenticate(self, request, username, password):
        
        try:
            # to verify if entered username is mobile number or email if mobile no. then if condition will be executed
            if username.isnumeric():
                # check if entered mobile number is registered or not
                try:
                    customuser = CustomUser.objects.get(mobile=username)
                    user = User.objects.get(username=customuser)
                except:
                    messages.error(request, ('Incorrect Mobile Number, please try again!'))
                    return None
            else:
                # check if entered email is registered or not
                
                user = User.objects.get(email=username)
                if username != user.email:
                    messages.error(request, ('Incorrect Email Address, please try again!'))
                    return None
              
            # if email or mobile no. is registered then verify the password is correct or not
            success = user.check_password(password)
    
            # if password is correct then returned user to adminLogin function in views.py
            if success:
                return user
            else:
                messages.error(request, ('Incorrect Password, please try again!'))	
                return None
            
        except User.DoesNotExist:
            messages.error(request, ('Incorrect Email Address, please try again!'))
        return None

    def get_user(self,uid):
        print(uid)
        try:
            return User.objects.get(pk=uid)
        except:
            return None
        
