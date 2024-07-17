from .models import *

def reportsManagement(request):
	print("Entered REport context")
	if request.user.is_authenticated:
		print("Entered Report context But should not")
		
		reports = ReportManagement.objects.filter(user=request.user).all()
		print(reports)
		
		if reports:
			return {"reports":reports}
		else:
			return {"reports":[]}

	else:
		return {"reports":[]}