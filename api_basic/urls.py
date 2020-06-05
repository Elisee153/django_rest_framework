from django.urls import path,include
#views
from .views import article_list,article_detail,ArticleAPIView,ArticleDetailAPIView,GenericAPIView,ArticleViewSet,ArticleGenericViewSet,ArticleModalViewSet
#router
from rest_framework.routers import DefaultRouter
#===============================================

router = DefaultRouter()
router.register('article',ArticleModalViewSet, basename = 'article')

urlpatterns = [    
    path('model_viewset/', include(router.urls)),
    path('model_viewset/<int:pk>/', include(router.urls)),
    path('generic_viewset/', include(router.urls)),
    path('generic_viewset/<int:pk>/', include(router.urls)),
    #path('article/',article_list),
    path('article/',ArticleAPIView.as_view()),
    #path('detail/<int:pk>/',article_detail),
    path('detail/<int:id>/',ArticleDetailAPIView.as_view()),
    path('generic/article/', GenericAPIView.as_view()),
    path('generic/article/<int:id>/',GenericAPIView.as_view())
]