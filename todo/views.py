from .models import Person, Todo
from .serializers import PersonSerializer, TodoSerializer
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema # for coreapi


# Create your views here.

# persons
# for coreapi; deosn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['POST'], request_body=PersonSerializer()) 
@api_view(['GET', 'POST'])
def persons(request):
    if request.method == 'GET':
        # getting all persons data and serializing it
        all_persons = Person.objects.all()
        serializer = PersonSerializer(all_persons, many=True)

        # parsing data into dict for response
        data = {
            "message": "success",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # get and deserialize data
        serializer = PersonSerializer(data=request.data) # get and serialize

        # validating data and saving if valid, else = error
        if serializer.is_valid():
            serializer.save()

            data = {
                "message": "success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            error = {
                "message": "failed",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


# person detail
# for coreapi; doesn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=PersonSerializer()) 
@api_view(['GET', 'PUT', 'DELETE'])
def person_detail(request, person_id):
    """
        Takes in a person_id and returns the http response depending on the http method

        Args:
        person_id: Interger

        Allowed method
        GET - get the detail of a single person
        PUT - Allows you to edit the person detail
        DELETE - This logic deletes the person record from the data base
    """

    try:# get the data from the model
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        error = {
            "message": "failed",
            "errors": f"Student with id {person_id} does not exist"
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PersonSerializer(person)
        data = { # prepare response data
            "message": "success",
            "data": serializer.data
        } 
        # send the response
        return Response(data, status=status.HTTP_200_OK) 

    elif request.method == "PUT":
        # partial allows for patch updates as well
        serializer = PersonSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
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
        person.delete()
        context = {"message":"success"}
        return Response(context, status=status.HTTP_204_NO_CONTENT)



# todolist
# for coreapi; doesn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['POST'], request_body=TodoSerializer()) 
@api_view(['GET', 'POST'])
def todolist(request):
    if request.method == 'GET':
        # getting all todo data and serializing it
        all_todo = Todo.objects.all()
        serializer = TodoSerializer(all_todo, many=True)

        # parsing data into dict for response
        data = {
            "message": "success",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # get and deserialize data
        serializer = TodoSerializer(data=request.data)

        # validating data and saving if valid, else = error
        if serializer.is_valid():
            serializer.save()

            data = {
                "message": "success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            error = {
                "message": "failed",
                "errors": serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


# todo detail
# for coreapi; doesn't need 'GET' because it has no request.body
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=TodoSerializer()) 
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
            "message": "success",
            "data": serializer.data
        } 
        # send the response
        return Response(data, status=status.HTTP_200_OK) 

    elif request.method == "PUT":
        # partial allows for patch updates as well
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
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
        todo.delete()
        context = {"message":"success"}
        return Response(context, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_today(request):
    if request.method == 'GET':
        # getting values for a field in django model
        thisday = Person.objects.values_list('today', flat=True)
        data = {today:{
            "count": Person.objects.filter(today=today).count(),
            "data": Person.objects.filter(today=today).values()
            } for today in thisday}
        print(thisday)

        context = {"message": "success", "data": data} 
        return Response(context, status=status.HTTP_200_OK)

