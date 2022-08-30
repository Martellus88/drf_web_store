from rest_framework.routers import SimpleRouter

from .views import ProductAPIView, CategoryAPIView

router = SimpleRouter()
router.register(r'products', ProductAPIView)
router.register(r'category', CategoryAPIView)

urlpatterns = [] + router.urls
