import json
from django.apps import apps

def HelpFetchData(model_name, list_value, filter_value, types_of_operation):

    model = apps.get_model('users', model_name)

    if types_of_operation == "count":
        print("---------")
        if filter_value == "" and list_value == "":
            data = model.objects.all().count()
            data_list = {"model_name":model_name,"count": data}
            return data_list

        elif filter_value != "" and list_value != "":
            filter_data = json.loads(filter_value) #converting str to dict
            list_of_fields = list_value.split(',') 
            data = model.objects.filter(**filter_data).values(*list_of_fields).count()
            data_list = {"model_name":model_name,"count": data}
            return data_list

        elif filter_value == "" or list_value != "":
            list_of_fields = list_value.split(',') #spliting list values using ","
            data = model.objects.all().values(*list_of_fields).count()
            data_list = {"model_name":model_name,"count": data}
            return data_list

        elif filter_value != "" or list_value == "":
            filter_data = json.loads(filter_value) #converting str to dict
            data = model.objects.filter(**filter_data).all().count()
            data_list = {"model_name":model_name,"count": data}
            return data_list
    else:
        if filter_value == "" and list_value == "":
            data = model.objects.all().values()
            data_list = list(data)
            return data_list

        elif filter_value != "" and list_value != "":
            filter_data = json.loads(filter_value) #converting str to dict
            list_of_fields = list_value.split(',') 
            data = model.objects.filter(**filter_data).values(*list_of_fields)
            data_list = list(data)
            print(data_list)
            return data_list    

        elif filter_value == "" or list_value != "":
            list_of_fields = list_value.split(',') #spliting list values using ","
            data = model.objects.all().values(*list_of_fields)
            data_list = list(data)
            return data_list

        elif filter_value != "" or list_value == "":
            filter_data = json.loads(filter_value) #converting str to dict
            data = model.objects.filter(**filter_data).all().values()
            data_list = list(data)
            return data_list
        
# Reports
from .models import *
from django.apps import apps

# class SharedExpense(Base):
#     event = models.ForeignKey(EventTracker,on_delete=models.CASCADE)
#     shared_expense = models.ForeignKey(SharedOutstationExpense,on_delete=models.CASCADE)
#     split_price = models.FloatField(default=0, blank=False, null=False)
#     split_ratio = models.FloatField(default=0,blank=True,null=True)

#     def __str__(self):
#         return self.shared_expense.name

def totalPriceUpdate(event_id,id,model,total_attr):
    event = CustomUser.objects.get(id = int(event_id))
    print("###############################################")
    model_instance = apps.get_model('users',model)
    
    transaction_obj = model_instance.objects.get(id=id)


    event_duration = event.end_date - event.start_date 
    event_hours = round(float(event_duration.total_seconds()/3600),2)

    total_price = getattr(event, total_attr)

    print(total_price)
    print(transaction_obj.event_price)

    event_price = event.event_total
    event_price = event_price - total_price
    total_price = total_price - transaction_obj.event_price

    print(event_price)
    print(total_price)
    print(transaction_obj.category)

    if transaction_obj.category == 'fixed':
        if model == 'EquipmentTransactions':
            transaction_price = transaction_obj.rental_cost
        else:
            transaction_price = transaction_obj.price
        print("--------------------Fix-------------------")
        print(transaction_price)
        print(total_price)
        total_price = total_price + transaction_price
        print(total_price)
        print(transaction_obj.price)
        print("----------------------------")
    
    elif transaction_obj.category == 'rate':
        if transaction_obj.rate_type == 'Day':
            multiplication_factor = round(float(event_hours/8),2)
            if model == 'EquipmentTransactions':
                transaction_price = float(transaction_obj.rental_cost * multiplication_factor)
            else:
                transaction_price = float(transaction_obj.price * multiplication_factor)

            total_price = total_price + transaction_price

            print(transaction_obj.price)
            print(transaction_price, multiplication_factor, "Day")


        elif transaction_obj.rate_type == 'Hourly':
            multiplication_factor = round(event_hours,2)
            if model == 'EquipmentTransactions':
                transaction_price = float(transaction_obj.rental_cost * multiplication_factor)
            else:
                transaction_price = float(transaction_obj.price * multiplication_factor)

            total_price = total_price + transaction_price

    else:
        return f"Category incorrect {transaction_obj.category}", 404

    print(transaction_obj.name, transaction_obj.event_price, transaction_price)
    setattr(transaction_obj, "event_price", transaction_price)
    transaction_obj.save()

    print(total_price)
    setattr(event, total_attr, total_price)
    event_price = event_price + total_price
    event.event_total = event_price
    event.save()
    print("###############################################")

    
def set_if_not_none(mapping, key, value):
    if value :
        print("valueee",value)
        mapping[key] = value


import mysql.connector
from decouple import config

# # connecting mysql database
# connection = mysql.connector.connect(
#   host=config('DATABASE_HOST'),
#   user=config('DATABASE_USER'),
#   password=config('DATABASE_PASSWORD'),
#   database=config('DATABASE_NAME')
# )


import pytz
from datetime import date, datetime
from usermanagement.settings import TIME_ZONE
# from django.utils import timezone

def naiveTimeConversion(date):
    aware_tz = pytz.timezone(TIME_ZONE)                     
    aware_time = aware_tz.localize(date)
    return aware_time

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        obj = str(obj)
        return obj
       
    raise TypeError ("Type %s not serializable" % type(obj))


import calendar
from datetime import date,datetime, timedelta

def get_days_in_month(month,year):

    _, days_in_month = calendar.monthrange(year, month)
    start_date = date(year,month,1)
    end_date = date(year,month,days_in_month)

    return start_date, end_date

# Monday to Sunday
def get_last_week_dates():
    today = datetime.today()
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = last_week_start + timedelta(days=6)
    return last_week_start, last_week_end


def get_last_month_and_year():
    today = datetime.today()
    last_month = today.month - 1 if today.month > 1 else 12
    last_year = today.year if today.month > 1 else today.year - 1
    return last_month, last_year


def get_last_four_months_days(total_months):
    today = datetime.today()
    last_four_months_days = []
    

    for i in range(total_months):
        month = today.month - i-1
        year = today.year

        if month <= 0:
            month += 12
            year -= 1

        _, days_in_month = calendar.monthrange(year, month)

        last_four_months_days.append(days_in_month)
        total_days = sum(last_four_months_days)
    return total_days

def get_total_days_in_year(year):
    return 365 if not calendar.isleap(year) else 366


import json
from usermanagement.settings import BASE_DIR
import os

def generate_and_save_json(data, creator):
    # Fetch data from the Django model or create a dictionary manually
    json_data = {
        "action": "csv",
        "data": data,
        "createdBy": creator
    }

    # Convert data to JSON string
    json_data = json.dumps(json_data,default=json_serial)

    # Open a file in write mode

    path = os.path.join(BASE_DIR,"users/report_json.json")

    print(path)
    with open(path, "w+") as file:
        # Write the JSON string to the file
        file.write(json_data)
        file.close()
    
    return path
    # Call the function to generate and save the JSON
