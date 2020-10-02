from django.shortcuts import render

#Make the necessary imports

# Additional imports we'll need:
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse


#Import access to only admin user
from django.contrib.admin.views.decorators import staff_member_required

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# iMPORT THINGS FROM MODELS

from .models import Yam, Plantain, Potatoe, Purchased


# THIS IMPORT ALLOWS US TO SEND Email to a user in django
from django.core.mail import send_mail


# Create your views here.

# Food menu is a list consisting of the food on the menu. If a new menu is added, it must be registered here to be visible to customers
foodMenu = [['Plantain', Plantain.objects.all()], ['Potatoe', Potatoe.objects.all()], ['Yam', Yam.objects.all()]]

#
from django.core import validators
from django.core.validators import RegexValidator
from django.forms import CharField


#


#Create form for user login
class LoginForm(forms.Form):
    
    #Validators allows you choose for example, what should not be allowed on a field. validate_slug allows only alphanumeric text, and that is what we want in this case
    username = forms.CharField(max_length=25, min_length=2, label='Username', validators=[validators.validate_slug])
    password = forms.CharField(max_length=25, min_length=5, widget=forms.PasswordInput, label='Password')

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=25, min_length=2, label='Username', validators=[validators.validate_slug])
    
    email = forms.EmailField()
    password1 = forms.CharField(max_length=25, min_length=5, widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=25, min_length=5, widget=forms.PasswordInput, label='Retype Password')


#Message to be displayed on pages
displayMsgs=['Complete the day with bole and Pepsi', 'Saturdays are more fun with Bole', 'Delicious is the word we put in your mouth']


#Registration page
def register(request):
    if request.method == "POST":
        
        #If post request, get the details from the form
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            #if username already exist, return to form, ith a message saying username has already been taken
            if User.objects.filter(username=username).exists():
                return render(request, 'bolemix/register.html', {'form': RegisterForm(), 'msg': 'Username has already been taken. Try a different one '})
            
            #Else, if username is not taken, try verifying both passwords coincide, and that email hasnt been taken
            else:
                #If both passwords do not coincide, return a passwords do not match response
                if password1 != password2:
                    return render(request, 'bolemix/register.html', {'form': form, 'msg': 'Passwords do not match '})
                elif User.objects.filter(email=email).exists():
                    return render(request, 'bolemix/register.html', {'form': form, 'msg': 'Email already in use '})
                
                #If all criteria is met, register user
                else:
                    user = User.objects.create_user(username, email, password1)
                    user.save()
                    
                    #Redirect user to login page
                    return HttpResponseRedirect(reverse('loginPage'))      

        else:
            return render(request, 'bolemix/register.html', {'form': RegisterForm(), 'msg': 'Please, use only alphanumeric characters '})          

    else:
        form = RegisterForm()
        return render(request, 'bolemix/register.html', {'form': form, 'msg': 'Delicious is the word we put in your mouth. Sign up to enjoy the taste we bring'})


def loginPage(request):
    if request.method == 'POST':
        #check if user is 
        form = LoginForm(request.POST)


        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            
            
            # Check if username and password are correct, returning User object if so
            user = authenticate(request, username=username, password=password)

            # If user object is returned, log in and route to menu page:
            if user is not None:
                login(request, user)
                #Route to menu pagereturn 
                return HttpResponseRedirect(reverse('menu'))
                
            else:
                return render(request, 'bolemix/login.html', {'form': LoginForm(),'msg': 'Username does not match password'})
        
        else:
            return render(request, 'bolemix/login.html', {'form': LoginForm(),'msg': 'Username must be alphanumeric'})

    else:
        #Include display message chosen by admin, to everyone's page
        if len(displayMsgs)>0:
            length = len(displayMsgs) - 1
            displayMsg = displayMsgs[length]
        else:
            displayMsg = ''
        form = LoginForm()
        return render(request, 'bolemix/login.html', {'form': form, 'msg': displayMsg})

#Menu 
def menu(request):
    #If user is authenticated, gonto menus page
    if request.user.is_authenticated:
        #Include display message chosen by admin, to everyone's page
        if len(displayMsgs)>0:
            length = len(displayMsgs) - 1
            displayMsg = displayMsgs[length]
        else:
            displayMsg = ''  

        #Carry users to home page
        return render(request, 'bolemix/menus.html', {'total':foodMenu, 'displayMsg': displayMsg, 'user': request.user})
    
    #Else, return to logim page
    else:
        return render(request, 'bolemix/login.html', {'form': LoginForm(),'msg': 'Log in to get access to dbolemix'})

    
