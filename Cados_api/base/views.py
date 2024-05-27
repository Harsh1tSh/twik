from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status

from .models import Advocate, Company
from .serializers import AdvocateSeriaizer, CompanySerializer

# Create your views here.
@api_view(["GET"])
def endpoints(request):
    data = ['/advocates','advocates/:username']
    return Response(data)


@api_view(["GET", "POST"])
def advocates_list(request):
    if request.method == 'GET':
        query = request.GET.get('query')

        if query == None:
            query = ''

        advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serialiser = AdvocateSeriaizer(advocates, many=True)
        return Response(serialiser.data)
    
    if request.method == 'POST':
        advocate = Advocate.objects.create(
            username = request.data['username'],
            bio = request.data['bio']
        )
        serialiser = AdvocateSeriaizer(advocate, many=False)
        return Response(serialiser.data)


class AdvocateDetail(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise Http404("Advocate doesn't exist.")

    def get(self, request, username):
        advocate = self.get_object(username)
        serializer = AdvocateSeriaizer(advocate, many=False)
        return Response(serializer.data)

    def put(self, request, username):
        advocate = self.get_object(username)
        serializer = AdvocateSeriaizer(advocate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username):
        advocate = self.get_object(username)
        advocate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        



# @api_view(["GET","PUT","DELETE"])
# def advocate_detail(request, username):
#     advocate = get_object_or_404(Advocate, username__iexact=username)
#     if request.method == "GET":
#         serializer = AdvocateSeriaizer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method == "PUT":
#         advocate.username = request.data['username']
#         advocate.bio = request.data['bio']
#         advocate.save()
#         serializer = AdvocateSeriaizer(advocate, many=False)
#         return Response(serializer.data)
    

#     if request.method == "DELETE":
#         advocate.delete()
#         return Response("User was deleted")

@api_view(["GET"])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)
