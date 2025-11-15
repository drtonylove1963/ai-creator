"""
UI components for multi-agent orchestration.
"""

import gradio as gr
import json
from typing import List, Dict, Any
from ai_creator import TextAgent, ImageAgent, AnalysisAgent


def create_manager_interface(agent_manager, execution_history: List):
    """Create the multi-agent orchestration interface."""

    gr.Markdown("## Multi-Agent Orchestration")
    gr.Markdown("Coordinate multiple agents to work together on complex tasks.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Agent Registry")

            # Agent creation section
            with gr.Group():
                gr.Markdown("**Create New Agent**")
                new_agent_type = gr.Dropdown(
                    choices=["TextAgent", "ImageAgent", "AnalysisAgent"],
                    value="TextAgent",
                    label="Agent Type"
                )
                new_agent_name = gr.Textbox(
                    label="Agent Name",
                    placeholder="e.g., Writer, Analyzer, Designer"
                )
                add_agent_btn = gr.Button("➕ Add Agent", variant="secondary")
                add_status = gr.Textbox(label="Status", interactive=False, max_lines=2)

            # List of registered agents
            gr.Markdown("**Registered Agents**")
            agents_list = gr.Textbox(
                value="No agents registered yet.",
                label="Active Agents",
                interactive=False,
                lines=6
            )
            refresh_agents_btn = gr.Button("🔄 Refresh List", variant="secondary")
            clear_agents_btn = gr.Button("🗑️ Clear All Agents", variant="stop")

        with gr.Column(scale=2):
            gr.Markdown("### Orchestration")

            execution_mode = gr.Radio(
                choices=["Sequential", "Parallel", "Collaborative"],
                value="Sequential",
                label="Execution Mode",
                info="How agents should work together"
            )

            # Agent selection
            selected_agents = gr.CheckboxGroup(
                choices=[],
                label="Select Agents to Execute",
                info="Choose which agents to include in this execution"
            )

            task_description = gr.Textbox(
                label="Task Description",
                placeholder="Describe the task for the agents...",
                lines=4
            )

            with gr.Accordion("Advanced Options", open=False):
                pass_output = gr.Checkbox(
                    value=True,
                    label="Pass Output Between Agents (Sequential mode)",
                    info="Each agent receives the previous agent's output"
                )

                max_rounds = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    label="Max Collaboration Rounds",
                    info="For Collaborative mode only"
                )

            execute_btn = gr.Button("▶️ Execute Agents", variant="primary", size="lg")

            gr.Markdown("### Results")

            execution_status = gr.Textbox(
                label="Execution Status",
                interactive=False
            )

            results_output = gr.Textbox(
                label="Execution Results",
                lines=12,
                interactive=False
            )

            results_json = gr.JSON(label="Detailed Results")

    # Add agent function
    def add_agent(agent_type, agent_name):
        if not agent_name:
            return "❌ Please provide an agent name.", agents_list.value

        # Check if agent already exists
        if agent_manager.get_agent(agent_name):
            return f"❌ Agent '{agent_name}' already exists!", agents_list.value

        try:
            # Create and register agent
            if agent_type == "TextAgent":
                agent = TextAgent(name=agent_name)
            elif agent_type == "ImageAgent":
                agent = ImageAgent(name=agent_name)
            else:
                agent = AnalysisAgent(name=agent_name)

            agent_manager.register_agent(agent)

            # Update agents list
            agent_names = agent_manager.list_agents()
            agents_text = "\n".join([f"• {name}" for name in agent_names])

            return f"✅ Added {agent_type}: {agent_name}", agents_text

        except Exception as e:
            return f"❌ Error: {str(e)}", agents_list.value

    add_agent_btn.click(
        fn=add_agent,
        inputs=[new_agent_type, new_agent_name],
        outputs=[add_status, agents_list]
    )

    # Refresh agents list
    def refresh_agents():
        agent_names = agent_manager.list_agents()
        if not agent_names:
            return "No agents registered yet.", []

        agents_text = "\n".join([f"• {name}" for name in agent_names])
        return agents_text, agent_names

    refresh_agents_btn.click(
        fn=refresh_agents,
        outputs=[agents_list, selected_agents]
    )

    # Clear all agents
    def clear_all_agents():
        agent_names = agent_manager.list_agents()
        for name in agent_names:
            agent_manager.unregister_agent(name)
        return "No agents registered yet.", []

    clear_agents_btn.click(
        fn=clear_all_agents,
        outputs=[agents_list, selected_agents]
    )

    # Execute agents function
    def execute_multi_agents(
        mode,
        selected_agent_names,
        task_desc,
        pass_out,
        max_rnd
    ):
        if not selected_agent_names:
            return "❌ Please select at least one agent.", "", {}

        if not task_desc:
            return "❌ Please provide a task description.", "", {}

        try:
            results_text = []
            results_data = {}

            if mode == "Sequential":
                responses = agent_manager.run_sequential(
                    agent_names=selected_agent_names,
                    input_data=task_desc,
                    pass_output=pass_out
                )

                results_text.append(f"Sequential Execution: {len(responses)} agents")
                results_text.append("=" * 60)

                for i, response in enumerate(responses, 1):
                    results_text.append(f"\nAgent {i}: {response.agent_name}")
                    results_text.append(f"Status: {response.status.value}")
                    results_text.append(f"Iterations: {response.iterations}")

                    if isinstance(response.content, dict):
                        content_str = json.dumps(response.content, indent=2)
                    else:
                        content_str = str(response.content)

                    results_text.append(f"Output: {content_str[:300]}...")
                    results_text.append("-" * 60)

                results_data = {
                    "mode": "sequential",
                    "agents": [r.to_dict() for r in responses]
                }

            elif mode == "Parallel":
                responses = agent_manager.run_parallel(
                    agent_names=selected_agent_names,
                    input_data=task_desc
                )

                results_text.append(f"Parallel Execution: {len(responses)} agents")
                results_text.append("=" * 60)

                for response in responses:
                    results_text.append(f"\n{response.agent_name}:")
                    results_text.append(f"  Status: {response.status.value}")
                    results_text.append(f"  Iterations: {response.iterations}")

                    if isinstance(response.content, dict):
                        content_str = json.dumps(response.content, indent=2)
                    else:
                        content_str = str(response.content)

                    results_text.append(f"  Output: {content_str[:200]}...")
                    results_text.append("-" * 60)

                results_data = {
                    "mode": "parallel",
                    "agents": [r.to_dict() for r in responses]
                }

            else:  # Collaborative
                result = agent_manager.collaborate(
                    task=task_desc,
                    agent_names=selected_agent_names,
                    max_rounds=int(max_rnd)
                )

                results_text.append(f"Collaborative Execution: {result['rounds']} rounds")
                results_text.append("=" * 60)

                for round_data in result['collaboration_log']:
                    results_text.append(f"\nRound {round_data['round']}:")
                    for agent_result in round_data['results']:
                        results_text.append(f"  • {agent_result['agent']}: {agent_result['response']['status']}")
                    results_text.append("-" * 60)

                results_data = result

            # Add to execution history
            execution_history.append({
                "mode": mode,
                "agents": selected_agent_names,
                "task": task_desc,
                "results": results_data
            })

            status = f"✅ Execution completed successfully ({mode} mode)"
            return status, "\n".join(results_text), results_data

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            return error_msg, error_msg, {"error": str(e)}

    execute_btn.click(
        fn=execute_multi_agents,
        inputs=[
            execution_mode,
            selected_agents,
            task_description,
            pass_output,
            max_rounds
        ],
        outputs=[
            execution_status,
            results_output,
            results_json
        ]
    )

    # Auto-refresh agent list when tab is opened
    def auto_refresh():
        return refresh_agents()
