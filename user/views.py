from xml.dom import ValidationErr
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from .models import Customer
import json


@require_POST
@csrf_exempt  #! REMOVE LATER. ONLY FOR TESTING
def registerUser(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)

    # will take all the data sent from the front-end through an HTTP POST request
    form = RegisterForm(data)

    if form.is_valid():
        try:
            # if the data are valid create a new customer object with the updated data
            user = Customer.objects.create_user(  # type: ignore
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"],
                date_of_birth=form.cleaned_data["date_of_birth"],
            )

            # login will create a session and create a session cookie and login will allow us to use the user details in different views later
            login(request, user)
            return JsonResponse(
                {"success": True, "message": "User registered successfully"}, status=200
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        errors = form.errors.as_json()
        return JsonResponse({"success": False, "errors": errors}, status=400)


@require_POST
@csrf_exempt
def loginUser(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    form = LoginForm(data)

    if form.is_valid():
        user = form.cleaned_data["user"]

        # provide a session cookie and login the user
        login(request, user)
        return JsonResponse(
            {"success": True, "message": "User login successful"}, status=200
        )
    else:
        errors = form.errors.as_json()
        return JsonResponse({"success": False, "error": errors}, status=400)
