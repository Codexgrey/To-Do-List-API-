from .serializers import CustomUserSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# for password/user authentication
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

User = get_user_model()

# checking password
def password_isvalid(password):
    #password logic
    if (len(password) < 6) or (len(password) > 12):
        isValid = False
    elif not any(char.isdigit() for char in password): 
        isValid = False
    elif not any(char.islower() for char in password):
        isValid = False
    elif not any(char.isupper() for char in password):
        isValid = False
    else:
        isValid = True

    return isValid


# Create your views here.
# for coreapi; deosn't need 'GET' because it has no request.body
# user account get and post methods split
# add user - POST
@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer())
@api_view(['POST'])
def add_user(request):
    """ Allows the user to be able to sign up on the platform """
    if request.method == 'POST':
        serializer = CustomUserSerializer(data = request.data)
        if serializer.is_valid():
            # checking password
            password = serializer.validated_data['password']

            if password_isvalid(password):
                # hashing password
                password = make_password(password)

                # validated new user is created, unpacked and serialized
                user = User.objects.create(**serializer.validated_data)      
                user_serializer = CustomUserSerializer(user)

                # new user sent as data
                data = {
                    "status": True,
                    "message": "success",
                    "data": user_serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)

            else:
                error = {
                    "message": "failed",
                    "errors": [
                        "Password length should be at least 6 and not more than 8", 
                        "Password must have lower and uppercase alphabets as well as number(s)"
                    ]
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

        else:
            error = {
                "status": False,
                "message": "unsuccessful",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


# get user - GET (with admin priviledges only) 
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
@api_view(['GET'])
def get_user(request):
    """Allows the admin to see all users (both admin and normal users) """
    if request.method == 'GET':
        user = User.objects.filter(is_active=True)

        serializer = CustomUserSerializer(user, many =True)
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }
        return Response(data, status=status.HTTP_200_OK)



# login view
@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view(['POST'])
def user_login(request):
    
    """
    Allows users to log in to the platform. 
    Sends the jwt refresh and access tokens. 
    Check settings for token life time.
    """
    
    if request.method=='POST':
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        
        if user is not None:
            if user.is_active==True:
                try:
                    user_detail = {}
                    user_detail['id'] = user.id
                    user_detail['first_name'] = user.first_name
                    user_detail['last_name'] = user.last_name
                    user_detail['email'] = user.email
                    user_detail['username'] = user.username
                    
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                        'status'  : True,
                        'message' : 'Successful',
                        'data' : user_detail
                    }
                    return Response(data, status=status.HTTP_200_OK)
                
                except Exception as e: 
                    raise e

            else:
                data = {
                    'status': False,
                    'error': 'This account has not been activated'
                }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        else:
            data = {
                'status': False,
                'error': 'Please provide a valid username and a password'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)



# user profile - get the detail of a single user by their ID
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=CustomUserSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def profile(request):
    """
    Allows the logged in user to view their profile, 
    edit or deactivate account. 
    Do not use this view for changing password or resetting password
    """
    
    try:
        user = User.objects.get(id=request.user.id, is_active=True)
    
    except User.DoesNotExist:
        data = {
                "status"  : False,
                "message" : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        
        data = {
                "status"  : True,
                "message" : "Successful",
                "data" : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    # update the profile of the user
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data = request.data, partial=True) 

        if serializer.is_valid():
            if "password" in serializer.validated_data:
                raise ValidationError(detail="Cannot change password with this view")
            
            serializer.save()

            data = {
                "status" : True,
                "message": "Successful",
                "data": serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                "status"  : False,
                "message" : "Unsuccessful",
                "error" : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    # delete the account by changing `is.active to False`
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
                "status"  : True,
                "message" : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_200_OK)



# user detail for admin
@swagger_auto_schema(methods=['DELETE'], request_body=CustomUserSerializer()) 
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
@api_view(['GET', 'DELETE'])
def user_detail(request, user_id):
    """
        Takes in a user_id and returns the http response depending on the http method
        Args:
        user_id: Interger
        Allowed method
        GET - get the detail of a single user
        PUT - Allows you to edit the user detail
        DELETE - This logic deletes the user record from the data base
    """

    try:# get the data from the model
        user = User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        error = {
            "status": False,
            "message": f"Custom User with id {user_id} does not exist"
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        data = { 
            # prepare response data
            "status": True,
            "message": "Successful",
            "data": serializer.data
        } 
        # send the response
        return Response(data, status=status.HTTP_200_OK) 

    # delete the user
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
            "status": True,
            "message":"Deleted Successfully"
            }
        return Response(data, status=status.HTTP_200_OK)



# change/reset password
# for coreapi; deosn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['POST'], request_body=ResetPasswordSerializer()) 
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        # getting logged in user
        user = request.user
        # serializing POST request data
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid:
            old_password = serializer.validated_data['old_password']

            if check_password(old_password, user.password):
                # using AbstractedUser method `set_password` to set new_password
                user.set_password(serializer.validated_data['new_password'])
                user.save()

                data = {
                    "status": True,
                    "message":"Password Change Successful"
                    }
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                error = {
                    "status": False,
                    "message": "Old password not correct"
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            error = {
                "status": "False",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)