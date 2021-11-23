from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, ChangePasswordSerializer
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from drf_yasg.utils import swagger_auto_schema
# for password authentication
authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

# CustomUser
# for coreapi; deosn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer()) 
@api_view(['GET', 'POST'])
def user_accounts(request):
    if request.method == 'GET':
        # getting all students data and serializing it
        # all_Users = CustomUser.objects.all()
        all_Users = CustomUser.objects.filter(is_active=True)
        serializer = CustomUserSerializer(all_Users, many=True)

        # parsing data into dict for response
        data = {
            "message": "success",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # get and deserialize data
        serializer = CustomUserSerializer(data=request.data)

        # validating data and saving if valid, else = error
        if serializer.is_valid():
            # hashing password
            serializer.validated_data['password'] = make_password(
                serializer.validated_data['password']
            )

            # validated new user is created, unpacked and serialized
            user = CustomUser.objects.create(**serializer.validated_data)            
            user_serializer = CustomUserSerializer(user)

            # new user sent as data
            data = {
                "message": "success",
                "data": user_serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            error = {
                "message": "failed",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=CustomUserSerializer()) 
@api_view(['GET', 'PUT', 'DELETE'])
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
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        error = {
            "message": "failed",
            "errors": f"Custom User with id {user_id} does not exist"
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        data = { # prepare response data
            "message": "success",
            "data": serializer.data
        } 
        # send the response
        return Response(data, status=status.HTTP_200_OK) 

    elif request.method == "PUT":
        # partial allows for patch updates as well
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Best Practice;
            # if 'password' in serializer.validated_data.keys():
            #   raise ValidationError("Unable to change password")
            #
            if "password" in serializer.validated_data:
                error = {
                    "message": "failed",
                    "errors": serializer.errors
                }
                return Response(error, status=status.HTTP_403_FORBIDDEN)
            
            else:
                serializer.save()

                data = {
                    "message": "success",
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_202_ACCEPTED)

        else:
            error = {
                "message": "failed",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        context = {"message":"success"}
        return Response(context, status=status.HTTP_204_NO_CONTENT)


# change password
# for coreapi; deosn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer()) 
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        # getting logged in user
        user = request.user
        # serializing POST request data
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid and serializer.validate_password():
            old_password = serializer.validated_data['old_password']

            if check_password(old_password, user.password):
                # using AbstractedUser method `set_password` to set new_password
                user.set_password(serializer.validated_data['new_password'])
                user.save()

                context = {"message": "success"}
                return Response(context, status=status.HTTP_204_NO_CONTENT)
            
            else:
                error = {
                    "message": "failed",
                    "error": "Old pssword not correct"
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            error = {
                "message": "failed",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)