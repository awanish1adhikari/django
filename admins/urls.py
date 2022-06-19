from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.admin_dashboard),

    path('products', views.product),
    path('deleteProduct/<int:p_id>', views.delete_product),
    path('updateProduct/<int:p_id>', views.update_product),

    path('order', views.order),
    path('deleteOrder/<int:o_id>', views.delete_order),

    path('user', views.get_user),
    path('update-user-to-admin/<int:user_id>', views.update_user_to_admin),

    path('register/', views.register_user_admin),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)
