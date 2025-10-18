"""Custom Sphinx extension for generating tables from Python Enum classes."""

import importlib
import inspect
from enum import Enum
from typing import Any

from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class EnumTableDirective(SphinxDirective):
    """Directive to generate a table from a Python Enum class."""

    required_arguments = 1  # The fully qualified enum class path
    optional_arguments = 0
    has_content = False

    def run(self):
        """Generate the enum table."""
        # Get the class path from the directive argument
        class_path = self.arguments[0]

        # Import the enum class
        try:
            module_path, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            enum_cls = getattr(module, class_name)
        except (ValueError, ImportError, AttributeError) as e:
            error = self.state_machine.reporter.error(
                f"Failed to import enum '{class_path}': {e}",
                nodes.literal_block("", ""),
                line=self.lineno,
            )
            return [error]

        # Verify it's an Enum
        if not (inspect.isclass(enum_cls) and issubclass(enum_cls, Enum)):
            error = self.state_machine.reporter.error(
                f"Class '{class_path}' is not a Python Enum",
                nodes.literal_block("", ""),
                line=self.lineno,
            )
            return [error]

        # Generate the table
        table_lines = self._generate_table(enum_cls)

        # Parse the table as reStructuredText
        rst_lines = ViewList()
        for i, line in enumerate(table_lines):
            rst_lines.append(line, f"<enum-table>", i)

        # Create a container node to hold the parsed content
        node = nodes.section()
        node.document = self.state.document

        # Parse the reStructuredText into the node
        self.state.nested_parse(rst_lines, self.content_offset, node)

        # Return the children of the section node
        return node.children

    def _generate_table(self, enum_cls: type[Enum]) -> list[str]:
        """Generate reStructuredText list-table from Enum class."""
        lines = []

        # Start the list-table directive
        lines.append(".. list-table::")
        lines.append("   :header-rows: 1")
        lines.append("   :widths: 40 60")
        lines.append("")

        # Add header row
        lines.append("   * - Name")
        lines.append("     - Value")

        # Get all enum members
        members = list(enum_cls.__members__.items())

        # Add data rows for each enum member
        for name, member in members:
            # Format name as code
            name_str = f"``{name}``"

            # Format value
            value = member.value
            if value is None:
                value_str = "``None``"
            elif isinstance(value, bool):
                # Handle boolean values (must check before int since bool is subclass of int)
                value_str = f"``{value}``"
            elif isinstance(value, str):
                # Escape special characters and show as string
                escaped_value = value.replace("|", "\\|").replace("*", "\\*")
                value_str = f"``\"{escaped_value}\"``"
            elif isinstance(value, (int, float)):
                value_str = f"``{value}``"
            else:
                value_str = f"``{repr(value)}``"

            # Add row
            lines.append(f"   * - {name_str}")
            lines.append(f"     - {value_str}")

        lines.append("")  # Empty line after table
        return lines


def setup(app: Sphinx) -> dict[str, Any]:
    """Setup the Sphinx extension."""
    app.add_directive("enum-table", EnumTableDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
