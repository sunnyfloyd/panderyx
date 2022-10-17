from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Set

from django.db import models
from django.utils.translation import gettext_lazy as _

from panderyx.users.models import User

if TYPE_CHECKING:
    from panderyx.workflows.tools.models import Tool


class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workflows")
    name = models.CharField(max_length=100, verbose_name=_("workflow name"))
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("date of creation")
    )
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_("last update"))

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.name} workflow owned by {self.user.username}"

    @property
    def tool_execution_order(self) -> List[Tool]:
        """List of Tool objects that defines their execution order inside a Workflow.

        Raises:
            ValueError: catches case in which Workflow does not contain any input-like Tools

        Returns:
            List[Tool]: list of Tool objects that defines their execution order
        """
        tool_qs = self.tools.prefetch_related("inputs")
        starting_tools = list(tool_qs.filter(inputs=None))

        if not starting_tools:
            raise ValueError("Workflow cannot be run without any input files.")

        return self._find_next_tools(set(starting_tools), starting_tools, set(tool_qs))

    def _find_next_tools(
        self,
        previous_tools: Set[Tool],
        tool_order: List[Tool],
        tool_set: Set[Tool],
    ) -> List[Tool]:
        """Recurrent function that returns a list of Tool objects in the order of their execution.

        Args:
            previous_tools (Set[Tool]): tools from previous iteration for which connected tools are to be found
            tool_order (List[Tool]): current status of tool execution order
            tool_set (Set[Tool]): starting set of tools that includes all of the Tool objects from the current workflow

        Returns:
            List[Tool]: final status of tool execution order
        """
        # TODO Check how many DB queries are fired for this function
        tools = tool_set - previous_tools - set(tool_order)
        next_iteration_candidates = set(
            tool for tool in tools if set(tool.inputs.all()) & previous_tools
        )
        tools_with_complete_inputs = [
            candidate
            for candidate in next_iteration_candidates
            if not (set(candidate.inputs.all()) - set(tool_order))
        ]

        if not tools_with_complete_inputs:
            return tool_order

        tool_order.extend(tools_with_complete_inputs)

        return self._find_next_tools(
            set(tools_with_complete_inputs), tool_order, tool_set
        )
