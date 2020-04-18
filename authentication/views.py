import random
import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.email_thread import SendEmailThread
from authentication.permissions import IsOwnerOrReadOnly as IsOwnerOnly
from utils import check_token_autorization
from .models import UserProfile, PaymentMethod as PaymentMethodModel, PinVerify, PasswordReset
from apartment.models import Review, Apartment
from apartment.serializers import ReviewSerializer
from .serializers import UserRegisterSerializer, VerifyUserSerializer
from bongalo_backend.settings import PINDO_API_TOKEN
from cryptography.fernet import Fernet


def send_email(to, subject, message):
    print(settings.DEFAULT_FROM_EMAIL)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to],
        fail_silently=False,
    )


def send_sms(to, message):
    # TODO : Put token in dotenv files need to be refractored
    token = PINDO_API_TOKEN
    headers = {'Authorization': 'Bearer ' + token}

    # Add country code if not present
    if "+25" not in to:
        to = "+25" + to

    data = {'to': to, 'text': message, 'sender': 'Bongalo LTD'}

    url = 'http://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)


class UserVerifyView(APIView):
    def post(self, request):
        if not UserProfile.objects.filter(uuid=request.data.get('user'), is_active=True).exists():
            response = {
                'message': 'User does not exists'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        user = UserProfile.objects.get(uuid=request.data.get('user'), is_active=True)
        verification_image = request.data.get('verification_image')
        if not verification_image:
            response = {
                'message': 'Verification image is needed'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('is_passport') is None:
            response = {
                'message': 'is_passport field is required'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('is_passport'):
            user.passport = verification_image
        else:
            user.national_id = verification_image

        user.save()

        email_message = "Hi \nA user with name {} {} has requested to verify his account".format(user.user.first_name,
                                                                                                 user.user.last_name)
        email_thread = SendEmailThread("nellybaz10@gmail.com", "User verification Request", email_message)

        # Spawn a new thread to run sending email to admin, to reduce the response time for the users
        email_thread.run()

        response = {
            'message': 'Verification has been sent successfully'
        }
        return Response(data=response, status=status.HTTP_200_OK)


# Password change for logged in users
class PasswordChangeView(APIView):
    def put(self, request):
        if not UserProfile.objects.filter(uuid=request.data.get('user'), is_active=True).exists():
            response = {
                'message': 'User does not exists'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        user = UserProfile.objects.get(uuid=request.data.get('user'), is_active=True)
        new_password = request.data.get('password')
        if not new_password:
            response = {
                'message': 'Password is needed'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        user.user.set_password(new_password)
        user.user.save()

        email_message = "Hi \nYou recently changed your password. If this was not you, please call us now. \nThanks"
        email_thread = SendEmailThread(user.user.email, "Password Change Alert", email_message)

        email_thread.run()

        response = {
            'message': 'Password has has been changed successfully'
        }
        return Response(data=response, status=status.HTTP_200_OK)


class ResendVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if UserProfile.objects.filter(user__email=email).exists():
            verification_pin = ''.join(random.sample('0123456789', 5))
            user = UserProfile.objects.get(user__email=email)
            user_verify_object = PinVerify.objects.get(user=user)
            user_verify_object.pin = verification_pin
            user_verify_object.save()
            send_email(
                request.data.get('email'),
                "Bongalo Email Verification",
                "Hi, \nYour pin verification is " +
                verification_pin)

            response = {
                'responseCode': 1,
                'message': 'Verification pin resent to email',
            }
            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            'responseCode': 0,
            'message': 'Email address not registered. Try registering again',
        }
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class UserReviewView(APIView):
    def post(self, request):
        data = {
            'given_by': request.data.get('user'),
            'apartment': request.data.get('apartment'),
            'review': request.data.get('review'),
        }

        serialized = ReviewSerializer(data=data)
        if serialized.is_valid():
            serialized.save()

            response = {
                'responseCode': 1,
                'message': 'apartment review given',
                'data': serialized.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        response = {
            'responseCode': 0,
            'data': serialized.errors,
            'message': 'error occurred saving review'
        }

        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        if not UserProfile.objects.filter(uuid=self.request.query_params.get('user'), is_active=True).exists():
            response = {
                'responseCode': 0,
                'message': 'user does not exists'
            }

            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        user = UserProfile.objects.get(uuid=self.request.query_params.get('user'), is_active=True)
        all_reviews_by_user = Review.objects.filter(given_by=user)
        serialized = ReviewSerializer(all_reviews_by_user, many=True)

        response = {
            'data': serialized.data,
            'message': 'all user reviews retrieved'
        }

        return Response(data=response, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    def post(self, request):
        pin = request.data.get('pin')
        email = request.data.get('email')
        try:
            user = UserProfile.objects.get(user__email=email)
            user_pin = PinVerify.objects.get(user=user)
            user.is_active = True
            user.save()
            if user_pin.pin == pin:
                response = {
                    'responseCode': 1,
                    'data': {
                        'uuid': user.uuid,
                        'email': user.user.email,
                        'first_name': user.user.first_name,
                        'last_name': user.user.last_name,
                        'profile_image': user.profile_image,
                        'phone_number': user.phone,
                        'token': Token.objects.get(user=user.user).key
                    }
                }
                return Response(data=response, status=status.HTTP_200_OK)
            response = {
                'responseCode': 0,
                'data': 'Wrong pin',
                'message': 'Wrong pin'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            response = {
                'responseCode': 0,
                'data': 'Error occurred'
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # check if user is active
            profile = UserProfile.objects.get(user=user)
            if profile.is_active:
                # Get token
                token = Token.objects.get(user=user)
                response_data = {
                    'responseCode': 1,
                    'data': {
                        "first_name": profile.user.first_name,
                        "last_name": profile.user.last_name,
                        "email": profile.user.email,
                        "profile_image": profile.profile_image,
                        "uuid": profile.uuid,
                        "token": token.key}}
                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'responseCode': 0,
                    'data': "user account is not active"
                            'message' "user account is not active"
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {'responseCode': 0, 'data': "login failed", "message": "Email and password do not match"}
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterViews(APIView):
    def post(self, request):  # Handle user registration
        verification_pin = ''.join(random.sample('0123456789', 5))

        serialized = UserRegisterSerializer(
            data=request.data,
            context={
                "request": "post",
                "pin_code": verification_pin},
            partial=True)
        if serialized.is_valid():
            serialized.save()
            send_email(
                request.data.get('email'),
                "Bongalo Email Verification",
                "Hi, \nYour pin verification is " +
                verification_pin)

            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {'responseCode': 0, 'data': serialized.errors, 'message': 'error occurred'}
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SocialAuth(APIView):
    def post(self, request):
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # check if user is active
            profile = UserProfile.objects.get(user=user)
            if profile.is_active:
                # Get token
                token = Token.objects.get(user=user)
                response_data = {
                    'responseCode': 1,
                    'data': {
                        "email": profile.user.username,
                        "first_name": profile.user.first_name,
                        "profile_image": profile.profile_image,
                        "last_name": profile.user.last_name,
                        "uuid": profile.uuid,
                        "token": token.key}}

                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'responseCode': 0,
                    'data': "user does not exists anymore",
                    'message': 'user does not exists anymore'
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        serialized = UserRegisterSerializer(
            data=request.data, context={
                "request": "post"}, partial=True)
        if serialized.is_valid():
            serialized.save()
            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {'responseCode': 0, 'data': serialized.errors, 'message': 'error occurred'}
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserView(APIView):
    permission_classes = [IsOwnerOnly, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user_id = self.request.query_params.get('user')
        if UserProfile.objects.filter(uuid=user_id, is_active=True).exists():
            user = UserProfile.objects.get(uuid=user_id)
            res = {
                'responseCode': 1,
                'data': {
                    "uuid": user.uuid,
                    "first_name": user.user.first_name,
                    "last_name": user.user.last_name,
                    "email": user.user.email,
                    "profile_image": user.profile_image,
                    "phone_number": user.phone,
                    "description": user.description,
                    "token": Token.objects.get(user=user.user).key,

                }
            }
            return Response(data=res, status=status.HTTP_200_OK)

        res = {
            'responseCode': 0,
            'data': 'user does not exists',
            'message': 'user does not exists'
        }
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        is_exists = UserProfile.objects.filter(uuid=request.data.get('user'))
        if is_exists.exists():  # Update data if user exists
            profile = UserProfile.objects.get(uuid=request.data.get('user'))

            # Check if user can update account
            if not check_token_autorization.check_token_authorization(
                    profile, request):
                response_data = {'responseCode': 0,
                                 'data': "This user cannot update this account",
                                 'message': "This user cannot update this account"
                                 }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
            self.check_object_permissions(request, profile)

            country = request.data.get("country")
            city = request.data.get("city")
            user = profile.user
            profile.phone = request.data.get('phone')
            profile.description = request.data.get('description')
            profile.resident_city = city if city else ""
            profile.resident_country = country if country else ""
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')

            profile.save()
            user.save()

            response_data = {
                'responseCode': 1, 'data': {
                    "message": "user profile updated"}}
            return Response(data=response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'responseCode': 0, 'data': {
                    "error": "user does not exists",
                    "message": "user does not exists"
                }}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)


class DeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        is_exists = User.objects.filter(username=request.data.get('username'))
        if is_exists.exists():
            user = User.objects.get(username=request.data.get('username'))
            profile = UserProfile.objects.get(user=user)

            # Check if user can update account
            if not check_token_autorization.check_token_authorization(
                    user, request):
                response_data = {'responseCode': 0,
                                 'data': "This user cannot update this account",
                                 'message': "This user cannot update this account"
                                 }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            if profile.is_active:
                profile.is_active = False
                profile.save()
                response_data = {
                    'responseCode': 1, 'data': {
                        "message": "Deleted successfully"}}
                return Response(
                    data=response_data,
                    status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'responseCode': 0, 'data': {
                        "error": "This User does not exists anymore",
                        "message": "This User does not exists anymore"
                    }}
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = {
                'responseCode': 0, 'data': {
                    "error": "User does not exists",
                    "message": "User does not exists"
                }}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if "national_id" not in request.data and "passport" not in request.data:
            response_data = {'responseCode': 0,
                             'data': "passport or national_id required",
                             'message': "passport or national_id required"
                             }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(username=request.data.get('username')).exists():
            response_data = {'responseCode': 0, 'data': "user does not exits",
                             'message': "user does not exits"
                             }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=request.data.get('username'))
        request.data.pop("username")
        serialized = VerifyUserSerializer(
            UserProfile.objects.get(
                user=user), data=request.data, context={
                "request": "put"}, partial=True)
        if serialized.is_valid():
            serialized.save()
            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {'responseCode': 0, 'data': serialized.errors, 'message': 'Error occurred'}
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProfileImage(APIView):

    def post(self, request):
        user_id = request.data.get('uuid')
        image_url = request.data.get('image')

        if UserProfile.objects.filter(uuid=user_id).exists():
            profile = UserProfile.objects.get(uuid=user_id)
            profile.profile_image = image_url
            profile.save()

            # send_email("nellybaz10@gmail.com", "Update on profile", "Your profile image changed")
            # send_sms("0784650455", "Your profile image changed")
            response = {
                "responseCode": 1,
                "message": "Profile image updated successfully"
            }
            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            "responseCode": 0,
            "message": "User does not exists"
        }
        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentMethod(APIView):

    def get(self, request):
        user_id = self.request.query_params.get('user')
        user = UserProfile.objects.get(uuid=user_id)
        if PaymentMethodModel.objects.filter(user=user).exists():
            number = PaymentMethodModel.objects.get(user=user)

            response = {
                "responseCode": 1,
                "data": number.momo_number
            }
            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            "responseCode": 0,
            "data": "no payment method added",
            "message": "no payment method added"
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user_id = request.data.get('user')
        number = request.data.get('momo_number')

        user = UserProfile.objects.get(uuid=user_id)
        if PaymentMethodModel.objects.filter(user=user).exists():
            payment_method = PaymentMethodModel.objects.get(user=user)
            payment_method.momo_number = number
            payment_method.save()

        else:
            PaymentMethodModel.objects.create(user=user, momo_number=number)
        send_email(
            user.user.email,
            "Bongalo Payment Info Update",
            "Hi {0} \nYour mobile number for receiving "
            "payments on Bongalo has been changed. If this "
            "action was performed by you pls call 0784650455 to "
            "cancel immediately".format(
                user.user.first_name))

        response = {
            "responseCode": 1,
            "data": "Payment method added successfully"
        }
        return Response(data=response, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """
    Receive email address, and send an encrypted link of the user's uuid and email to the email address
    """

    def post(self, request):
        user_email = request.data.get('email')
        if not UserProfile.objects.filter(user__email=user_email, is_active=True).exists():
            response = {
                "responseCode": 0,
                "message": "User with this email does not exits"
            }

            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        user = UserProfile.objects.get(user__email=user_email, is_active=True)
        key = Fernet.generate_key()  # Generate the unique key to encrypt text with
        message_to_encrypt = "uuid={}&email={}".format(user.uuid, user_email).encode()
        f_encrypt = Fernet(key)  # Initialize the encrypt object
        encrypted_message = f_encrypt.encrypt(message_to_encrypt)  # Encrypt the message

        #  Generate the reset link to be sent
        reset_password_link = "http://localhost:8080/reset-password?token=" + encrypted_message.decode() + "&email=" + user_email
        print(reset_password_link)
        send_email(
            user_email,
            "Password Reset",
            "Hi {} \nFollow this link {} to reset your password".format(user.user.first_name, reset_password_link))

        PasswordReset.objects.create(
            user=user,
            is_used=False,
            reset_key=key.decode()
        )
        response = {
            'responseCode': 1,
            'message': 'Email sent, check your email for a link to reset your password'
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def put(self, request):
        user_email = request.data.get('email')
        if not UserProfile.objects.filter(user__email=user_email, is_active=True).exists():
            response = {
                "responseCode": 0,
                "message": "User with this email does not exits"
            }

            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        user = UserProfile.objects.get(user__email=user_email, is_active=True)
        token = request.data.get('token').encode()

        # If the link is already used
        if not PasswordReset.objects.filter(user__user__email=user_email, is_used=False).order_by(
                'created_at').exists():
            response = {
                'responseCode': 0,
                'message': 'Link invalid, please request to reset password again'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        password_reset_object = PasswordReset.objects.filter(user__user__email=user_email, is_used=False).order_by(
            'created_at').first()

        reset_key = password_reset_object.reset_key
        f_encrypt = Fernet(reset_key.encode())  # Initialize the encrypt object
        try:
            decrypted_message = f_encrypt.decrypt(token)
        except BaseException:
            response = {
                'responseCode': 0,
                'message': 'Invalid link/token please make another request to reset password'
            }

            return Response(data=response, status=status.HTTP_200_OK)

        if decrypted_message.decode() == "uuid={}&email={}".format(user.uuid, user.user.email):
            user.user.set_password(request.data.get('password'))
            user.user.save()

            #  Update the password reset object to used
            password_reset_object.is_used = True
            password_reset_object.save()

            response = {
                'responseCode': 1,
                'message': 'Password reset successfully'
            }

            return Response(data=response, status=status.HTTP_200_OK)

        response = {
            'responseCode': 0,
            'message': 'Password reset failed'
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
