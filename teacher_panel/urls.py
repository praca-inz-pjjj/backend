from django.urls import path

from teacher_panel.other_views.download_parent_list import DownloadParentList
from teacher_panel.other_views.get_children_of_receiver import GetChildrenOfReceiverView
from teacher_panel.other_views.get_receivers import GetReceiversView


from .other_views.accept_receipt import AcceptReceiptView
from . import views
from .other_views.child_parents import ChildParentsView
from .views import ObtainTeacherTokenPairView
from .other_views.create_parent import CreateParent
from .other_views.create_children import create_children

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
    path('children/<int:id>', GetChildrenOfReceiverView.as_view()),
    path('child/<int:child_id>/receiver/<int:receiver_id>/signature-delivery', views.update_receiver_signature, name='update_receiver_signature'),
]