# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Object-Oriented Chart Classes
- **BarChart** - Create horizontal bar charts with type-safe configuration
- **LineChart** - Create line charts with date/time formatting and multiple series
- **ColumnChart** - Create vertical column charts with custom ranges and styling
- **AreaChart** - Create area charts with fills and stacking options
- **ScatterPlot** - Create scatter plots with size and color encoding
- **StackedBarChart** - Create stacked bar charts for composition analysis
- **ArrowChart** - Create arrow charts for showing change over time
- **MultipleColumnChart** - Create grouped column charts for comparisons

#### Type-Safe Enums
- **NumberFormat** - 31 semantic number formatting options (e.g., `THOUSANDS_SEPARATOR`, `ABBREVIATED`, `PERCENT_TWO_DECIMALS`)
- **DateFormat** - 50 date formatting patterns (e.g., `MONTH_ABBREVIATED_WITH_YEAR`, `YEAR_QUARTER`, `DAY_OF_WEEK_FULL`)
- **NumberDivisor** - 11 number scaling options (e.g., `DIVIDE_BY_MILLION`, `AUTO_DETECT`, `MULTIPLY_BY_HUNDRED`)
- **LineWidth** - 4 line width options (`THIN`, `MEDIUM`, `THICK`, `EXTRA_THICK`)
- **LineDash** - 5 line dash patterns (`SOLID`, `DASHED`, `DOTTED`, `DASH_DOT`, `LONG_DASH`)

#### Pydantic Models
- **ColumnFormat** - Type-safe column formatting with validation
- **Annotate** - Chart annotation configuration
- **Describe** - Chart description and metadata
- **Logo** - Custom logo configuration
- **Publish** - Publishing settings and options
- **PublishBlocks** - Control which chart elements to publish
- **Sharing** - Social sharing configuration
- **Transform** - Data transformation settings
- **Visualize** - Visualization-specific settings

#### Annotation Classes
- **TextAnnotation** - Add text annotations to charts
- **RangeAnnotation** - Add range annotations to highlight data regions
- **ConnectorLine** - Add connector lines to annotations

#### Line Configuration
- **Line** - Configure individual lines in line charts
- **LineSymbol** - Configure line symbols/markers
- **LineValueLabel** - Configure value labels on lines
- **AreaFill** - Configure area fills under lines

#### Serialization Utilities
- **ColorCategory** - Handle color category mappings
- **CustomRange** - Handle custom axis ranges
- **CustomTicks** - Handle custom tick marks
- **ModelListSerializer** - Serialize lists of Pydantic models
- **NegativeColor** - Handle negative value coloring
- **PlotHeight** - Handle plot height configuration
- **ReplaceFlags** - Handle flag icon replacement
- **ValueLabels** - Handle value label configuration

### Changed

- **Recommended approach** - Object-oriented chart classes are now the recommended way to create charts
- **Documentation structure** - Reorganized to prioritize OOP features for newcomers
- **Code examples** - All examples now showcase type-safe enums and Pydantic models
- **Package manager** - Updated from pipenv to uv for faster dependency management

### Deprecated

- **Low-level API** - While still fully supported and backwards compatible, the low-level dictionary-based API (`create_chart()` with raw dictionaries, `update_metadata()` with nested dicts) is no longer the recommended approach. It remains available for advanced use cases and edge cases not yet covered by OOP classes.

### Technical Details

- **Pydantic validation** - All chart classes use Pydantic v2 for runtime type checking and validation
- **Backwards compatibility** - All existing code using the low-level API continues to work without changes
- **Test coverage** - 754 tests passing (unit, integration, and functional tests)
- **Type safety** - Full mypy type checking support
- **Code quality** - Passes ruff linting checks

### Benefits

- 🎯 **Type safety** - Catch configuration errors before runtime with Pydantic validation
- 💡 **IDE autocomplete** - Discover available options as you type with full IntelliSense support
- 📖 **Readable code** - Use semantic enum names (e.g., `NumberFormat.THOUSANDS_SEPARATOR`) instead of cryptic format strings (e.g., `"0,0"`)
- 🔧 **Flexible** - Mix OOP chart classes with low-level API calls when needed
- 📚 **Self-documenting** - Comprehensive docstrings and type hints make the API discoverable

## [Previous Releases]

See [GitHub Releases](https://github.com/chekos/datawrapper/releases) for information about previous versions.
