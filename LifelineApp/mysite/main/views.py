from re import template
from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
import pyrebase
from django.contrib import auth
from django.contrib.auth import logout


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
autho = firebase.auth()
storage = firebase.storage()

def index(request):
  #accessing our firebase data and storing it in a variable
  medicine_list = []
  medicine_dict = {}

  #print(udata['localId'])
  uid = request.session['uid']
  #user_meds = db.child("people").child(uid).child("prescriptions").get()
  user_meds = db.child("people").child(uid).child("presc").get()
  print("user_meds key:   " + user_meds.key()) # presc
  user_meds_dict = user_meds.val() # OrderedDict([('medsID', ['m1', 'm2'])])
  if user_meds_dict is not None:
    user_meds_dict = user_meds_dict.values() # odict_values([['m1', 'm2', 'm3']])
    
    user_meds_list = list(user_meds_dict)[0] # ['m1', 'm2', 'm3']

    for med in user_meds_list:
      print("med" + med)
      med_info = db.child("medicine").child(str(med)).get()
      print( " med_ info key " + med_info.key())
      print(med_info.val())
      medicine_dict[med_info.key()] = med_info.val()
  
  medicine_list = medicine_dict.values()

  context = {
      'medicine':medicine_list
  }
  return render(request, 'index.html', context)
  
'''
    med_info = med.val()
    if med_info is not None:
      medicine_dict[med.key()] = med_info
  medicine_list = medicine_dict.values()
'''

'''
users_medicines = db.child("people").child(uid).child("prescriptions").get() # in this case would be m1
for user_med in users_medicines.each():

  users_med_info =  db.child("medicine").child(users_medicines).get() 

added_med_id = db.child("medicine").get()
for med in added_med_id.each():
  if med.val()['name'] == selectedToAdd:
    med_id = med.key()
    db.child("people").child(uid).update({"prescriptions": med_id})
'''



def add(request):
  selected=request.POST.get('selectedToAdd')
  #print(dict(request.POST))
  #print(selected)
  added_med_id = db.child("medicine").get()
  for med in added_med_id.each():
    #print("key: "+ med.key())
    #print("val: "+ med.val()['name'])
    if med.val()['name'] == selected:
      med_id = med.key()
      #db.child("people").child(request.session['uid']).child("prescriptions").update({"med_id": med_id})
      db.child("people").child(request.session['uid']).child("presc").child("medsID").update({ med_id: med_id})
      #print("updated!")
  return render(request, 'add.html')


def signIn(request):
  return render(request, 'login.html')


def postSignIn(request):
  email=request.POST.get('email')
  passw=request.POST.get('password')
  try:
    user=autho.sign_in_with_email_and_password(email,passw)
  except:
    message="Invalid log in credentials."
    return render(request, "login.html",{"messg":message})
  session_id=user['idToken']
  uid = user['localId']
  request.session['uid'] = uid
  return index(request)


def logOut(request):
  try:
      del request.session['uid']
      auth.logout(request)
  except:
      pass
  return render(request,"login.html")


def postSignUp(request):
  email=request.POST.get('newemail')
  password=request.POST.get('newpassword')
  try:
    user=autho.create_user_with_email_and_password(email, password)
    uid = user['localId']
  except:
    message="A user with this email already exists."
    return render(request, "login.html",{"messg":message})
  uid = user['localId']
  request.session['uid'] = uid
  db.child("people").child(request.session['uid']).update({'email':email})


  context = {
      "email":email
  }
  return render(request, 'profile.html', context)


def register(request):
  print( "in register:  " +request.session['uid'])
  name=request.POST.get('fullname')
  print("REGISTRATION NAME " + name)
  birthday=request.POST.get('birthday')
  print("REGISTRATION birthday " + birthday)
  db.child("people").child(request.session['uid']).update({'name':name})
  print("1")
  db.child("people").child(request.session['uid']).update({'birthday':birthday})
  print("2")
  #return render(request, 'home.html')
  return index(request)


def profile(request):
  user_info = db.child("people").child(request.session['uid']).get()
  user_info = user_info.val()




  context = {
      "user_info":user_info
  }
  return render(request, 'profile.html', context)
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

class DescriptionPageView(TemplateView):
  template_name = "description.html"
