from re import template
from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import logout
import pyrebase
from datetime import datetime

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


##### --------- VIEW PAGE FUNCTIONS ---------- ######



def index(request):
  # home page view of medicine
  medicine_list = []
  medicine_dict = {}

  uid = request.session['uid']
  user_meds = db.child("people").child(uid).child("presc").get()
  user_meds_dict = user_meds.val() # OrderedDict([('medsID', ['m1', 'm2'])])
  if user_meds_dict is not None:
    user_meds_dict = user_meds_dict.values() # odict_values([['m1', 'm2', 'm3']])
    
    user_meds_list = list(user_meds_dict)[0] # ['m1', 'm2', 'm3']

    for med in user_meds_list:
      med_info = db.child("medicine").child(str(med)).get()
      medicine_dict[med_info.key()] = med_info.val()
  
  medicine_list = medicine_dict.values()

  context = {
      'medicine':medicine_list
  }
  return render(request, 'index.html', context)
  


def add(request):
  # manage page function to add medicine
  selected=request.POST.get('selectedMed')
  added_med_id = db.child("medicine").get()
  for med in added_med_id.each():
    if med.val()['name'] == selected:
      med_id = med.key()
      db.child("people").child(request.session['uid']).child("presc").child("medsID").update({ med_id: med_id})
  return render(request, 'add.html')


def deleteMed(request):
  # manage page function to delete medicine
  selected=request.POST.get('selectedMed')
  print(selected)
  meds_id = db.child("medicine").get()
  for med in meds_id.each():
    if med.val()['name'] == selected:
      med_id = med.key()
  med_id = med_id
  trytest = db.child("people").child(request.session['uid']).child("presc").child("medsID").child(med_id).get() 
  if trytest.val() is None:
    message= selected + "is not in your medicine list."
    return render(request, "add.html",{"messg":message}) 
  db.child("people").child(request.session['uid']).child("presc").child("medsID").child(med_id).remove() 
  return index(request)


def signIn(request):
  #display log in page upon entering app
  return render(request, 'login.html')


def postSignIn(request):
  # logs user in and fetches user's data from database
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
  # ends user session and returns to log in page
  try:
      del request.session['uid']
      auth.logout(request)
  except:
      pass
  return render(request,"login.html")


def postSignUp(request):
  # creates user in the firebase authenticaton and the database
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
  # prompts user to populate profile info and stores it in database
  name=request.POST.get('fullname')
  birthday=request.POST.get('birthday')
  phone=request.POST.get('phone')
  db.child("people").child(request.session['uid']).update({'name':name})
  db.child("people").child(request.session['uid']).update({'birthday':birthday})
  db.child("people").child(request.session['uid']).update({'phone':phone})
  #return render(request, 'home.html')
  return add(request)

def profile(request):
  user_info = db.child("people").child(request.session['uid']).get()
  user_info = user_info.val()
  bday = user_info['birthday']
  bday = datetime.strptime(user_info['birthday'], '%Y-%m-%d')

  bday = bday.strftime("%b %d %Y")
  user_info['birthday'] = bday

  context = {
      "user_info":user_info
  }
  return render(request, 'profile.html', context)


# shows description page
class DescriptionPageView(TemplateView):
  template_name = "description.html"
