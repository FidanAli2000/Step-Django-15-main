from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CategoryViewSet, TagViewSet

app_name = "api"

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("categories", CategoryViewSet)
router.register("tags", TagViewSet)

urlpatterns = router.urls
