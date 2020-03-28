import json
import bcrypt
import jwt

from .models       import Account
from .utils        import Login_Check, validate_password, validate_special_char
from my_settings   import SECRET_KEY

from django.views            import View
from django.http             import HttpResponse, JsonResponse
from django.db               import IntegrityError
from django.core.validators  import validate_email
from django.core.exceptions  import ValidationError
from django.db               import IntegrityError, transaction

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            validate_email(data["email"])

            if validate_special_char(data["email"]):
                return JsonResponse({"message" : "INVALID_CHAR"}, status=400)

            if validate_password(data["password"]):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)

            if Account.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message" : "EXISTS_EMAIL"}, status=400)

            Account(
                username  = data['username'],
                email     = data["email"],
                password  = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
            ).save()

            return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)        

        try:
            validate_email(data["email"])

            if validate_special_char(data["email"]):
                return JsonResponse({"message" : "INVALID_CHAR"}, status=400)

            if Account.objects.filter(email=data["email"]).exists():
                user = Account.objects.get(email=data["email"])

                if bcrypt.checkpw(data["password"].encode(), user.password.encode("UTF-8")):
                    token = jwt.encode({"email" : data["email"]}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")

                    return JsonResponse({"Authorization" : token}, status=200) 

                return HttpResponse(status=401)

            return JsonResponse({"message" : "NOT_EXISTS_MAIL"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)


class ProfileView(View):
    @Login_Check
    def get(self, request):
        try:
            profile = Account.objects.filter(id = request.user).values('username', 'email', 'phone')

            return JsonResponse({"account_profile": list(profile)}, status=200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({'message': 'ACCOUNT_DOES_NOT_EXISTS'}, status=401)