# Prompt Expander

This project generates package files for Espanso from individual YAML prompt files. It uses Jinja2 templates to format the prompts into a package.yml file and creates a _manifest.yml file with the version from the VERSION file.

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

Create YAML files in the `prompts` directory with the following structure:

```yaml
trigger: ":shortcut"
replace: |
  Your prompt text here
  Can be multiple lines
label: "Optional label for the prompt"
source: "Optional source URL"
author: "Optional author name"
```

Example (`prompts/rtf.yml`):
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

### Generating the Package Files

Run the Python script to generate the package files:

```bash
# Make sure the virtual environment is activated
source venv/bin/activate

# Run the script
python deploy.py
```

This will:
1. Read the version number from the `VERSION` file
2. Read all YAML files from the `prompts` directory
3. Process them using the Jinja2 templates:
   - `src/espanso-hub/package.yml.j2` for the package.yml file
   - `src/espanso-hub/_manifest.yml.j2` for the _manifest.yml file (using the version from the VERSION file)
   - `src/textexpander/llm-prompts.csv.j2` for the TextExpander CSV file
4. Generate the final files:
   - Espanso files at `deploy/espanso-hub/packages/llm-prompts/<version>/` (where `<version>` is the content of the VERSION file)
   - TextExpander CSV file at `deploy/textexpander/llm-prompts.csv`

## Project Structure

- `prompts/`: Directory containing individual prompt YAML files
- `src/espanso-hub/package.yml.j2`: Jinja2 template for the package.yml file
- `src/espanso-hub/_manifest.yml.j2`: Jinja2 template for the _manifest.yml file
- `src/textexpander/llm-prompts.csv.j2`: Jinja2 template for the TextExpander CSV file
- `deploy.py`: Python script to generate the package files
- `VERSION`: Contains the current version number
- `deploy/espanso-hub/packages/llm-prompts/<version>/`: Output directory for Espanso files containing:
  - `package.yml`: Generated package file
  - `_manifest.yml`: Generated manifest file with version from VERSION file
  - `README.md`: Copied README file
- `deploy/textexpander/llm-prompts.csv`: Generated CSV file for TextExpander

## Using with TextExpander

In addition to Espanso, this project also generates a CSV file that can be imported into TextExpander. Here's how to import the CSV file:

1. Run the deploy script to generate the CSV file:
   ```bash
   python deploy.py
   ```

2. Open TextExpander on your computer.

3. Go to File > Import > Snippets...

4. Select "Tab-delimited text or CSV file" from the import options.

5. Navigate to the `deploy/textexpander/llm-prompts.csv` file and select it.

6. In the import dialog:
   - Make sure the columns are correctly mapped:
     - First column: Abbreviation
     - Second column: Content
     - Third column: Label
   - Choose whether to import into an existing group or create a new group.
   - Click "Import" to complete the process.

7. Your prompts are now available in TextExpander. You can use them by typing the trigger text (e.g., `:pirate`) and TextExpander will replace it with the corresponding prompt.

## Using with Espanso

This project generates an Espanso package that can be installed directly from the Espanso Hub. Here's how to install and use the package:

### Installation

1. Make sure you have [Espanso](https://espanso.org/) installed on your system.

2. Install the package using the Espanso CLI:
   ```bash
   espanso install llm-prompts
   ```

   Alternatively, if you've generated the package locally:
   ```bash
   # First, generate the package files
   python deploy.py
   
   # Then, install the package from the local directory
   espanso package install --path deploy/espanso-hub/packages/llm-prompts/0.1.0/
   ```

### Usage

Once installed, you can use the prompts in two ways:

1. Type `:prompt` to open a search menu with all available prompts
2. Use the specific trigger for each prompt directly (e.g., `:rtf`, `:bab`, `:pirate`)

After inserting a prompt template, fill in the details as needed. The cursor will be positioned at the first input field.

### Available Prompts

The package includes various prompt templates for different purposes:

- Simple prompts like `:pirate`
- Structured frameworks like Role-Task-Format (`:rtf`), Before-After-Bridge (`:bab`), and Situation-Complication-Question-Answer (`:scqa`)
- Special purpose prompts for goal setting (`:goals`), abundance mindset (`:abundance`), and startup evaluation (`:startup`)

For a complete list of available prompts and their descriptions, refer to the YAML files in the `prompts` directory.
