#!/usr/bin/env python3
import os
import yaml
import shutil
from jinja2 import Template, Environment, FileSystemLoader

def load_yaml_files(directory):
    """Load all YAML files from the specified directory."""
    prompts = []
    for filename in os.listdir(directory):
        if filename.endswith('.yml'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                prompt_data = yaml.safe_load(file)
                # Ensure the trigger doesn't have a colon prefix in the data structure
                if 'trigger' in prompt_data and prompt_data['trigger'].startswith(':'):
                    prompt_data['trigger'] = prompt_data['trigger'][1:]
                prompts.append(prompt_data)
    return prompts

def render_template(template_path, context):
    """Render the Jinja2 template with the provided context."""
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    
    # Render the template
    return template.render(**context)

def get_version():
    """Read version from VERSION file."""
    try:
        with open('VERSION', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("WARNING: VERSION file not found. Using default version 0.1.0.")
        return "0.1.0"

def copy_file(source_path, dest_path):
    """Copy a file from source to destination."""
    shutil.copy(source_path, dest_path)
    print(f"Copied {source_path} to {dest_path}")

def main():
    # Get version
    version = get_version()
    
    # Paths
    prompts_dir = 'src/prompts'
    template_path = 'src/espanso-hub/package.yml.j2'
    output_dir = f'deploy/espanso-hub/packages/llm-prompts/{version}'
    output_path = f'{output_dir}/package.yml'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load YAML files
    prompts = load_yaml_files(prompts_dir)
    
    # Add filename as a property for each prompt (for use in templates)
    for i, prompt in enumerate(prompts):
        # Find the filename for this prompt
        for filename in os.listdir(prompts_dir):
            if filename.endswith('.yml'):
                filepath = os.path.join(prompts_dir, filename)
                with open(filepath, 'r') as file:
                    data = yaml.safe_load(file)
                    if data.get('trigger') == prompt.get('trigger'):
                        prompts[i]['_filename'] = os.path.splitext(filename)[0]
                        break
    
    # Render package.yml template
    package_context = {'prompts': prompts}
    package_output = render_template(template_path, package_context)
    
    # Write package.yml output to file
    with open(output_path, 'w') as file:
        file.write(package_output)
    
    # Render _manifest.yml template
    manifest_template_path = 'src/espanso-hub/_manifest.yml.j2'
    manifest_context = {'version': version}
    manifest_output = render_template(manifest_template_path, manifest_context)
    
    # Write _manifest.yml output to file
    manifest_output_path = f'{output_dir}/_manifest.yml'
    with open(manifest_output_path, 'w') as file:
        file.write(manifest_output)
    copy_file('src/espanso-hub/README.md', f'{output_dir}/README.md')
    
    # Render TextExpander CSV template
    textexpander_template_path = 'src/textexpander/llm-prompts.csv.j2'
    textexpander_output_path = 'deploy/textexpander/llm-prompts.csv'
    textexpander_output = render_template(textexpander_template_path, package_context)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(textexpander_output_path), exist_ok=True)
    
    # Write TextExpander CSV output to file
    with open(textexpander_output_path, 'w') as file:
        file.write(textexpander_output)
    
    print(f"Generated {output_path} successfully!")
    print(f"Generated {textexpander_output_path} successfully!")

if __name__ == "__main__":
    main()