def getmenu(request, names):

    if request.user.is_authenticated:
        #Include display message chosen by admin, to everyone's page
        if len(displayMsgs)>0:
            length = len(displayMsgs) - 1
            displayMsg = displayMsgs[length]
        else:
            displayMsg = ''
        

        for val in foodMenu:
            if val[0] == names:
                foodItems = val[1]

                return render(request, 'bolemix/menus.html', {'foodItems': foodItems, 'total': foodMenu, 'displayMsg': displayMsg, 'user': request.user})

    else:
        return render(request, 'bolemix/login.html', {'form': LoginForm(),'msg': 'Log in to get access to dbolemix'})

#cart function is what processes the objects passed to to the cart for possible purchase, by converting them to sessions that can be passed around
def cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            total = request.POST['total']
            products = request.POST['buys']
            
            #store purchases in session
            request.session['products'] = products
            request.session['total'] = total
            return JsonResponse({"post": products, 'total': total})
        else:
            return HttpResponseRedirect(reverse('menu'))
    
    else:
        return render(request, 'bolemix/login.html', {'form': LoginForm(),'msg': 'Log in to get access to dbolemix'})


#Purchase does the job of redirecting users to the cart containing their purchases, and allow them edit it if they want
def purchased(request):

    #Get products and total stored in session
    if request.user.is_authenticated:
        products = request.session.get('products')
        total = request.session.get('total')
    
        
        
        #return HttpResponse(f'{products} - {total}')
        return render(request, 'bolemix/cart.html', {'total': total, 'products': products, 'user': request.user})    


