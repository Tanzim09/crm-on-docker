from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http  import HttpResponse
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
  records = Record.objects.all()
  if request.method == 'POST':
    username = request.POST['user_name']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      messages.success(request, "You have logged in")
      return redirect('Home')
    else:
      messages.error(request, "Error")
      return redirect('Home')
  
  else: 
    return render(request, 'website/home.html', {'records': records})



def login_user(request):
  pass

def logout_user(request):
  logout(request)
  messages.success(request, 'You have been logged out!')
  return redirect('Home')


def register_user(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)
      login(request,user)
      messages.success(request, 'You have been registered!')
      return redirect('Home')
    
    else:
      # IMPORTANT: return a response when the form is invalid
      # messages.error(request, 'Please fix the errors below.')
      return render(request, 'website/register.html', {'form': form})
  
  else:
    form = SignUpForm()
    return render(request, 'website/register.html', {'form': form})


      
  # return render(request, 'website/register.html')


def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'website/record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('Home')





def delete_record(request, pk):
   if request.user.is_authenticated:
    delete_it = Record.objects.get(id=pk)
    delete_it.delete()
    messages.success(request, "Record Deleted Successfully...")
    return redirect('Home')
   
   else:
    messages.success(request, "You Must Be Logged In...")
    return redirect('Home')
   

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('Home')
		return render(request, 'website/add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('Home')





def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('Home')
		return render(request, 'website/update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('Home')