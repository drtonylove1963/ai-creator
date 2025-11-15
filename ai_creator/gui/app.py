"""
Main Gradio application for AI Creator GUI.
"""

import gradio as gr
from typing import Dict, Any
from ai_creator import (
    TextAgent,
    ImageAgent,
    AnalysisAgent,
    AgentManager,
    AgentConfig,
)
from ai_creator.gui.agent_ui import create_agent_interface
from ai_creator.gui.manager_ui import create_manager_interface
from ai_creator.gui.tools_ui import create_tools_interface


# Global state
agent_manager = AgentManager()
execution_history = []


def create_app() -> gr.Blocks:
    """
    Create the main Gradio application.

    Returns:
        Gradio Blocks application
    """
    with gr.Blocks(
        title="AI Creator - Agent System",
        theme=gr.themes.Soft(),
    ) as app:
        gr.Markdown(
            """
            # 🤖 AI Creator - Agent System

            Build and orchestrate autonomous AI agents with an intuitive interface.
            """
        )

        with gr.Tabs() as tabs:
            # Tab 1: Single Agent
            with gr.Tab("🎯 Single Agent", id=0):
                create_agent_interface(agent_manager, execution_history)

            # Tab 2: Multi-Agent Orchestration
            with gr.Tab("🔗 Multi-Agent", id=1):
                create_manager_interface(agent_manager, execution_history)

            # Tab 3: Agent Tools
            with gr.Tab("🔧 Tools", id=2):
                create_tools_interface()

            # Tab 4: History & Results
            with gr.Tab("📊 History", id=3):
                create_history_interface(execution_history)

            # Tab 5: Documentation
            with gr.Tab("📖 Documentation", id=4):
                create_documentation_interface()

        # Footer
        gr.Markdown(
            """
            ---
            **AI Creator** | [GitHub](https://github.com/drtonylove1963/ai-creator) | Version 0.1.0
            """
        )

    return app


def create_history_interface(history):
    """Create the history viewing interface."""
    gr.Markdown("## Execution History")
    gr.Markdown("View and analyze past agent executions.")

    def get_history_display():
        if not history:
            return "No execution history yet. Run some agents to see results here!"

        output = []
        for i, entry in enumerate(reversed(history[-20:]), 1):  # Last 20 entries
            output.append(f"### Execution #{len(history) - i + 1}")
            output.append(f"**Agent:** {entry.get('agent_name', 'Unknown')}")
            output.append(f"**Status:** {entry.get('status', 'Unknown')}")
            output.append(f"**Iterations:** {entry.get('iterations', 0)}")

            if entry.get('thoughts'):
                output.append(f"**Thoughts:** {len(entry['thoughts'])} recorded")

            if entry.get('content'):
                content_str = str(entry['content'])
                if len(content_str) > 200:
                    content_str = content_str[:200] + "..."
                output.append(f"**Result:** {content_str}")

            output.append("---")

        return "\n\n".join(output)

    history_display = gr.Markdown(get_history_display())
    refresh_btn = gr.Button("🔄 Refresh History", variant="secondary")

    def refresh_history():
        return get_history_display()

    refresh_btn.click(fn=refresh_history, outputs=history_display)

    # Clear history button
    clear_btn = gr.Button("🗑️ Clear History", variant="stop")

    def clear_history():
        history.clear()
        agent_manager.clear_history()
        return "History cleared!"

    clear_msg = gr.Markdown()
    clear_btn.click(fn=clear_history, outputs=clear_msg)


def create_documentation_interface():
    """Create the documentation interface."""
    gr.Markdown(
        """
        ## 📖 Quick Start Guide

        ### Single Agent Usage

        1. Navigate to the **Single Agent** tab
        2. Select an agent type (Text, Image, or Analysis)
        3. Configure the agent settings
        4. Enter your task or prompt
        5. Click "Run Agent" to execute

        ### Multi-Agent Orchestration

        1. Navigate to the **Multi-Agent** tab
        2. Create and register multiple agents
        3. Choose execution mode:
           - **Sequential**: Agents run one after another
           - **Parallel**: Agents run simultaneously with same input
           - **Collaborative**: Agents work together over multiple rounds
        4. Execute and view results

        ### Agent Types

        **TextAgent**
        - Text generation and creative writing
        - Content summarization
        - Text rewriting and refinement

        **ImageAgent**
        - Image generation from descriptions
        - Image analysis and understanding
        - Image modification and editing

        **AnalysisAgent**
        - Sentiment analysis
        - Entity extraction
        - Topic identification
        - Logical reasoning

        ### Tips

        - Use clear, specific prompts for better results
        - Monitor execution history to track performance
        - Experiment with different agent configurations
        - Combine agents for complex workflows

        ### Agent Configuration

        - **Name**: Unique identifier for the agent
        - **Max Iterations**: Maximum think-act cycles (1-20)
        - **Temperature**: Controls randomness (0.0-1.0)
        - **Memory**: Enable to remember past interactions

        ### Example Workflows

        **Content Creation Pipeline**
        1. TextAgent generates initial content
        2. AnalysisAgent reviews quality
        3. TextAgent refines based on feedback

        **Creative Project**
        1. TextAgent creates concept description
        2. ImageAgent generates visuals
        3. AnalysisAgent evaluates coherence

        ### Support

        For more information, check:
        - Project README.md
        - Example scripts in `examples/`
        - Test files in `tests/`
        """
    )


def launch_gui(share: bool = False, server_port: int = 7860):
    """
    Launch the GUI application.

    Args:
        share: Whether to create a public shareable link
        server_port: Port to run the server on
    """
    app = create_app()
    app.launch(
        share=share,
        server_port=server_port,
        server_name="0.0.0.0",
        show_error=True,
    )


if __name__ == "__main__":
    launch_gui()
