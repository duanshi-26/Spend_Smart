from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
import os
from datetime import datetime
from django.conf import settings

EXPENSES_FILE = os.path.join(settings.BASE_DIR, 'expenses.json')

def index(request):
    return render(request, 'app/index.html')

@csrf_exempt
def expenses(request):
    if request.method == 'GET':
        try:
            with open(EXPENSES_FILE, 'r') as f:
                expenses = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            expenses = []
        return JsonResponse(expenses, safe=False)
    elif request.method == 'POST':
        try:
            with open(EXPENSES_FILE, 'r') as f:
                expenses = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            expenses = []
        data = json.loads(request.body)
        new_expense = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'description': data['description'],
            'amount': float(data['amount']),
            'category': data['category'],
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        expenses.append(new_expense)
        with open(EXPENSES_FILE, 'w') as f:
            json.dump(expenses, f, indent=2)
        return JsonResponse(new_expense, status=201)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def delete_expense(request, id):
    if request.method == 'DELETE':
        try:
            with open(EXPENSES_FILE, 'r') as f:
                expenses = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            expenses = []
        expenses = [expense for expense in expenses if expense['id'] != id]
        with open(EXPENSES_FILE, 'w') as f:
            json.dump(expenses, f, indent=2)
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['DELETE'])
