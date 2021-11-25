from .models import Todo
from .serializers import TodoSerializer, FutureSerializer
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema # for coreapi
from django.utils import timezone

# for authentication
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Create your views here.

# todolist
# for coreapi; doesn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['POST'], request_body=TodoSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def todolist(request):
    if request.method == 'GET':
        objs = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(objs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer =  TodoSerializer(data=request.data)
        if serializer.is_valid():
            
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')
                
            object = Todo.objects.create(**serializer.validated_data, user=request.user)
            serializer = TodoSerializer(object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# todo detail
# for coreapi; doesn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=TodoSerializer()) 
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, todo_id):
    """
        Takes in a todo_id and returns the http response depending on the http method

        Args:
        todo_id: Interger

        Allowed method
        GET - get the detail of a single todo
        PUT - Allows you to edit the todo detail
        DELETE - This logic deletes the todo record from the data base
    """

    try:# get the data from the model
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        error = {
            "message": "failed",
            "errors": f"Student with id {todo_id} does not exist"
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        data = { # prepare response data
            "status": True,
            "message": "success",
            "data": serializer.data
        } 
        # send the response
        return Response(data, status=status.HTTP_200_OK) 

    # update TODO
    elif request.method == "PUT":
        # partial allows for patch updates as well
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            data = {
                "status": True,
                "message": "success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)

        else:
            error = {
                "status": False,
                "message": "failed",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    # delete TODO
    elif request.method == 'DELETE':
        todo.delete()
        context = {
            "status": True,
            "message":"deleted"
            }
        return Response(context, status=status.HTTP_200_OK)


# list to_do for today
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_today(request):
    if request.method == 'GET':
        # getting values for a field in django model
        today = timezone.now().date()
        objects = Todo.objects.filter(day=today, user=request.user)
        serializer = TodoSerializer(objects, many=True)

        data = {
            "status": True,
            "message": "success",
            "data": serializer.data
            }
        return Response(data, status=status.HTTP_200_OK)


# list future to_do
@swagger_auto_schema(method='post', request_body=FutureSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def list_future(request):
    if request.method == 'POST':
        serializer = FutureSerializer(data=request.data)

        if serializer.is_valid():
            objects = Todo.objects.filter(day=serializer.validated_data['day'], user=request.user)
            serializer = TodoSerializer(objects, many=True)
            data = {
                "status"  : True,
                "message" : "successful",
                "data" : serializer.data,
            }
            return Response(data, status = status.HTTP_200_OK)

        else:
            error = {
                "status"  : False,
                "message" : "failed",
                "error" : serializer.errors,
            }
            return Response(error, status = status.HTTP_200_OK)



# mark to_do complete
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def mark_complete(request, todo_id):
   
    try:
        obj = Todo.objects.get(id=todo_id)
    
    except Todo.DoesNotExist:
        data = {
            "status"  : False,
            "message" : "Does not exist"
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if obj.user != request.user:
        raise PermissionDenied(detail='You do not have permission to perform this action')
    
    
    if request.method == 'GET':
        if obj.completed == False:
            obj.completed=True
            obj.save()
                  
            data = {
                "status"  : True,
                "message" : "Successful"
            }
            return Response(data, status=status.HTTP_200_OK)

        else:   
            data = {
                    "status"  : False,
                    "message" : "Already marked complete"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)