#bought does the job of adding each purchase to the database of purchased items, with a status of pending. Each purchase is uniquely identified by their details
def bought(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # get form details 
            total = request.POST['total']
            deliverTo = request.POST['deliverTo']
            products = request.POST['products']
            address = request.POST['address']
            phone = request.POST['phone']
            time = request.POST['time']
            comment = request.POST['comment']
            

            
    


            #Store purchase in Purchased model(table)
            purchase = Purchased(products=products, total=total, address=address, deliverTo=deliverTo, phone=phone, user=str(request.user), statusValue='pending', time=time, comment=comment)
            purchase.save()
            # Append to list showing all purchases
            newPurchase = {
            #user: request.user
            'products' : products,
            'total' : total,
            'address': address,   
            'deliverTo': deliverTo,
            'phone' : phone
            }
            request.session['products'] = str([])
            request.session['total'] = str(0)
            #Return JsonResponse
            #return JsonResponse({'time': 'time'})
            return JsonResponse(newPurchase)

        #Done just to let us see what is in our list item
        else:
            return render(request, 'bolemix/cart.html', {'msg': 'No item pushed to cart yet'})    
    
    else:
        return render(request, 'bolemix/login.html', {'form': LoginForm(),'msg': 'Log in to get access to dbolemix'})        




#Requested does the job of showing users sort of their purchase history
def requested(request):
    if request.user.is_authenticated:
    
        # Convert returned table data to dictionaries, which are easier to work with in JavaScript

        #For pending purchases
        pendingPurchases = []
        for purchase in Purchased.objects.filter(user=str(request.user)).filter(statusValue='pending'):
            pendingPurchase = {"user": str(purchase.user), "products": str(purchase.products), "deliverTo": str(purchase.deliverTo), "phone": str(purchase.phone), "address": str(purchase.address), 'total': str(purchase.total), 'time':str(purchase.time), 'comment': str(purchase.comment)}
            pendingPurchases.append(pendingPurchase)
        
        #For received Purchases
        receivedPurchases = []
        for purchase in Purchased.objects.filter(user=str(request.user)).filter(statusValue='received'):
            receivedPurchase = {"user": str(purchase.user), "products": str(purchase.products), "deliverTo": str(purchase.deliverTo), "phone": str(purchase.phone), "address": str(purchase.address), 'total': str(purchase.total), 'time':str(purchase.time), 'comment': str(purchase.comment)}
            receivedPurchases.append(receivedPurchase) 

        #For delivered Purchases
        deliveredPurchases = []
        for purchase in Purchased.objects.filter(user=str(request.user)).filter(statusValue='delivered'):
            deliveredPurchase = {"user": str(purchase.user), "products": str(purchase.products), "deliverTo": str(purchase.deliverTo), "phone": str(purchase.phone), "address": str(purchase.address), 'total': str(purchase.total), 'time':str(purchase.time), 'comment': str(purchase.comment)}
            deliveredPurchases.append(deliveredPurchase)


        
        #Pass in details for each purchase by the specific user
        return render(request, 'bolemix/purchases.html', {'pendingPurchases': pendingPurchases, 'receivedPurchases': receivedPurchases, 'deliveredPurchases': deliveredPurchases, 'user': request.user})




#This url route can only be accessed by staff(admin) 
# It is used for both editing purchase status(e.g from pending to received) as well as showing history of purchases for All users
@staff_member_required
def adminDetails(request):
    if request.method == 'POST':
        # get form details 
        user = str(request.POST['user'])
        total = str(request.POST['total'])
        deliverTo = str(request.POST['deliverTo'])
        products = str(request.POST['products'])
        address = str(request.POST['address'])
        phone = str(request.POST['phone'])
        statusValue = str(request.POST['statusValue'])
        time = str(request.POST['time'])
        comment = str(request.POST['comment'])
        
        #If request has status of pending, convert to received
        if 'pending' in statusValue:
            p = Purchased.objects.filter(phone__contains=phone).filter(statusValue__contains=statusValue).filter(address__contains=address).filter(time__contains=time).filter(user__contains=user).first()
            # This is where we use the send_mail function to send email to the use telling them about we have received their purchase.
            send_mail(f'hello {request.user}', f'We got your purchases. We are glad you thought about us. We will be delivering your Purchases totalling {total}. It will be delivered to {address}', 'atumasaake@gmail.com', [request.user.email], fail_silently=False)

            
            p.statusValue='received'
            p.save()

            
            return JsonResponse({"p": products})
        
        #if request has status of received, convert to delivered
        elif 'received' in statusValue:
            p = Purchased.objects.filter(phone__contains=phone).filter(statusValue__contains=statusValue).filter(address__contains=address).filter(time__contains=time).filter(user__contains=user).first()
            p.statusValue='delivered'
            p.save()
            return JsonResponse({"p": products})
        
        
    else:
        # Convert returned table data to dictionaries, which are easier to work with in JavaScript

        #For pending purchases
        pendingPurchases = []
        for purchase in Purchased.objects.filter(statusValue='pending'):
            pendingPurchase = {"user": str(purchase.user), "products": str(purchase.products), "deliverTo": str(purchase.deliverTo), "phone": str(purchase.phone), "address": str(purchase.address), 'total': str(purchase.total), 'statusValue':str(purchase.statusValue), 'time':str(purchase.time), 'comment': str(purchase.comment)}
            pendingPurchases.append(pendingPurchase)
        
        #For received Purchases
        receivedPurchases = []
        for purchase in Purchased.objects.filter(statusValue__contains='received'):
            receivedPurchase = {"user": str(purchase.user), "products": str(purchase.products), "deliverTo": str(purchase.deliverTo), "phone": str(purchase.phone), "address": str(purchase.address), 'total': str(purchase.total), 'statusValue':str(purchase.statusValue), 'time':str(purchase.time), 'comment': str(purchase.comment)}
            receivedPurchases.append(receivedPurchase) 

        #For delivered Purchases
        deliveredPurchases = []
        for purchase in Purchased.objects.filter(statusValue='delivered'):
            deliveredPurchase = {"user": str(purchase.user), "products": str(purchase.products), "deliverTo": str(purchase.deliverTo), "phone": str(purchase.phone), "address": str(purchase.address), 'total': str(purchase.total), 'statusValue':str(purchase.statusValue), 'time':str(purchase.time), 'comment': str(purchase.comment)}
            deliveredPurchases.append(deliveredPurchase)


        
        #Pass in details for each purchase by the specific user
        return render(request, 'bolemix/adminviews.html', {'pendingPurchases': pendingPurchases, 'receivedPurchases': receivedPurchases, 'deliveredPurchases': deliveredPurchases})
        

@staff_member_required
def displaymsg(request):
    if request.method == 'POST':
        displayMsg = request.POST['msgToDisplay']
        displayMsgs.append(displayMsg)
        return render(request, 'bolemix/displaymsg.html', {'displayMsg': displayMsg})
        

    else:
        return render(request, 'bolemix/displaymsg.html')


def logoutView(request):
    logout(request)
    return render(request, 'bolemix/login.html', {'form': LoginForm(),'msg': 'Logged out'})

def pract(request):
    if request.user.is_authenticated:
        name= 'Samuel'
        address = 'No 13 Amadi street, Mgbouba, Port Harcourt'
        send_mail('hello', f'hey {name}, your address is {address} You fool', 'atumasaake@gmail.com', [request.user.email], fail_silently=False)
        
        return HttpResponse('Email sent successfully')