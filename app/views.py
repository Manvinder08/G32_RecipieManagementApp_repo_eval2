
from django.shortcuts import render, redirect
from app.models import CustomUser,Recipe
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
import re
import random

def home_view(request):
    user_id = request.session.get("user_id")
    if user_id:
        return render(request, "index.html", {"auth":True})
    else:
        return render(request, "index.html", {"auth":False})



def register(request):

    if request.method == "POST":
        username = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirm_password")
        mobileNumber = request.POST.get("mobile")
        print(username, email, password, mobileNumber, confirmPassword)

        if not all([username, email, password, confirmPassword, mobileNumber]):
            return render(request, "register.html", {"error": "All fields are required"} )

        if password != confirmPassword:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if len(password) < 8:
            return render(request, "register.html", {"error": "Password must be at least 8 characters long"})

        if not re.search(r"[A-Z]", password):
            return render(request, "register.html", {"error": "Password must contain at least one uppercase letter"})

        if not re.search(r"\d", password):
            return render(request, "register.html", {"error": "Password must contain at least one number"})

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return render(request, "register.html", {"error": "Password must contain at least one special character"})
        
        if len(mobileNumber) != 10 :
            return render(request, "register.html", {"error": "Mobile number must be at least 10 digits long"})
        
        
        



        if CustomUser.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "User with this email aldready exists"})
        if CustomUser.objects.filter(mobile_number=mobileNumber).exists():
            return render(request, "register.html", {"error": "User with this mobile number already exists"})

        user = CustomUser.objects.create(username=username, email=email, password=make_password(password) ,mobile_number=mobileNumber)
        request.session["user_id"] = user.id  
        request.session["username"] = user.username


        return redirect("home")

    return render(request, "register.html")





def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
            if check_password(password, user.password):
                request.session["user_id"] = user.id 
                return redirect("home")
            else:
                return render(request, "login.html", {"error": "Incorrect password"})
        except CustomUser.DoesNotExist:
            return render(request, "login.html", {"error": "User does not exist"})

    return render(request, "login.html")




def logout_view(request):
    request.session.flush()  
    return redirect("home")




def post_recipe(request):

    user_id = request.session.get("user_id")
    isadmin = request.session.get("admin") 
    if not user_id:
                return redirect('login')
    
    if isadmin==False :
                return redirect('home')



    if request.method == "POST":
        title = request.POST.get("title")
        img_url = request.POST.get("image")
        overview = request.POST.get("overview")
        ingredients = request.POST.get("ingredients")
        time = request.POST.get("time")
        process = request.POST.get("process")


        Recipe.objects.create(
            title=title,
            img_url=img_url,
            overview=overview,
            ingredients=ingredients,
            time_to_prepare=time,
            full_process=process
        )

        return render(request, 'post.html',{"error": "Recipe posted successfully"})

    return render(request, 'post.html')



# def get_all_recipes(request):
#     user_id = request.session.get("user_id")


#     if not user_id:
#         return redirect('login')

#     isadmin =  CustomUser.objects.get(id=user_id)

#     recipies = Recipe.objects.all()
#     trending_recipes = recipies[3:6]
#     for recipe in trending_recipes:
#         recipe.ingredient_list = recipe.ingredients.split(',')

#     for r in recipies:
#         r.ingredient_list = r.ingredients.split(',')[:5]
#         r.short_overview = ' '.join(r.overview.split()[:21])
    

#     return render(request, "main.html", {
#         "recipies": recipies,  
#         'trending_recipes': trending_recipes,
#         "isadmin": isadmin.is_admin,
#         "username": isadmin.username
#     })




def get_all_recipes(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect('login')

    isadmin = CustomUser.objects.get(id=user_id)

    veg_param = '1'
    if(request.GET.get('veg')):
        veg_param = request.GET.get('veg')
        if veg_param == '1':
            recipies = Recipe.objects.filter(is_veg=True)
        else:
            recipies = Recipe.objects.all()

    if veg_param == '1':
        recipies = Recipe.objects.filter(is_veg=True)
    else:
        recipies = Recipe.objects.all()

    trending_recipes = recipies[3:6]
    
    for recipe in trending_recipes:
        recipe.ingredient_list = recipe.ingredients.split(',')

    for r in recipies:
        r.ingredient_list = r.ingredients.split(',')[:5]
        r.short_overview = ' '.join(r.overview.split()[:21])

    return render(request, "main.html/", {
        "recipies": recipies,  
        'trending_recipes': trending_recipes,
        "isadmin": isadmin.is_admin,
        "username": isadmin.username,
        "veg": veg_param,
    })




def recipe_profile(request, recipe_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')

    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    recipe.ingredient_list = recipe.ingredients.split(",")

    return render(request, 'recipie.html', {'recipie': recipe})
    




def updaterecipiepost(request, recipieid):
    recipie = get_object_or_404(Recipe, id=recipieid)

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')
    isadmin =  CustomUser.objects.get(id=user_id).is_admin
    if not isadmin:
        return redirect('main')

    if request.method == 'POST':
        recipie.title = request.POST.get('title')
        recipie.img_url = request.POST.get('image')
        recipie.overview = request.POST.get('overview')
        recipie.ingredients = request.POST.get('ingredients')
        recipie.time_to_prepare = request.POST.get('time')
        recipie.full_process = request.POST.get('process')
        recipie.save()
        return render(request,'update.html',{'error': "Recipie Updated Successfully",'recipie': recipie})  

    return render(request, 'update.html', {'recipie': recipie})



def deleterecipe(request, recipieid):
    try:
        recipie = Recipe.objects.get(id=recipieid)
    except Recipe.DoesNotExist:
        return redirect('main')  

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')
    isadmin = CustomUser.objects.get(id=user_id).is_admin
    if not isadmin:
        return redirect('main')

    recipie.delete()
    return redirect('main')




def search_recipes(request):

    user_id = request.session.get("user_id")


    if not user_id:
        return redirect('login')

    user =  CustomUser.objects.get(id=user_id)


    query = request.GET.get('q', '')
    

    results = []
    if(query==""):
        return redirect('main')

    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(ingredients__icontains=query)
    )



    for r in results:
        r.ingredient_list = r.ingredients.split(',')[:5]
        r.short_overview = ' '.join(r.overview.split()[:21])
    
    if(len(results)==0):
        return render(request, 'main.html', {'query': query ,"username":user.username,'recipies': results,"found":True,"isadmin": user.is_admin}) 
    else:
        return render(request, 'main.html', {'query': query ,"username":user.username,'recipies': results,"isadmin": user.is_admin,})



    
    
