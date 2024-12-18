from django.urls import path

from teacher_panel.use_cases.downloadParentList import DownloadParentList
from teacher_panel.use_cases.getChildrenOfReceiver import GetChildrenOfReceiverView
from teacher_panel.use_cases.getReceivers import GetReceiversView


from .use_cases.acceptReceipt import AcceptReceiptView
from . import views
from .use_cases.childParents import ChildParentsView
from .views import ObtainTeacherTokenPairView
from .use_cases.createParent import CreateParent
from .use_cases.createChildren import create_children

urlpatterns = [
    path("", views.teacher_data),
    path("token",ObtainTeacherTokenPairView.as_view() , name="token_obtain_pair"),
    path("class/<int:id>", views.class_data),
    path('class/create', views.create_classroom, name='create_classroom'),
    path('class/<int:id>/child', views.create_child, name='create_child'),
    path('class/<int:id>/children', create_children, name='create_children'),
    path('child/<int:id>', ChildParentsView.as_view()),
    path('check-receipt', views.check_receipt, name='check_receipt'),
    path('check-twofactorcode', views.check_two_factor_code, name='check_two_factor_code'),
    path('receipt', AcceptReceiptView.as_view()),
    path('create-parent', CreateParent.as_view()),
    path('class/<int:id>/download', DownloadParentList.as_view()),
    path('receivers', GetReceiversView.as_view()),
    path('children/<int:id>', GetChildrenOfReceiverView.as_view())
]