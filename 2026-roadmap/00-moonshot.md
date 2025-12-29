# AI-Powered Visualization Assistant

**Category:** Moonshot
**Quarter:** Q4+
**T-shirt Size:** XXL

## Why This Matters

Data visualization is both an art and a science—choosing the right chart type, configuring axes, selecting colors, writing captions that tell the story. Most developers aren't visualization experts, and even experts spend significant time on repetitive configuration. An AI-powered assistant could democratize data storytelling: describe what you want to show, and get a publication-ready visualization.

This isn't just a feature—it's a paradigm shift. The library becomes an intelligent collaborator that understands your data and your intent, making every Python developer capable of creating visualizations that would previously require specialized knowledge.

## Why This Is a Moonshot

This is the most ambitious initiative because it requires:

1. **Integration with LLMs**: Building reliable, production-grade AI features is still emerging territory
2. **Data understanding**: The AI must analyze datasets to make meaningful recommendations
3. **Subjective quality**: "Good" visualization involves aesthetic and journalistic judgment that's hard to encode
4. **Reliability requirements**: AI recommendations must be trustworthy enough for professional use
5. **API design challenge**: Making AI feel natural without being intrusive or annoying
6. **Cost considerations**: LLM API costs could be significant for high-volume usage

The upside is transformative: a library where you can simply say "show me how sales changed over time, highlighting the Q3 dip" and get a perfectly configured, annotated, publication-ready chart.

## Current State

Chart creation is entirely manual and requires explicit knowledge:

```python
# User must know:
# - Which chart type fits the data
# - How to configure all options
# - What annotations would help
# - Color and formatting best practices

chart = dw.LineChart(
    title="Monthly Sales 2024",  # Manual title
    data=df,
    axis_label_format=dw.NumberFormat.DOLLAR,  # Must know option exists
    line_color="#1f77b4",  # Must choose color
    # ... 20 more configuration options
)
```

Users who aren't visualization experts often:
- Choose suboptimal chart types
- Miss important configuration options
- Create charts without annotations or context
- Use poor color schemes for accessibility

## Proposed Future State

An intelligent assistant that collaborates on visualization:

```python
import datawrapper as dw

# Natural language chart creation
chart = dw.ai.create(
    data=sales_df,
    prompt="Show monthly sales trend, highlighting the Q3 decline and annotating the holiday spike"
)
# Returns a fully configured LineChart with annotations, title, and insights

# Interactive refinement
chart = dw.ai.create(data=df, prompt="Compare regions")
chart = chart.refine("Make the Western region stand out more")
chart = chart.refine("Add context about why Eastern dropped")

# AI-assisted analysis
insights = dw.ai.analyze(df)
# Returns: "This data shows quarterly revenue by region. Key observations:
#           1. Western region grew 45% YoY
#           2. Eastern region declined in Q3, likely due to..."

# Chart type recommendation
recommendation = dw.ai.recommend_chart(df)
# Returns: {"recommended": "grouped-bar", "reasoning": "...", "alternatives": [...]}

# Auto-generate complete dashboard
dashboard = dw.ai.dashboard(
    data_sources={"sales": sales_df, "costs": costs_df, "customers": customers_df},
    prompt="Executive summary of Q4 business performance"
)
# Returns a Gallery with multiple coordinated charts, narrative text, and insights

# Caption and alt-text generation
chart = dw.BarChart(title="Sales", data=df)
chart.description = dw.ai.generate_description(chart)  # Accessible description
chart.caption = dw.ai.generate_caption(chart)  # Journalistic caption

# Style transfer
chart = dw.ai.create(data=df, style="economist")  # Match The Economist's style
chart = dw.ai.create(data=df, style="nytimes")  # Match NYT's data viz style
```

### AI-Powered CLI

```bash
# Natural language from terminal
$ dw ai "Create a chart showing how Python adoption grew compared to other languages"
? Found dataset 'programming_languages.csv'. Use this? Yes
? Recommended chart: Stacked Area Chart. Proceed? Yes
Creating chart... Done!
Published: https://datawrapper.dwcdn.net/abc123/

# Interactive session
$ dw ai --interactive
🤖 What data would you like to visualize?
> I have sales data by region and quarter
🤖 Please provide the data file or database connection
> sales_q4.csv
🤖 I see quarterly revenue for 5 regions. I recommend:
   1. Grouped bar chart (compare regions per quarter)
   2. Line chart (show trends over time)
   3. Heatmap (show all combinations)
   Which would you prefer?
> 1
🤖 Creating grouped bar chart... Here's a preview:
   [ASCII preview of chart]
   Would you like to:
   1. Publish as-is
   2. Add annotations
   3. Change colors
   4. Start over
```

## Key Deliverables

### Core AI Features
- [ ] **`dw.ai.create()`** - Natural language to chart
- [ ] **`dw.ai.analyze()`** - Data insights and recommendations
- [ ] **`dw.ai.recommend_chart()`** - Chart type suggestion engine
- [ ] **`dw.ai.refine()`** - Iterative chart improvement
- [ ] **`dw.ai.dashboard()`** - Multi-chart narrative generation

### Content Generation
- [ ] **Caption generation** - Journalistic-quality captions
- [ ] **Alt-text generation** - Accessibility descriptions
- [ ] **Title suggestions** - Context-aware titles
- [ ] **Annotation recommendations** - Key points to highlight

