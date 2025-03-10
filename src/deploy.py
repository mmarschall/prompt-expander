#!/usr/bin/env python3
import os
import yaml
import shutil
import sys
from jinja2 import Template, Environment, FileSystemLoader

def load_yaml_files(directory):
    """Load all YAML files from the specified directory."""
    prompts = []
    for filename in os.listdir(directory):
        if filename.endswith('.yml'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                prompt_data = yaml.safe_load(file)
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

def deploy_espanso_package(prompts, version):
    """
    Deploy the espanso package with the given prompts and version.
    
    Args:
        prompts: List of prompt data loaded from YAML files
        version: Version string for the package
    """
    # Paths
    template_path = 'src/espanso-hub/package.yml.j2'
    output_dir = f'deploy/espanso-hub/packages/llm-prompts/{version}'
    output_path = f'{output_dir}/package.yml'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
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
    
    # Copy README file
    copy_file('src/espanso-hub/README.md', f'{output_dir}/README.md')
    
    print(f"Generated {output_path} successfully!")

def deploy_textexpander_csv(prompts):
    """
    Deploy the TextExpander CSV with the given prompts.
    
    Args:
        prompts: List of prompt data loaded from YAML files
    """
    # Paths
    textexpander_template_path = 'src/textexpander/llm-prompts.csv.j2'
    textexpander_output_path = 'deploy/textexpander/llm-prompts.csv'
    
    # Render TextExpander CSV template
    package_context = {'prompts': prompts}
    textexpander_output = render_template(textexpander_template_path, package_context)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(textexpander_output_path), exist_ok=True)
    
    # Write TextExpander CSV output to file
    with open(textexpander_output_path, 'w') as file:
        file.write(textexpander_output)
    
    print(f"Generated {textexpander_output_path} successfully!")

def main():
    # Get version
    version = get_version()
    
    # Load YAML files from prompts directory
    prompts_dir = 'prompts'
    prompts = load_yaml_files(prompts_dir)
    
    # Check command line arguments
    deploy_espanso = True
    deploy_textexpander = True
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--espanso":
            deploy_textexpander = False
        elif sys.argv[1] == "--textexpander":
            deploy_espanso = False
    
    # Deploy based on arguments
    if deploy_espanso:
        deploy_espanso_package(prompts, version)
    
    if deploy_textexpander:
        deploy_textexpander_csv(prompts)

if __name__ == "__main__":
    main()
