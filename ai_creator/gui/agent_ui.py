"""
UI components for single agent execution.
"""

import gradio as gr
import json
from typing import Dict, Any, List
from ai_creator import TextAgent, ImageAgent, AnalysisAgent, AgentConfig


def create_agent_interface(agent_manager, execution_history: List):
    """Create the single agent execution interface."""

    gr.Markdown("## Single Agent Execution")
    gr.Markdown("Create and run individual agents for specific tasks.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Agent Configuration")

            agent_type = gr.Dropdown(
                choices=["TextAgent", "ImageAgent", "AnalysisAgent"],
                value="TextAgent",
                label="Agent Type",
                info="Select the type of agent to create"
            )

            agent_name = gr.Textbox(
                value="MyAgent",
                label="Agent Name",
                placeholder="Enter a unique name for your agent"
            )

            with gr.Accordion("Advanced Settings", open=False):
                max_iterations = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=5,
                    step=1,
                    label="Max Iterations",
                    info="Maximum number of think-act cycles"
                )

                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.7,
                    step=0.1,
                    label="Temperature",
                    info="Controls randomness (higher = more creative)"
                )

                memory_enabled = gr.Checkbox(
                    value=True,
                    label="Enable Memory",
                    info="Agent remembers past interactions"
                )

        with gr.Column(scale=2):
            gr.Markdown("### Task Input")

            # Dynamic input based on agent type
            task_input = gr.Textbox(
                label="Task/Prompt",
                placeholder="Enter your task or prompt here...",
                lines=5
            )

            # Additional inputs for specific agent types
            with gr.Accordion("Task-Specific Options", open=False):
                task_type = gr.Dropdown(
                    choices=["generate", "summarize", "rewrite", "analyze"],
                    value="generate",
                    label="Task Type",
                    visible=True
                )

                analysis_type = gr.Dropdown(
                    choices=["sentiment", "entities", "topics", "reasoning", "general"],
                    value="general",
                    label="Analysis Type",
                    visible=False
                )

            run_btn = gr.Button("🚀 Run Agent", variant="primary", size="lg")

            gr.Markdown("### Results")

            with gr.Row():
                status_box = gr.Textbox(label="Status", interactive=False)
                iterations_box = gr.Textbox(label="Iterations", interactive=False)

            thoughts_box = gr.Textbox(
                label="Agent Thoughts",
                lines=5,
                interactive=False
            )

            output_box = gr.Textbox(
                label="Agent Output",
                lines=8,
                interactive=False
            )

            actions_json = gr.JSON(label="Actions Detail")

    # Update task type visibility based on agent type
    def update_task_options(agent_type_value):
        if agent_type_value == "TextAgent":
            return gr.update(visible=True), gr.update(visible=False)
        elif agent_type_value == "AnalysisAgent":
            return gr.update(visible=False), gr.update(visible=True)
        else:
            return gr.update(visible=False), gr.update(visible=False)

    agent_type.change(
        fn=update_task_options,
        inputs=[agent_type],
        outputs=[task_type, analysis_type]
    )

    # Run agent function
    def run_single_agent(
        agent_type_val,
        agent_name_val,
        max_iter,
        temp,
        memory_en,
        task_input_val,
        task_type_val,
        analysis_type_val
    ):
        try:
            # Create agent based on type
            if agent_type_val == "TextAgent":
                agent = TextAgent(
                    name=agent_name_val,
                    max_iterations=int(max_iter),
                    temperature=temp,
                    memory_enabled=memory_en
                )
                # Prepare input
                if task_type_val != "generate":
                    input_data = {
                        "task": task_type_val,
                        "content": task_input_val
                    }
                else:
                    input_data = task_input_val

            elif agent_type_val == "ImageAgent":
                agent = ImageAgent(
                    name=agent_name_val,
                    max_iterations=int(max_iter),
                    temperature=temp,
                    memory_enabled=memory_en
                )
                input_data = {
                    "task": "generate",
                    "description": task_input_val
                }

            else:  # AnalysisAgent
                agent = AnalysisAgent(
                    name=agent_name_val,
                    max_iterations=int(max_iter),
                    temperature=temp,
                    memory_enabled=memory_en
                )
                input_data = {
                    "type": analysis_type_val,
                    "content": task_input_val
                }

            # Run the agent
            response = agent.run(input_data)

            # Store in history
            execution_history.append({
                "agent_name": response.agent_name,
                "status": response.status.value,
                "iterations": response.iterations,
                "thoughts": response.thoughts,
                "content": response.content,
                "actions": response.actions
            })

            # Format output
            thoughts_text = "\n\n".join([
                f"Thought {i+1}: {thought}"
                for i, thought in enumerate(response.thoughts)
            ])

            # Format content based on type
            if isinstance(response.content, dict):
                content_text = json.dumps(response.content, indent=2)
            else:
                content_text = str(response.content)

            return (
                response.status.value,
                str(response.iterations),
                thoughts_text,
                content_text,
                response.actions
            )

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            return (
                "ERROR",
                "0",
                error_msg,
                error_msg,
                []
            )

    run_btn.click(
        fn=run_single_agent,
        inputs=[
            agent_type,
            agent_name,
            max_iterations,
            temperature,
            memory_enabled,
            task_input,
            task_type,
            analysis_type
        ],
        outputs=[
            status_box,
            iterations_box,
            thoughts_box,
            output_box,
            actions_json
        ]
    )