### Style Intelligence
- [ ] **Style library** - Named styles (economist, nytimes, scientific)
- [ ] **Color palette recommendation** - Based on data and context
- [ ] **Accessibility checker** - AI-powered a11y validation

### Integration
- [ ] **LLM abstraction layer** - Support OpenAI, Anthropic, local models
- [ ] **Prompt templates** - Optimized prompts for visualization tasks
- [ ] **Caching layer** - Reduce redundant LLM calls
- [ ] **Streaming responses** - Progressive generation feedback
- [ ] **CLI integration** - `dw ai` command family

### Safety & Quality
- [ ] **Confidence scoring** - How sure is the AI about recommendations?
- [ ] **Human-in-the-loop** - Confirmations for significant decisions
- [ ] **Audit trail** - Log AI decisions for debugging
- [ ] **Fallback paths** - Graceful degradation without AI

## Prerequisites

- Initiative 01 (Complete Chart Type Coverage) - AI needs all chart types available
- Initiative 06 (CLI) - For AI-powered command line experience
- Initiative 09 (Gallery Builder) - For AI-generated dashboards
- Initiative 08 (Data Pipeline) - For data-aware recommendations

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Python API  │  │    CLI      │  │    Jupyter Magic        │  │
│  │ dw.ai.xxx() │  │ $ dw ai ... │  │  %%datawrapper_ai      │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │                │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI Orchestration Layer                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                 Intent Classifier                        │    │
│  │  "create chart" → CreateIntent                          │    │
│  │  "analyze data" → AnalyzeIntent                         │    │
│  │  "refine this"  → RefineIntent                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ┌─────────────┐  ┌──────────┴──────────┐  ┌─────────────────┐  │
│  │   Data      │  │   Chart Type        │  │    Content      │  │
│  │   Analyzer  │  │   Recommender       │  │    Generator    │  │
│  └──────┬──────┘  └──────────┬──────────┘  └────────┬────────┘  │
│         │                    │                      │            │
│         ▼                    ▼                      ▼            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Prompt Templates                        │    │
│  │  - chart_selection.txt                                  │    │
│  │  - data_analysis.txt                                    │    │
│  │  - caption_generation.txt                               │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LLM Abstraction                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   OpenAI    │  │  Anthropic  │  │   Local (Ollama)        │  │
│  │   GPT-4     │  │   Claude    │  │   Llama, Mistral        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
│  Features: Retry logic, rate limiting, caching, streaming      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Chart Generation                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  AI Output → Pydantic Models → Chart Classes → API      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Risks & Open Questions

### Technical Risks
- **LLM reliability**: AI outputs can be inconsistent; need robust validation
- **Prompt engineering**: Visualization-specific prompts require expertise
- **Latency**: LLM calls add seconds; must not feel slow
- **Cost**: API costs could be prohibitive for high-volume users
- **Model dependency**: OpenAI/Anthropic API changes could break functionality

### Product Risks
- **User trust**: Will users trust AI-generated visualizations for professional work?
- **Skill atrophy**: Does AI assistance reduce users' visualization skills?
- **Vendor lock-in**: Deep LLM integration creates dependency
- **Scope creep**: AI features can expand infinitely

### Open Questions
- **Which LLM?**: OpenAI GPT-4, Anthropic Claude, or support multiple?
- **Local vs cloud**: Should local models be supported for privacy?
- **Pricing model**: Free tier with limits? Usage-based? Premium feature?
- **Data privacy**: How to handle sensitive data in LLM prompts?
- **Determinism**: Same prompt should ideally produce similar charts

## Implementation Phases

### Phase 1: Foundation (Q4 2026)
- LLM abstraction layer with OpenAI support
- Basic `dw.ai.create()` for simple charts
- Chart type recommendation

### Phase 2: Intelligence (Q1 2027)
- Data analysis and insights
- Caption and description generation
- Iterative refinement

### Phase 3: Advanced (Q2 2027)
- Multi-chart dashboard generation
- Style transfer and templates
- CLI integration

### Phase 4: Polish (Q3 2027)
- Local model support
- Advanced caching and optimization
- Production hardening

## Notes

The `rich` library already supports Markdown rendering, which could display AI explanations beautifully in the terminal.

Pydantic models (`datawrapper/charts/models/`) provide structured output targets for LLM responses:

```python
from pydantic import BaseModel

class ChartRecommendation(BaseModel):
    chart_type: str
    title: str
    reasoning: str
    confidence: float
    configuration: dict

# LLM returns structured JSON that Pydantic validates
response = llm.complete(prompt, response_format=ChartRecommendation)
```

Consider using function calling / tool use for structured LLM outputs:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_bar_chart",
            "description": "Create a bar chart visualization",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "x_column": {"type": "string"},
                    "y_column": {"type": "string"},
                    # ...
                }
            }
        }
    }
]
```

For data privacy, consider:
- Only sending column names and sample values to LLM
- Local embedding models for data analysis
- User consent for cloud processing
- Enterprise self-hosted LLM option

---

## The Vision

Imagine a world where creating a publication-quality visualization is as simple as:

```python
>>> dw.ai.create(sales_data, "Why did Q3 underperform?")
```

The AI analyzes the data, identifies the story, chooses the right visualization, configures every option thoughtfully, writes an insightful caption, and produces a chart that a data journalist would be proud of.

That's the moonshot.
