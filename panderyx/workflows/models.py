import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from panderyx.users.models import User


class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_("workflow name"))
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date of creation")
    )
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_("last update"))

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.name} workflow owned by {self.user.username}"
