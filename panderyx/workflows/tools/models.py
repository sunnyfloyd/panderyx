import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from panderyx.workflows.models import Workflow


class Tool(models.Model):
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, related_name="tools"
    )
    name = models.CharField(max_length=100, verbose_name=_("tool name"), null=True)
    x = models.IntegerField(
        verbose_name=_("x coordinate"), validators=[MinValueValidator(0)], default=100
    )
    y = models.IntegerField(
        verbose_name=_("y coordinate"), validators=[MinValueValidator(0)], default=100
    )
    inputs = models.ManyToManyField(
        "self", symmetrical=False, related_name="outputs", blank=True
    )
    config = models.JSONField()

    class Meta:
        ordering = ["workflow", "name"]
        unique_together = [["workflow", "name"]]

    def __str__(self) -> str:
        return f"{self.get_name()} in {self.workflow.name}"

    def get_name(self):
        return self.name or f"Tool ({self.id})"
