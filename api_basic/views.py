from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
#api_view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#class based api view
from rest_framework.views import APIView


# Creation de view basé sur les fonctions.

#@ csrf_exempt
@api_view(['GET','POST'])
def article_list(request):
    #Verification du type de la requete
    if request.method == 'GET':
        #recuperation des donnee
        articles = Article.objects.all()
        #serialization
        serializer = ArticleSerializer(articles,many=True)
        #without api_view => return JsonResponse(serializer.data, safe = False)
        #with api_view 
        return Response(serializer.data)
    
    elif request.method == 'POST':
        #without api_view => data = JSONParser().parse(request)
        #with api_view decorator we dont need to parse the request        
        serializer = ArticleSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            #without api_view
           # return JsonResponse(serializer.data, status = 201)
        #return JsonResponse(serializer.errors,status = 400)
        #with api_view
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        

#detail article
#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk = pk)
    
    except Article.DoesNotExist:
        return HttpResponse(status = status.HTTP_404_NOT_FOUND)
    
    #read
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        #WITHOUT API_VIEW()
        #return JsonResponse(serializer.data)
        #with api_view
        return Response(serializer.data)
    
    #update
    elif request.method == 'PUT':
        # without api_view => data = JSONParser().parse(request)
        #on modifie l'article recupere
        #with api_view
        serializer = ArticleSerializer(article,data = request.data)
        if serializer.is_valid():
            serializer.save()
            #without api_view
        #     return JsonResponse(serializer.data)
        # return JsonResponse(serializer.errors,status=400)
            return Response(serializer.data)
        return  Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    #delete
    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

#Creation des views basésur les classes

class ArticleAPIView(APIView):
    #read
    def get(self, request):
        articles = Article.objects.all()        
        serializer = ArticleSerializer(articles,many=True)        
        return Response(serializer.data)
    
    #create
    def post(self,request):
        serializer = ArticleSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
     
    
    

     