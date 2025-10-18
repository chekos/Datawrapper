"""Custom Sphinx extension for generating parameter tables from Pydantic models."""

import importlib
import inspect
from typing import Any, get_args, get_origin

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class ParameterTableDirective(SphinxDirective):
    """Directive to generate a parameter table from a Pydantic model class."""

    required_arguments = 1  # The fully qualified class path
    optional_arguments = 0
    has_content = False

    def run(self):
        """Generate the parameter table."""
        # Get the class path from the directive argument
        class_path = self.arguments[0]

        print(f"\n=== DEBUG: ParameterTableDirective.run() called ===")
        print(f"Class path: {class_path}")

        # Import the class
        try:
            module_path, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            print(f"Successfully imported class: {cls}")
        except (ValueError, ImportError, AttributeError) as e:
            error = self.state_machine.reporter.error(
                f"Failed to import class '{class_path}': {e}",
                nodes.literal_block("", ""),
                line=self.lineno,
            )
            return [error]

        # Verify it's a Pydantic model
        if not issubclass(cls, BaseModel):
            error = self.state_machine.reporter.error(
                f"Class '{class_path}' is not a Pydantic BaseModel",
                nodes.literal_block("", ""),
                line=self.lineno,
            )
            return [error]

        # Collect all fields including inherited ones
        all_fields = {}
        for base_cls in reversed(cls.__mro__):
            if issubclass(base_cls, BaseModel) and base_cls is not BaseModel:
                all_fields.update(base_cls.model_fields)

        print(f"Collected {len(all_fields)} fields")
        print(f"Field names: {list(all_fields.keys())[:5]}...")  # Show first 5

        # Generate the table
        table_lines = self._generate_table(all_fields)

        print(f"Generated {len(table_lines)} table lines")
        print(f"First 5 lines:")
        for line in table_lines[:5]:
            print(f"  '{line}'")

        # Parse the table as reStructuredText
        # Create a ViewList (StringList) with proper source tracking
        from docutils.statemachine import ViewList

        rst_lines = ViewList()
        for i, line in enumerate(table_lines):
            rst_lines.append(line, f"<parameter-table>", i)

        # Create a container node to hold the parsed content
        node = nodes.section()
        node.document = self.state.document

        # Parse the reStructuredText into the node
        self.state.nested_parse(rst_lines, self.content_offset, node)

        print(f"Node children: {len(node.children)}")
        if node.children:
            print(f"First child type: {type(node.children[0])}")
            if isinstance(node.children[0], nodes.system_message):
                print(f"ERROR MESSAGE: {node.children[0].astext()}")
        print(f"=== END DEBUG ===\n")

        # Return the children of the section node (not the section itself)
        return node.children

    def _generate_table(self, fields: dict[str, FieldInfo]) -> list[str]:
        """Generate reStructuredText list-table from Pydantic fields."""
        lines = []

        # Start the list-table directive
        lines.append(".. list-table::")
        lines.append("   :header-rows: 1")
        lines.append("   :widths: 20 15 35 30")
        lines.append("")

        # Add header row
        lines.append("   * - Parameter")
        lines.append("     - Default")
        lines.append("     - Description")
        lines.append("     - Type")

        # Sort fields alphabetically and add data rows
        for field_name in sorted(fields.keys()):
            field_info = fields[field_name]

            # Get parameter name (use Python name, not alias)
            param_name = f"``{field_name}``"

            # Get type annotation
            type_str = self._format_type(field_info.annotation)

            # Get default value
            default_str = self._format_default(field_info)

            # Get description
            description = field_info.description or ""

            # Add row
            lines.append(f"   * - {param_name}")
            lines.append(f"     - {default_str}")
            lines.append(f"     - {description}")
            lines.append(f"     - {type_str}")

        lines.append("")  # Empty line after table
        return lines

    def _format_type(self, annotation: Any) -> str:
        """Format a type annotation as a string, including enum values."""
        if annotation is None:
            return ""

        # Handle Optional types (Union with None)
        origin = get_origin(annotation)
        args = get_args(annotation)

        if annotation is type(None):
            return "None"

        # Handle Union types (including Optional)
        # Check for Union from typing module or Python 3.10+ union syntax
        from typing import Union
        if origin is Union or (hasattr(origin, "__name__") and origin.__name__ == "UnionType"):
            # For Union types
            type_parts = []
            for arg in args:
                if arg is type(None):
                    type_parts.append("None")
                else:
                    type_parts.append(self._format_single_type(arg))
            return " or ".join(type_parts)

        return self._format_single_type(annotation)

    def _format_single_type(self, annotation: Any) -> str:
        """Format a single type annotation."""
        # Check if it's an Enum
        if inspect.isclass(annotation):
            try:
                # Try to get enum values
                if hasattr(annotation, "__members__"):
                    enum_values = list(annotation.__members__.keys())  # type: ignore
                    if enum_values:
                        # Show first few values with ellipsis if too many
                        if len(enum_values) > 3:
                            shown = ", ".join(enum_values[:3])
                            return f"{annotation.__name__} ({shown}, ...)"
                        else:
                            shown = ", ".join(enum_values)
                            return f"{annotation.__name__} ({shown})"
            except Exception:
                pass

        # Handle generic types (list, dict, etc.)
        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is not None:
            origin_name = getattr(origin, "__name__", str(origin))
            if args:
                arg_strs = [self._format_single_type(arg) for arg in args]
                return f"{origin_name}[{', '.join(arg_strs)}]"
            return f"{origin_name}"

        # Handle regular types
        if hasattr(annotation, "__name__"):
            return f"{annotation.__name__}"

        # Fallback to string representation
        return f"{str(annotation)}"

    def _format_default(self, field_info: FieldInfo) -> str:
        """Format the default value of a field."""
        if field_info.is_required():
            return "**Required**"

        default = field_info.default
        if default is None:
            return "`None`"

        # Handle special default values
        if isinstance(default, str):
            # Escape pipe characters
            default_str = default.replace("|", "\\|")
            # Truncate long strings
            if len(default_str) > 30:
                return f"`\"{default_str[:27]}...\"`"
            return f"`\"{default_str}\"`"

        if isinstance(default, bool):
            return f"`{default}`"

        if isinstance(default, (int, float)):
            return f"`{default}`"

        if isinstance(default, (list, tuple)):
            if len(default) == 0:
                return "`[]`"
            # Show abbreviated version for long lists
            if len(default) > 3:
                return f"`[...{len(default)} items]`"
            return f"`{default}`"

        if isinstance(default, dict):
            if len(default) == 0:
                return "`{}`"
            return "`{...}`"

        # Fallback
        return f"`{repr(default)}`"


def setup(app: Sphinx) -> dict[str, Any]:
    """Setup the Sphinx extension."""
    app.add_directive("parameter-table", ParameterTableDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
