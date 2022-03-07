from django.urls import include, path
from rest_framework_nested import routers

from panderyx.tools.views import ToolViewSet
from panderyx.workflows.views import WorkflowViewSet

router = routers.SimpleRouter()
router.register(r"workflows", WorkflowViewSet)

tools_router = routers.NestedSimpleRouter(router, r"workflows", lookup="workflow")
tools_router.register(r"tools", ToolViewSet, basename="workflow-tools")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(tools_router.urls)),
]
