# AI Creator GUI

Web-based graphical interface for the AI Creator agent system.

## Overview

The GUI provides an intuitive, browser-based interface for creating, configuring, and orchestrating AI agents. Built with Gradio, it offers a modern, responsive design that works on desktop and mobile devices.

## Features

### 🎯 Single Agent Execution
- Create and configure individual agents (Text, Image, Analysis)
- Adjust agent parameters (max iterations, temperature, memory)
- View agent thoughts and actions in real-time
- See detailed execution results

### 🔗 Multi-Agent Orchestration
- Register and manage multiple agents
- Three execution modes:
  - **Sequential**: Agents run one after another
  - **Parallel**: Agents run simultaneously
  - **Collaborative**: Agents work together over multiple rounds
- Visual agent registry
- Detailed results for each execution mode

### 🔧 Tools Explorer
- Browse available agent tools
- Test tools with custom inputs
- View tool documentation
- Understand tool parameters and outputs

### 📊 Execution History
- View past agent executions
- Analyze results and performance
- Clear history when needed
- Track agent behavior over time

### 📖 Built-in Documentation
- Quick start guide
- Agent type descriptions
- Configuration tips
- Example workflows

## Launching the GUI

### From Command Line

```bash
# Simple launch (default port 7860)
python launch_gui.py

# Custom port
python launch_gui.py --port 8080

# Create shareable public link
python launch_gui.py --share

# With all options
python launch_gui.py --port 8080 --share
```

### From Python Code

```python
from ai_creator import launch_gui

# Basic launch
launch_gui()

# With options
launch_gui(share=True, server_port=8080)
```

### From the Package

```python
from ai_creator.gui import create_app

app = create_app()
app.launch(server_port=7860)
```

## Interface Guide

### Single Agent Tab

1. **Select Agent Type**: Choose TextAgent, ImageAgent, or AnalysisAgent
2. **Name Your Agent**: Give it a unique identifier
3. **Configure Settings**:
   - Max Iterations: How many think-act cycles (1-20)
   - Temperature: Randomness/creativity (0.0-1.0)
   - Memory: Enable to remember past interactions
4. **Enter Task**: Describe what you want the agent to do
5. **Run**: Click "Run Agent" and watch it work
6. **View Results**: See status, thoughts, and output

### Multi-Agent Tab

1. **Create Agents**: Add agents to the registry
   - Choose type and name
   - Click "Add Agent"
2. **Select Agents**: Check which agents to use
3. **Choose Mode**: Sequential, Parallel, or Collaborative
4. **Configure**: Set mode-specific options
5. **Describe Task**: What should agents accomplish?
6. **Execute**: Run the multi-agent system
7. **Review Results**: See how agents worked together

### Tools Tab

1. **Select Tool**: Choose from available tools
2. **View Info**: See tool description and parameters
3. **Enter Input**: Provide test data
4. **Test**: Run the tool
5. **See Results**: View output and details

## Architecture

The GUI is organized into modular components:

- `app.py`: Main Gradio application and layout
- `agent_ui.py`: Single agent execution interface
- `manager_ui.py`: Multi-agent orchestration interface
- `tools_ui.py`: Tools explorer and tester

This modular design makes it easy to:
- Extend with new features
- Customize existing components
- Maintain and debug
- Integrate into larger applications

## Customization

### Adding Custom Components

```python
from ai_creator.gui import create_app
import gradio as gr

# Create base app
app = create_app()

# Add custom components
with app:
    with gr.Tab("My Custom Tab"):
        gr.Markdown("## My Custom Feature")
        # Add your components here

app.launch()
```

### Theming

The GUI uses Gradio's Soft theme by default. To customize:

```python
import gradio as gr

app = create_app()
# Apply custom theme
app.theme = gr.themes.Base()  # or Glass(), Monochrome(), etc.
app.launch()
```

## Technical Details

- **Framework**: Gradio 4.0+
- **Server**: Built-in Gradio server
- **Port**: Default 7860 (configurable)
- **Interface**: Web-based (HTML/JavaScript)
- **State Management**: In-memory (per session)

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
python launch_gui.py --port 8080
```

### Gradio Not Installed

```bash
# Install GUI dependencies
pip install -r requirements.txt
```

### Share Link Not Working

- Check firewall settings
- Ensure internet connectivity
- Try without --share first

## Performance Tips

1. **Memory Management**: Clear history periodically
2. **Agent Limits**: Set reasonable max iterations
3. **Browser**: Use modern browsers (Chrome, Firefox, Safari)
4. **Network**: Local execution is fastest

## Security Considerations

When using `--share`:
- Creates a public URL (anyone with link can access)
- Temporary link (expires after session)
- Don't expose sensitive data
- Use for demos and testing only

For production:
- Run without --share
- Use proper authentication
- Deploy behind firewall/proxy
- Monitor access logs

## Future Enhancements

Planned features:
- User authentication
- Persistent storage
- Advanced visualizations
- Agent performance metrics
- Export/import configurations
- Batch processing
- API endpoint integration

## Support

For issues or questions:
- Check main README.md
- Review example code
- Open GitHub issue
- Check Gradio documentation
