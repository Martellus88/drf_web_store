from rest_framework.routers import SimpleRouter

from .views import OrderAPIView

router = SimpleRouter()
router.register(r'order', OrderAPIView, basename='order')


urlpatterns = [] + router.urls