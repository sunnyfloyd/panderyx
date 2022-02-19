from django.urls import path
from rest_framework.routers import DefaultRouter

from panderyx.workflows.views import WorkflowViewSet

router = DefaultRouter()
router.register(r"workflows", WorkflowViewSet)
