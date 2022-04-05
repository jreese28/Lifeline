from re import template
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import pyrebase

# Create your views here.
#def homepage(request):
#    return HttpResponse("Wow")

firebaseConfig = {
  "apiKey": "AIzaSyD3b8GXxpcjGhI-2nBVQM2hu_3JUpLj-uM",
  "authDomain": "seniorproject-husp22.firebaseapp.com",
  "databaseURL": "https://seniorproject-husp22-default-rtdb.firebaseio.com",
  "projectId": "seniorproject-husp22",
  "storageBucket": "seniorproject-husp22.appspot.com",
  "messagingSenderId": "759118984872",
  "appId": "1:759118984872:web:0d5ff96057621826e3749d",
  "measurementId": "G-MVNFP9QRN2"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

def index(request):
  #accessing our firebase data and storing it in a variable
  medicine = db.child('medicine').child('1').child("name").get().val()
  directions = db.child('medicine').child('1').child("directions").get().val()
  schedule = db.child('medicine').child('1').child("schedule").get().val()

  #medicine = db.child("people").order_by_child("age").start_at(30).get()
  #for med in medicine.each():
    # print(med.val()["name"])

  context = {
      'medicine':medicine,
      'directions':directions,
      'schedule':schedule
  }
  return render(request, 'index.html', context)

def add(request):
    return render(request, 'add.html')

class HomePageView(TemplateView):
  template_name = "index.html"

class AddPageView(TemplateView):
  template_name = "add.html" 

class ProfilePageView(TemplateView):
  template_name = "profile.html" 

class LogInPageView(TemplateView):
  template_name = "login.html"

class LoggedInPageView(TemplateView):
  template_name = "loggedin.html"

def signIn(request):
  return render(request, 'login.html')


def postSignIn(request):
  email=request.POST.get('email')
  passw=request.POST.get('password')
  try:
    user=auth.sign_in_with_email_and_password(email,passw)
  except:
    message="invalid credentials"
    return render(request, "login.html",{"messg":message})
  #print(user)
  return render(request, "loggedin.html",{"e":email})

'''
def view_name(request):
  if request.method == "POST":
    existingEmail = request.POST.get("handle", None)
    print(existingEmail)
  return render(request, "login.html")

    try:
      auth.sign_in_with_email_and_password(existingEmail,existingPassword)
      print("Successful log in!")
    except:
      print("Invalid email or password. Try again.")
'''
