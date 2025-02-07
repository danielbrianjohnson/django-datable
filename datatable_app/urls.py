from django.urls import path
from .views import index, dynamic_data, get_model_fields  # Import views

urlpatterns = [
    path('', index, name='index'),
    path('api/data/', dynamic_data, name='dynamic_data'),
    path('api/get-model-fields/', get_model_fields, name='get_model_fields'),  # 🔹 Add this line!
]
