from .models import *


def privileges(request):
	# print("In privileges function")
	# print(request.user)
	# print(request.user.is_authenticated)
	# print(request.user.is_superuser)
	
	# if request.user.is_authenticated and not request.user.is_superuser:
	# 	user_details = UserDetails.objects.get(user_id=request.user.id)
	# 	# user_details = CustomUser.objects.get(user_id=request.user.id)
	# 	# print(user_details)
	# 	# role = Roles.objects.filter(id=user_details.role.id).first()
	# 	# privileges = role.privileges.values_list('name',flat=True)
	# 	# print(request.session['role'])
	# 	# print(privileges)
	# 	privileges = []
	# 	roles = []
	# 	for role in user_details.role.all():
	# 		roles.append(role.name)
	# 		for privilege in role.privileges.all():
	# 			privileges.append(privilege.name)
	# else:
	# 	privileges = []
	# 	roles = []
	# print("privileges",privileges)
	# return {'privileges':privileges,'roles':roles} 
	return {'privileges':privileges,'roles':""} 


