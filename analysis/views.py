from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(user=request.user)
    context = {'expenses':expenses}

    return render(request, 'expenses/index.html', context)



def add_expenses(request):

    categories = Category.objects.all()

    context = {'categories': categories, 'values': request.POST}

    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)
    

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Please enter an amount')
            return render(request, 'expenses/add_expenses.html', context)

    
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']


        if not description:
            messages.error(request, 'Please enter a description')
            return render(request, 'expenses/add_expenses.html', context)
        
        Expense.objects.create(user=request.user, amount=amount, description=description, date=date, category=category)
        messages.success(request, 'Expense added successfully')
    return redirect('home')
    
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {'expense': expense, 'values':expense, 'categories': categories}
    if request.method == 'GET':
        return render(request, 'expenses/edit.html', context)
    else:
        messages.info(request, 'Expense updated successfully')
        return render(request, 'expenses/edit.html', context)
