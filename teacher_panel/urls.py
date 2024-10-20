from django.urls import path


from .use_cases.acceptReceipt import AcceptReceiptView
from . import views
from .use_cases.childParents import ChildParentsView
from .views import ObtainTeacherTokenPairView
from .use_cases.createParent import CreateParent

urlpatterns = [
    path("", views.teacher_data),
    path("token",ObtainTeacherTokenPairView.as_view() , name="token_obtain_pair"),
    path("class/<int:id>", views.class_data),
    path('class/create', views.create_classroom, name='create_classroom'),
    path('class/<int:id>/create', views.create_child, name='create_child'),
    path('child/<int:id>', ChildParentsView.as_view()),
    path('receipt', AcceptReceiptView.as_view()),
    path('create-parent', CreateParent.as_view())
]