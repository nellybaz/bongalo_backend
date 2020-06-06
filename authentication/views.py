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
from .models import UserProfile, PaymentMethod as PaymentMethodModel, PinVerify, PasswordReset, UserSubscribe as UserSubscribeModel
from apartment.models import Review, Apartment
from apartment.serializers import ReviewSerializer
from .serializers import UserRegisterSerializer, VerifyUserSerializer
from bongalo_backend.settings import PINDO_API_TOKEN
from cryptography.fernet import Fernet
from utils.email_thread import SendEmailThread, EmailService


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
    permission_classes = [IsOwnerOnly, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def put(self, request):
        if not UserProfile.objects.filter(user=request.user, is_active=True).exists():
            response = {
                'message': 'User does not exists'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        user = UserProfile.objects.get(user=request.user, is_active=True)
        new_password = request.data.get('password')
        old_password = request.data.get('old_password')
        if not new_password:
            response = {
                "responseCode": 0,
                'message': 'Password is needed'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # if not user.user.check_password(old_password):
        #     response = {
        #         "reponseCode":0,
        #         'message': 'Wrong old password'
        #     }
        #     return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        user.user.set_password(new_password)
        user.user.save()

        try:
            email_service = EmailService(user.user.email)
            payload = {
                'lastName': user.user.last_name,
            }
            email_thread = SendEmailThread(email_service.password_change, payload=payload)
            email_thread.run()
        except BaseException as e:
            print(str(e))

        response = {
            "responseCode": 1,
            'message': 'Password has been changed successfully'
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
            try:
                email_service = EmailService(email)
                payload = {
                    'recipient_last_name': user.user.last_name,
                    'verification_pin': verification_pin
                }
                email_thread = SendEmailThread(email_service.send_registration_pin, payload=payload)
                email_thread.run()
            except BaseException as e:
                response_data = {'responseCode': 0,
                                 'data': [],
                                 'message': 'Could not send registration token please try again ' + str(e)}
                return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

            try:
                email_service = EmailService(email)
                payload = {
                    'recipient_name': user.user.last_name,
                }
                email_thread = SendEmailThread(email_service.send_welcome, payload=payload)
                email_thread.run()
            except BaseException as err:
                print(str(err))

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
        except BaseException as err:
            print(str(err))
            response = {
                'responseCode': 0,
                'data': 'Error occurred'
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not UserProfile.objects.filter(user__email=username).exists():
            response_data = {
                             'responseCode': 0,
                             'data': "login failed",
                             "message": "Email address not found. Please register"
                            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

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
                    'data': "user account is not active",
                    'message': "user account is not active"
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {'responseCode': 0, 'data': "login failed", "message": "Email and password do not match"}
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterViews(APIView):
    def post(self, request):  # Handle user registration
        verification_pin = ''.join(random.sample('0123456789', 5))

        if UserProfile.objects.filter(user__email=request.data.get("email")).exists():
            response_data = {'responseCode': 0, 'data': [],
                             'message': 'Email address already registered. Please login'}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        serialized = UserRegisterSerializer(
            data=request.data,
            context={
                "request": "post",
                "pin_code": verification_pin},
            partial=True)

        try:
            email_service = EmailService(request.data.get("email"))
            payload = {
                'recipient_last_name': request.data.get('last_name'),
                'verification_pin': verification_pin
            }
            email_thread = SendEmailThread(email_service.send_registration_pin, payload=payload)
            email_thread.run()
        except BaseException as e:
            response_data = {'responseCode': 0,
                             'data': [],
                             'message': 'Could not send registration token please try again '+str(e)}
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if serialized.is_valid():
            serialized.save()

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
            try:
                email_service = EmailService(request.data.get('email'))
                payload = {
                    'recipient_name': request.data.get('last_name'),
                }
                email_thread = SendEmailThread(email_service.send_welcome, payload=payload)
                email_thread.run()
            except BaseException as err:
                print(str(err))

            response_data = {'responseCode': 1, 'data': serialized.data}
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {'responseCode': 0, 'data': serialized.errors, 'message': 'error occurred'}
        return Response(data=respvonse_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserView(APIView):
    permission_classes = [IsOwnerOnly, IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user_id = self.request.query_params.get('user')
        if UserProfile.objects.filter(uuid=user_id, is_active=True).exists():
            user = UserProfile.objects.get(uuid=user_id)
            payment_details = None
            if PaymentMethodModel.objects.filter(user=user).exists():
                payment_details = PaymentMethodModel.objects.get(user=user) 

            data = {
                    "uuid": user.uuid,
                    "first_name": user.user.first_name,
                    "last_name": user.user.last_name,
                    "email": user.user.email,
                    "profile_image": user.profile_image,
                    "phone_number": user.phone,
                    "description": user.description,
                    "city":user.resident_city,
                    "country": user.resident_country,
                    "joined": user.created_at,
                    "token": Token.objects.get(user=user.user).key,
                    "verification_status": user.verification_status,
                    "bank_name": payment_details.bank_name if payment_details else "",
                    "account_name": payment_details.account_name if payment_details else "",
                    "account_number": payment_details.account_number if payment_details else "",
                    "swift_code": payment_details.swift_code if payment_details else "",
                    "momo_number": payment_details.momo_number if payment_details else "",
                    "momo_name": payment_details.momo_name if payment_details else "",
                }


            res = {
                'responseCode': 1,
                'data': data
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

        print(request.user)
        if not request.user:
            response_data = {'responseCode': 0, 'data': "user does not exits",
                             'message': "user does not exits"
                             }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
        payment_data = {
            'momo_number':request.data.get('momo_number'),
            'momo_name': request.data.get('momo_name'),
            'bank_name': request.data.get('bank_name'),
            'account_name': request.data.get('account_name'),
            'account_number': request.data.get('account_number'),
            'swift_code': request.data.get('swift_code'),
        }

        if not request.user:
            response = {
            "responseCode": 0,
            "data": "User does not exist"
        }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        user = UserProfile.objects.get(user=request.user)
        if PaymentMethodModel.objects.filter(user=user).exists():
            payment_method = PaymentMethodModel.objects.get(user=user)
            payment_method.momo_number = payment_data['momo_number']
            payment_method.momo_name = payment_data['momo_name']
            payment_method.bank_name = payment_data['bank_name']
            payment_method.account_name = payment_data['account_name']
            payment_method.account_number = payment_data['account_number']
            payment_method.swift_code = payment_data['swift_code']
            payment_method.save()

        else:
            PaymentMethodModel.objects.create(user=user, **payment_data)
            # send_email(
            #     user.user.email,
            #     "Bongalo Payment Info Update",
            #     "Hi {0} \nYour mobile number for receiving "
            #     "payments on Bongalo has been changed. If this "
            #     "action was performed by you pls call 0784650455 to "
            #     "cancel immediately".format(
            #         user.user.first_name))

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
        try:
            email_message = "Hi {} \nFollow this link {} to reset your password".format(user.user.first_name, reset_password_link)

            email_thread = SendEmailThread(user_email, "Bongalo Password Reset", email_message)

            # Spawn a new thread to run sending email, to reduce the response time for the users
            email_thread.run()
        except:
            response = {
                "responseCode": 0,
                "message": "Could not send password reset link to your email. Please try again"
            }

            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class UserSubscribe(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            response = {
                "responseCode": 0,
                "message": "Email is required",
                "data": "",
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        if UserSubscribeModel.objects.filter(email=email).exists():
            response = {
                "responseCode": 0,
                "message": "Email already subscribed. But thanks for subscribing",
                "data": "",
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        UserSubscribeModel.objects.create(email=email)

        try:
            email_service = EmailService(email)
            payload = {
                # 'recipient_name': request.data.get('last_name'),
            }
            email_thread = SendEmailThread(email_service.newsletter_subscription, payload=payload)
            email_thread.run()
        except BaseException as err:
            print(str(err))

        response = {
            "responseCode": 1,
            "message": "Thanks for subscribing",
            "data": "",
        }
        return Response(data=response, status=status.HTTP_200_OK)
