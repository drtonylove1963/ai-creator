"""
UI components for agent tools.
"""

import gradio as gr
from ai_creator.agents.tools import default_registry


def create_tools_interface():
    """Create the tools interface."""

    gr.Markdown("## Agent Tools")
    gr.Markdown("Explore and test tools available to agents.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Available Tools")

            tool_names = default_registry.list_tools()

            tool_selector = gr.Dropdown(
                choices=tool_names,
                value=tool_names[0] if tool_names else None,
                label="Select Tool",
                info="Choose a tool to view details and test"
            )

            tool_info = gr.JSON(label="Tool Information")

            # Update tool info when selection changes
            def update_tool_info(tool_name):
                if tool_name:
                    return default_registry.get_tool_info(tool_name)
                return {}

            tool_selector.change(
                fn=update_tool_info,
                inputs=[tool_selector],
                outputs=[tool_info]
            )

            # Initialize with first tool
            if tool_names:
                tool_info.value = default_registry.get_tool_info(tool_names[0])

        with gr.Column(scale=2):
            gr.Markdown("### Tool Tester")
            gr.Markdown("Test tools with custom inputs.")

            # Tool-specific inputs
            with gr.Group():
                gr.Markdown("**Input Parameters**")

                # Text input (for most tools)
                text_input = gr.Textbox(
                    label="Text Input",
                    placeholder="Enter text for text-based tools...",
                    lines=4
                )

                # Number input
                number_input = gr.Number(
                    label="Number Input",
                    value=5,
                    visible=False
                )

                # Expression input
                expression_input = gr.Textbox(
                    label="Expression",
                    placeholder="e.g., 2 + 2, (10 * 5) / 2",
                    visible=False
                )

            test_btn = gr.Button("🧪 Test Tool", variant="primary")

            gr.Markdown("### Results")

            tool_output = gr.Textbox(
                label="Tool Output",
                lines=8,
                interactive=False
            )

            output_json = gr.JSON(label="Detailed Output")

    # Update inputs based on selected tool
    def update_inputs(tool_name):
        if tool_name == "calculate":
            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True)
            )
        elif tool_name in ["extract_keywords"]:
            return (
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False)
            )
        else:
            return (
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )

    tool_selector.change(
        fn=update_inputs,
        inputs=[tool_selector],
        outputs=[text_input, number_input, expression_input]
    )

    # Test tool function
    def test_tool(tool_name, text_val, num_val, expr_val):
        if not tool_name:
            return "Please select a tool", {}

        try:
            result = None

            if tool_name == "text_length":
                result = default_registry.execute(tool_name, text=text_val)
                output_text = f"Text length: {result} characters"

            elif tool_name == "word_count":
                result = default_registry.execute(tool_name, text=text_val)
                output_text = f"Word count: {result} words"

            elif tool_name == "extract_keywords":
                result = default_registry.execute(
                    tool_name,
                    text=text_val,
                    top_n=int(num_val)
                )
                output_text = f"Keywords: {', '.join(result)}"

            elif tool_name == "calculate":
                result = default_registry.execute(tool_name, expression=expr_val)
                output_text = f"Result: {result}"

            elif tool_name == "format_json":
                import json
                try:
                    # Try to parse text as JSON
                    data = json.loads(text_val)
                    result = default_registry.execute(tool_name, data=data)
                    output_text = result
                except json.JSONDecodeError:
                    # If not valid JSON, create a simple object
                    data = {"input": text_val}
                    result = default_registry.execute(tool_name, data=data)
                    output_text = result

            else:
                output_text = f"Tool '{tool_name}' test not implemented"
                result = None

            return output_text, {"result": result, "tool": tool_name}

        except Exception as e:
            error_msg = f"Error testing tool: {str(e)}"
            return error_msg, {"error": str(e)}

    test_btn.click(
        fn=test_tool,
        inputs=[tool_selector, text_input, number_input, expression_input],
        outputs=[tool_output, output_json]
    )

    # Tool documentation
    with gr.Accordion("📚 Tool Documentation", open=False):
        gr.Markdown(
            """
            ### Built-in Tools

            **text_length**
            - Calculate the length of text in characters
            - Input: text (string)
            - Output: integer

            **word_count**
            - Count words in text
            - Input: text (string)
            - Output: integer

            **extract_keywords**
            - Extract most common keywords from text
            - Input: text (string), top_n (integer, default=5)
            - Output: list of strings

            **format_json**
            - Format data as pretty JSON
            - Input: data (dict), indent (integer, default=2)
            - Output: formatted JSON string

            **calculate**
            - Safely evaluate mathematical expressions
            - Input: expression (string)
            - Output: float
            - Example: "2 + 2", "(10 * 5) / 2"

            ### Creating Custom Tools

            You can create custom tools by extending the ToolRegistry:

            ```python
            from ai_creator.agents.tools import Tool, default_registry

            def my_custom_tool(param1, param2):
                # Your tool logic
                return result

            tool = Tool(
                name="my_tool",
                description="Description of what it does",
                function=my_custom_tool,
                parameters={"param1": "type", "param2": "type"}
            )

            default_registry.register(tool)
            ```
            """
        )
