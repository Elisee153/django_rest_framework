from django.shortcuts import render, get_object_or_404
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
#generics and mixins=====================
from rest_framework import generics
from rest_framework import mixins
#========================================
#Authentification
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
#ViewSet and Router
from rest_framework import viewsets
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
    
    #create=> On serialize les donnees de la requete on les enregistre et on retourne le status
    def post(self,request):
        serializer = ArticleSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
     

class ArticleDetailAPIView(APIView):
    #request de recuperation
    def get_object(self, id):
        try:
            return Article.objects.get(id = id)
    
        except Article.DoesNotExist:
            return HttpResponse(status = status.HTTP_404_NOT_FOUND)
    # on recupere l'objet precis, on le serialize et on le retourne
    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    #PUT
    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    #DELETE
    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


#Creation des views generics

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin):
    
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()    
    lookup_field = "id"
    #authentification
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    # """
    # def get(self, request):
    # return self.list(request)
    # """
    def get(self, request, id = None):
        
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
            
    def post(self,request):
        return self.create(request)
     
    def put(self,request, id=None): 
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

#creation des viewsets

class ArticleViewSet(viewsets.ViewSet):
    
    def list(self, request): 
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = ArticleSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            Response(serializer.data,status = status.HTTP_201_CREATED)
        Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
     
    def retrieve(self,request,pk = None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset,pk = pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data) 
    
    def update(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
#Generic viewSet

class ArticleGenericViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.CreateModelMixin, mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    
#Model viewset

class ArticleModalViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    