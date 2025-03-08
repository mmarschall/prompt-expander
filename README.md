# Prompt Expander

This project generates a package.yml file for Espanso from individual YAML prompt files. It uses a Jinja2 template to format the prompts and combines them into a single package.yml file.

## Prerequisites

- Python 3.6 or higher
- Git (optional, for cloning the repository)

## Getting Started

Follow these steps to set up and use the prompt expander:

### 1. Clone or download the repository (optional)

```bash
git clone git@github.com:mmarschall/prompt-expander.git
cd prompt-expander
```

### 2. Create a virtual environment

Create a Python virtual environment to isolate the project dependencies:

```bash
python -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

Install the required Python packages:

```bash
pip install pyyaml jinja2
```

## Usage

### Adding Prompt Files

Create YAML files in the `src/prompts` directory with the following structure:

```yaml
trigger: ":shortcut"
replace: |
  Your prompt text here
  Can be multiple lines
label: "Optional label for the prompt"
source: "Optional source URL"
author: "Optional author name"
```

Example (`src/prompts/rtf.yml`):
```yaml
trigger: ":rtf"
replace: |
  Role: $|$
  Task: 
  Format:
label: "Role - Task - Format"
source: "https://www.linkedin.com/posts/jeremygrandillon_5-chatgpt-prompt-frameworks-that-make-your-activity-7301956962898837504-NR_i"
author: ""
```

### Generating the package.yml File

Run the Python script to generate the package.yml file:

```bash
# Make sure the virtual environment is activated
source venv/bin/activate

# Run the script
python generate_package.py
```

This will:
1. Read the version number from the `VERSION` file
2. Read all YAML files from the `src/prompts` directory
3. Process them using the Jinja2 template (`src/espanso-hub/package.yml.j2`)
4. Generate the final package.yml file at `deploy/espanso-hub/packages/llm-prompts/<version>/package.yml` (where `<version>` is the content of the VERSION file)

## Project Structure

- `src/prompts/`: Directory containing individual prompt YAML files
- `src/espanso-hub/package.yml.j2`: Jinja2 template for the package.yml file
- `generate_package.py`: Python script to generate the package.yml file
- `VERSION`: Contains the current version number
- `deploy/espanso-hub/packages/llm-prompts/<version>/package.yml`: Output file (where `<version>` is the content of the VERSION file)
