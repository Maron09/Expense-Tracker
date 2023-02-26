from django.shortcuts import render
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
import os
import json
import pdb
# Create your views here.



def index(request):

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currency.json')

    with open(file_path, 'r') as f:
        data = json.load(f)

        for k, v in data.items():
            currency_data.append({'name':k, 'value':v})
        

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None

    if exists:
       user_preferences = UserPreference.objects.get(user=request.user)
    # pdb.set_trace()

    if request.method == 'GET':


        # context= {'currency_data':currency_data}

        
        return render(request, 'preferences/index.html', {'currency_data': currency_data,
                                                          'user_preferences': user_preferences})
    else:
        currency = request.POST['currency']

        if exists:
            
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes Saved')
        return render(request, 'preferences/index.html', {'currency_data': currency_data,
                                                          'user_preferences': user_preferences})
