"""
UI components for skill management.
"""

import gradio as gr
import json
import tempfile
import os
from pathlib import Path
from typing import List
from ai_creator import (
    skill_registry,
    SkillLoader,
    create_skill_template,
)
from ai_creator.skills.builtin import register_all_builtin_skills


def create_skills_interface():
    """Create the skills management interface."""

    gr.Markdown("## Skills Management")
    gr.Markdown("Create, import, and manage skills for your agents.")

    with gr.Tabs():
        # Tab 1: Browse Skills
        with gr.Tab("📚 Browse Skills"):
            create_browse_skills_tab()

        # Tab 2: Import Skills
        with gr.Tab("📥 Import Skills"):
            create_import_skills_tab()

        # Tab 3: Create Skills
        with gr.Tab("✨ Create Skills"):
            create_create_skills_tab()

        # Tab 4: Skill Statistics
        with gr.Tab("📊 Statistics"):
            create_statistics_tab()


def create_browse_skills_tab():
    """Create the browse skills tab."""
    gr.Markdown("### Browse Available Skills")
    gr.Markdown("View and manage all registered skills in the system.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("**Actions**")

            load_builtin_btn = gr.Button("📦 Load All Built-in Skills", variant="primary")
            refresh_btn = gr.Button("🔄 Refresh List", variant="secondary")
            clear_registry_btn = gr.Button("🗑️ Clear Registry", variant="stop")

            gr.Markdown("**Filter**")
            category_filter = gr.Dropdown(
                choices=["All", "code", "research", "communication", "data", "creative", "analysis", "automation", "custom"],
                value="All",
                label="Category Filter"
            )

            search_box = gr.Textbox(
                label="Search Skills",
                placeholder="Enter skill name or description..."
            )
            search_btn = gr.Button("🔍 Search")

        with gr.Column(scale=2):
            gr.Markdown("**Skills Registry**")

            registry_status = gr.Textbox(
                label="Status",
                interactive=False,
                value="Click 'Load All Built-in Skills' to get started"
            )

            skills_display = gr.Textbox(
                label="Available Skills",
                lines=15,
                interactive=False,
                value="No skills loaded. Load built-in skills or import custom skills."
            )

            skill_count = gr.Textbox(
                label="Total Skills",
                interactive=False
            )

    with gr.Accordion("Skill Details", open=False):
        skill_selector = gr.Dropdown(
            label="Select Skill",
            choices=[],
            interactive=True
        )

        skill_info_display = gr.JSON(label="Skill Information")

    # Load built-in skills
    def load_builtin_skills():
        try:
            register_all_builtin_skills(skill_registry)
            skills = skill_registry.list_skills()
            count = len(skills)

            display_text = format_skills_display(skills)

            return (
                f"✅ Loaded {count} built-in skills successfully!",
                display_text,
                str(count),
                skills
            )
        except Exception as e:
            return f"❌ Error: {str(e)}", "", "0", []

    load_builtin_btn.click(
        fn=load_builtin_skills,
        outputs=[registry_status, skills_display, skill_count, skill_selector]
    )

    # Refresh skills list
    def refresh_skills():
        skills = skill_registry.list_skills()
        count = len(skills)
        display_text = format_skills_display(skills)
        return display_text, str(count), skills

    refresh_btn.click(
        fn=refresh_skills,
        outputs=[skills_display, skill_count, skill_selector]
    )

    # Clear registry
    def clear_registry():
        skill_registry.clear()
        return (
            "Registry cleared",
            "No skills in registry. Load or import skills.",
            "0",
            []
        )

    clear_registry_btn.click(
        fn=clear_registry,
        outputs=[registry_status, skills_display, skill_count, skill_selector]
    )

    # Filter by category
    def filter_by_category(category):
        if category == "All":
            skills = skill_registry.list_skills()
        else:
            from ai_creator.skills.base import SkillCategory
            try:
                cat_enum = SkillCategory(category)
                skills = skill_registry.list_skills(category=cat_enum)
            except:
                skills = []

        display_text = format_skills_display(skills)
        return display_text, str(len(skills)), skills

    category_filter.change(
        fn=filter_by_category,
        inputs=[category_filter],
        outputs=[skills_display, skill_count, skill_selector]
    )

    # Search skills
    def search_skills(query):
        if not query:
            skills = skill_registry.list_skills()
        else:
            skills = skill_registry.search(query)

        display_text = format_skills_display(skills)
        return display_text, str(len(skills)), skills

    search_btn.click(
        fn=search_skills,
        inputs=[search_box],
        outputs=[skills_display, skill_count, skill_selector]
    )

    # Show skill details
    def show_skill_details(skill_name):
        if not skill_name:
            return {}

        try:
            info = skill_registry.get_info(skill_name)
            return info
        except:
            return {"error": f"Skill '{skill_name}' not found"}

    skill_selector.change(
        fn=show_skill_details,
        inputs=[skill_selector],
        outputs=[skill_info_display]
    )


def create_import_skills_tab():
    """Create the import skills tab."""
    gr.Markdown("### Import Custom Skills")
    gr.Markdown("Upload a Python file containing a custom skill to import it into the registry.")

    with gr.Row():
        with gr.Column():
            gr.Markdown("**Upload Skill File**")
            gr.Markdown("""
            Upload a Python (.py) file that contains:
            - A class that inherits from `Skill`
            - A `skill_config` variable (optional)

            The skill will be automatically loaded and registered.
            """)

            file_upload = gr.File(
                label="Select Python File",
                file_types=[".py"],
                type="filepath"
            )

            import_btn = gr.Button("📥 Import Skill", variant="primary")

            import_status = gr.Textbox(
                label="Import Status",
                lines=5,
                interactive=False
            )

        with gr.Column():
            gr.Markdown("**Imported Skill Info**")

            imported_skill_info = gr.JSON(label="Skill Details")

            register_btn = gr.Button("✅ Register to System", variant="secondary", visible=False)
            register_status = gr.Textbox(
                label="Registration Status",
                interactive=False,
                visible=False
            )

    # Import skill from file
    import_skill_cache = {"skill": None}

    def import_skill_file(filepath):
        if not filepath:
            return "❌ No file selected", {}, gr.update(visible=False), gr.update(visible=False)

        try:
            # Load skill from file
            loader = SkillLoader()
            skill = loader.load_from_file(filepath)

            # Cache the skill
            import_skill_cache["skill"] = skill

            # Get skill info
            info = skill.get_info()

            status = f"""✅ Skill loaded successfully!

Name: {info['name']}
Description: {info['description']}
Category: {info['category']}
Version: {info['version']}
Author: {info['author']}

Click 'Register to System' to add this skill to the registry."""

            return (
                status,
                info,
                gr.update(visible=True),
                gr.update(visible=True)
            )

        except Exception as e:
            return (
                f"❌ Error loading skill: {str(e)}",
                {"error": str(e)},
                gr.update(visible=False),
                gr.update(visible=False)
            )

    import_btn.click(
        fn=import_skill_file,
        inputs=[file_upload],
        outputs=[import_status, imported_skill_info, register_btn, register_status]
    )

    # Register imported skill
    def register_imported_skill():
        skill = import_skill_cache.get("skill")
        if not skill:
            return "❌ No skill to register"

        try:
            skill_registry.register(skill)
            return f"✅ Skill '{skill.config.name}' registered successfully!"
        except Exception as e:
            return f"❌ Error registering skill: {str(e)}"

    register_btn.click(
        fn=register_imported_skill,
        outputs=[register_status]
    )

    # Example skill template
    with gr.Accordion("📖 Skill File Format", open=False):
        gr.Markdown("""
        ### Example Skill File

        Your Python file should look like this:

        ```python
        from ai_creator import Skill, SkillConfig, SkillResult, SkillCategory

        skill_config = SkillConfig(
            name="my_custom_skill",
            description="Does something useful",
            category=SkillCategory.CUSTOM,
            version="1.0.0",
            author="Your Name"
        )

        class MyCustomSkill(Skill):
            def __init__(self, config=skill_config):
                super().__init__(config)

            def execute(self, input_data, **kwargs):
                try:
                    # Your skill logic here
                    result = f"Processed: {input_data}"

                    return SkillResult(
                        skill_name=self.config.name,
                        success=True,
                        output=result
                    )
                except Exception as e:
                    return SkillResult(
                        skill_name=self.config.name,
                        success=False,
                        output=None,
                        error=str(e)
                    )
        ```
        """)


def create_create_skills_tab():
    """Create the create skills tab."""
    gr.Markdown("### Create New Skills")
    gr.Markdown("Generate a skill template to get started with your custom skill.")

    with gr.Row():
        with gr.Column():
            gr.Markdown("**Skill Configuration**")

            skill_name = gr.Textbox(
                label="Skill Name",
                placeholder="e.g., DataProcessor"
            )

            skill_description = gr.Textbox(
                label="Description",
                placeholder="What does this skill do?",
                lines=2
            )

            skill_category = gr.Dropdown(
                choices=["code", "research", "communication", "data", "creative", "analysis", "automation", "custom"],
                value="custom",
                label="Category"
            )

            skill_author = gr.Textbox(
                label="Author",
                value="Your Name"
            )

            generate_btn = gr.Button("✨ Generate Template", variant="primary")

        with gr.Column():
            gr.Markdown("**Generated Template**")

            template_output = gr.Code(
                label="Skill Template",
                language="python",
                lines=20
            )

            download_btn = gr.Button("💾 Download Template", variant="secondary")
            download_file = gr.File(label="Download", visible=False)

    # Generate template
    template_cache = {"code": ""}

    def generate_template(name, description, category, author):
        if not name or not description:
            return "# Error: Please provide skill name and description"

        try:
            # Generate template code
            template = create_skill_template(
                name=name,
                description=description,
                category=category
            )

            # Update author in template
            template = template.replace('"Your Name"', f'"{author}"')

            # Cache the template
            template_cache["code"] = template

            return template

        except Exception as e:
            return f"# Error generating template: {str(e)}"

    generate_btn.click(
        fn=generate_template,
        inputs=[skill_name, skill_description, skill_category, skill_author],
        outputs=[template_output]
    )

    # Download template
    def download_template():
        code = template_cache.get("code", "")
        if not code:
            return None

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name

        return temp_path

    download_btn.click(
        fn=download_template,
        outputs=[download_file]
    )


def create_statistics_tab():
    """Create the statistics tab."""
    gr.Markdown("### Skill Statistics")
    gr.Markdown("View execution statistics for registered skills.")

    with gr.Row():
        with gr.Column(scale=1):
            refresh_stats_btn = gr.Button("🔄 Refresh Statistics", variant="primary")

            skill_stats_selector = gr.Dropdown(
                label="Select Skill",
                choices=[],
                value=None
            )

        with gr.Column(scale=2):
            gr.Markdown("**Overall Statistics**")

            overall_stats = gr.Textbox(
                label="Registry Statistics",
                lines=5,
                interactive=False
            )

            gr.Markdown("**Individual Skill Stats**")

            individual_stats = gr.JSON(label="Skill Statistics")

    # Refresh statistics
    def refresh_statistics():
        skills = skill_registry.list_skills()

        if not skills:
            return "No skills in registry", {}, []

        total_skills = len(skills)
        by_category = skill_registry.list_by_category()

        overall_text = f"""Total Skills: {total_skills}

Skills by Category:"""

        for category, skill_list in by_category.items():
            overall_text += f"\n  {category}: {len(skill_list)}"

        return overall_text, {}, skills

    refresh_stats_btn.click(
        fn=refresh_statistics,
        outputs=[overall_stats, individual_stats, skill_stats_selector]
    )

    # Show individual skill stats
    def show_individual_stats(skill_name):
        if not skill_name:
            return {}

        try:
            stats = skill_registry.get_stats(skill_name)
            return stats
        except:
            return {"error": f"No statistics available for '{skill_name}'"}

    skill_stats_selector.change(
        fn=show_individual_stats,
        inputs=[skill_stats_selector],
        outputs=[individual_stats]
    )


def format_skills_display(skills: List[str]) -> str:
    """Format skills list for display."""
    if not skills:
        return "No skills available"

    # Group by category
    by_category = {}
    for skill_name in skills:
        try:
            info = skill_registry.get_info(skill_name)
            category = info.get('category', 'unknown')

            if category not in by_category:
                by_category[category] = []

            by_category[category].append({
                'name': skill_name,
                'description': info.get('description', '')
            })
        except:
            continue

    # Format output
    output = []
    for category, skill_list in sorted(by_category.items()):
        output.append(f"\n═══ {category.upper()} ═══")
        for skill in skill_list:
            output.append(f"\n• {skill['name']}")
            output.append(f"  {skill['description']}")

    return "\n".join(output)
