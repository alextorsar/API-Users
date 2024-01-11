from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .userViews import RegisterView, LoginView, UserView, LogOutView
from .ModelManagment.modelViews import ModelView
from .SubModelManagment.submodelViews import SubModelView
from .ModelManagment.modelExecutionViews import ModelDocumentationView, ModelExecutionView

urlpatterns = [
    path('model/<int:modelId>/run/', ModelExecutionView.as_view()),
    path('model/<int:modelId>/documentation/', ModelDocumentationView.as_view()),
    path('model/<int:modelId>/', ModelView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('model/', ModelView.as_view()),
    path('submodel/', SubModelView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
