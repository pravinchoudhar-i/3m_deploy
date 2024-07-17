from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,JsonResponse,FileResponse
from django.views import View
from .models import *
from datetime import datetime, timedelta,timezone
from django.contrib import messages
from django.db import connection
from openpyxl import Workbook
import json

from users.utilities import *
from decouple import config

# Create your views here.

class ReportQuery(View):
	def get(self,request,*args,**kwargs):
		
		report_id = int(self.kwargs.get('id'))
		custom_user = CustomUser.objects.filter(status=1).all()
		user_registration = UserRegistration.objects.filter(status=1).all()
		analysis = Analysis.objects.filter(status=1).all()
		master_log = MasterLog.objects.filter(status=1).all()
		sms_module = SMSModule.objects.filter(status=1).all()
		version_log = VersionLog.objects.filter(status=1).all()

		try:
			report_details = ReportManagement.objects.get(id=int(report_id))
		except:
			return HttpResponse("Please contact admin")


		primary_filters = report_details.filters_list.all()
		print("primary_filters", primary_filters)
		
		secondary_filters = {
			"custom_user":["Custom User",custom_user], "user_registration":["User Registration",user_registration], 
			"analysis":["Analysis",analysis], "master_log":["Master Log",master_log],
			"sms_module":["Sms Module",sms_module], "version_log":["Version Log",version_log]
			} 
		
		context = { "is_table":False, "report_details": report_details,
	      			"primary_filters":primary_filters, "secondary_filters":secondary_filters,
					"active_item_id":report_id}

		return render(request, 'reports_preview.html',context)		


	def post(self, request, *args, **kwargs):
		print(self.kwargs.get('id'))
		report_id = int(self.kwargs.get('id'))

		data = request.POST
		
		print(data)
		duration = data.get('duration')
		action = data.get('action')
		export = data.get('export')
		
		today = date.today()
		
		if duration == 'week':
			start_date, end_date = get_last_week_dates()
		elif duration == 'month':
			last_month, last_year = get_last_month_and_year()
			start_date, end_date = get_days_in_month(last_month, last_year)

		elif duration == 'quarter':
			last_month, last_year = get_last_month_and_year()
			start_date_last_month, end_date_last_month = get_days_in_month(last_month, last_year)

			days = get_last_four_months_days(3)

			# start_date_last_quarter = start_date_last_month - timedelta(days=days)
			start_date_last_quarter = end_date_last_month - timedelta(days=days)

			start_date = start_date_last_quarter
			end_date = end_date_last_month

		elif duration == 'half_yearly':
			last_month, last_year = get_last_month_and_year()
			start_date_last_month, end_date_last_month = get_days_in_month(last_month, last_year)

			days = get_last_four_months_days(6)

			start_date_last_quarter = start_date_last_month - timedelta(days=days)

			start_date = start_date_last_quarter
			end_date = end_date_last_month

		elif duration == 'yearly':
			today = date.today()
			last_year = today.year - 1

			start_date = date(last_year, 1, 1)
			end_date = date(last_year, 12, 31)
			
		elif duration == 'custom':
			start_date_raw = data.get('start_date')
			end_date_raw = data.get('end_date')
			format = "%Y-%m-%d"

			start_date = datetime.strptime(start_date_raw, format)
			end_date = datetime.strptime(end_date_raw, format)


		try:	
			report_data = ReportManagement.objects.get(id=report_id)
		
		except:
			return HttpResponse("Please contact admin")	
		
		query = report_data.query
		query = str(query)

		filters_list = report_data.filters_list.all()

		where_clause = ""
		filter_data = data.getlist('primary_filters')

		for filters in filters_list:
			if filters.db_name in filter_data:
				where_clause = where_clause + f"{filters.query_string}"			
				
				for filter_data in filter_data:
					filter_values_list = data.getlist(f'secondary_filters_{filters.db_name}')
					if filters.is_id == 0:
						filter_values_string = ', '.join(['"'+ item.split('_')[1] +'"' for item in filter_values_list])
					elif filters.is_id == 1:
						filter_values_string = ', '.join(['"'+ item.split('_')[0] +'"' for item in filter_values_list])

				if where_clause:
					where_clause = where_clause + " and "
					where_clause = where_clause.replace(filters.replacable_variable, f"({filter_values_string})")			 
				else:
					where_clause = where_clause.replace(filters.replacable_variable, f"({filter_values_string})")			 

		if duration == 'all':
			duration = f"LIKE ('%')"
			message = f"Displaying data for all records"

		else:
			query_start_date = start_date.strftime("%Y-%m-%d")
			query_end_date = end_date.strftime("%Y-%m-%d")
			duration = f"BETWEEN '{query_start_date}' AND '{query_end_date}'"	
			message = f"Displaying data from {query_start_date} to {query_end_date}"

		query = query.replace("$DURATION",duration)
		if where_clause:
			query = query.replace("$WHERECLAUSE",where_clause)
		else:
			query = query.replace("$WHERECLAUSE","")

		print("QUERY :- ",query)
		with connection.cursor() as cursor:
			cursor.execute(query)
			print("cursor.description: ",cursor.description)
			print("Component after query")
			try:
				data = cursor.fetchall()         
				header = [desc[0] for desc in cursor.description]
			except Exception as ex:
				messages.error(request, (f'Incorrect Query {ex}'))
				return redirect('report-data-table', id=report_id)
		# try:
		# 	mycursor = connection.cursor()
		# 	mycursor.execute(query) 
		# 	data = mycursor.fetchall()         
		# 	header = mycursor.description
		# except Exception as ex:
		# 	messages.error(request, (f'Incorrect Query {ex}'))
		# 	return redirect('report-data-table', id=report_id)
		# finally:
		# 	mycursor.close()

		table_headers = [field_name for field_name in header[int(report_data.columns_to_skip):]]
		print("table_headers",table_headers)
		table_data = []
		# table_data.append(table_headers)

		for x in data:
			fields = list(x[int(report_data.columns_to_skip):])

			table_data.append(fields) 

		jsonStr = json.dumps(table_data,default=json_serial)
		
		if action == "export" and export == 'csv':
			
			final_data = [table_headers] + table_data

			path = generate_and_save_json(final_data, request.user.username)	
			
			file = open(path, "r")
			
			# Sending request to elorca reports -----------------------------------------------
			import requests

			url = "https://reports.elorca.com/"

			payload={
				"token": "b2f11f01d535ea901a4e41da544f827460ce0dd3"
				}
			files=[
			('json',('report_json.json',open(path,'rb'),'application/json'))
			]
			headers = {
			'Content-Type': 'application/json',
			'Content-Type': 'application/octet-stream'
			}

			response_report = requests.request("POST", url, data=payload, files=files)


			file_url = response_report.text

			# Make the HTTP request to fetch the file
			response = requests.get(file_url)

			# Check if the request was successful
			if response.status_code == 200:
				# Create a FileResponse instance with the fetched file
				file_response = FileResponse(response)
				print(file_response)
				# Set the content type (optional)
				file_response["Content-Type"] = "application/octet-stream"

				# Set the file name for download (optional)
				file_response["Content-Disposition"] = "attachment; filename=report.csv"

				return file_response
			else:
				# Return an appropriate error response if the request fails
				return HttpResponse("Failed to fetch the file.", status=response.status_code)

			# --------------------------------------------------------------------------------

		elif action == "export" and export == 'xlsx':
			workbook = Workbook()

			# Get the active worksheet
			worksheet = workbook.active

			# Example data list
			data_list = final_data = [table_headers] + table_data
			print(data_list)
			# Write data to the worksheet
			for row in data_list:
				worksheet.append(row)

			# Create a response object with the appropriate content type
			response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

			# Set the file name for download
			response['Content-Disposition'] = 'attachment; filename=report.xlsx'

			# Save the workbook to the response
			workbook.save(response)

			return response
		
		context = {
			"table_data":table_data,
			"new_data":jsonStr,
			"table_headers":table_headers,
			"is_table":True,
			"message": message,

		}      
		cursor.close()    

		return render(request, 'reports_preview.html',context)
