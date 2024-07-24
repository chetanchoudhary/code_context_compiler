# Code Context Compiler

Code Context Compiler is a powerful CLI tool that scans a code project and creates a single file containing the entire project code with file-wise separation. The tool also masks sensitive information in the code to enhance security and provides various customization options.

## Features

- Scans an entire project directory
- Processes all file types by default
- Compiles all code files into a single output file
- Masks sensitive information such as passwords, API keys, and tokens
- Respects `.gitignore` patterns and custom ignore patterns
- Supports custom configuration via YAML files
- Asynchronous file processing for improved performance
- Progress indicator for large projects
- Multiple output formats: text, JSON, and YAML
- Option to only process files tracked by Git
- Customizable file extension filtering (optional)
- Customizable masking patterns
- AI-friendly output format, ideal for feeding project context to language models

## Use Cases

### Feeding Project Context to Language Models (LLMs)

Code Context Compiler is designed to be AI-friendly, making it an excellent tool for preparing entire project contexts for language models. Some key benefits include:

1. **Comprehensive Context**: By compiling the entire project into a single file, you provide LLMs with a complete view of your codebase, enabling more accurate and context-aware responses.

2. **Structured Output**: The file-wise separation in the output allows LLMs to understand the project structure and relationships between different files.

3. **Sensitive Information Protection**: With the built-in masking feature, you can safely share your project context with AI models without exposing sensitive data.

4. **Customizable Content**: Use the configuration options to include only the files and information relevant to your AI-related tasks.

5. **Multiple Output Formats**: Choose between text, JSON, or YAML output to best suit your LLM integration needs.

By using Code Context Compiler to prepare your project data, you can enhance the effectiveness of AI-powered code analysis, documentation generation, code review assistance, and other AI-driven development tools.

## Installation

## Using Pip

You can install Code Context Compiler directly from PyPI:

```
pip install code_context_compiler
```

## Usage

After installation, you can use the tool directly from the command line:

```
code_context_compiler [OPTIONS] PROJECT_PATH OUTPUT_FILE
```

...

## Using Git clone

To install Code Context Compiler, you need Python 3.8 or later and Poetry. Follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/code_context_compiler.git
   cd code_context_compiler
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Usage

To use Code Context Compiler, run the following command:

```
poetry run code_context_compiler [OPTIONS] PROJECT_PATH OUTPUT_FILE
```

Arguments:
- `PROJECT_PATH`: Path to the project to scan
- `OUTPUT_FILE`: Path to the output file

Options:
- `--config-file PATH`: Path to the configuration file
- `--output-format [text|json|yaml]`: Output format (default: text)
- `--help`: Show this message and exit

Example:
```
poetry run code_context_compiler /path/to/your/project /path/to/output/file.txt --config-file config.yaml --output-format json
```

## Configuration

You can customize the behavior of Code Context Compiler by creating a YAML configuration file. Here's an example configuration:

```yaml
ignore_patterns:
  - "*.log"
  - "*.tmp"
file_extensions:
  - ".py"
  - ".js"
  - ".java"
mask_patterns:
  - 'password\s*=\s*["\'].*?["\']'
  - 'api[_-]?key\s*=\s*["\'].*?["\']'
use_git: true
```

- `ignore_patterns`: List of file patterns to ignore
- `file_extensions`: List of file extensions to process (if empty, all files are processed)
- `mask_patterns`: List of regex patterns to mask sensitive information
- `use_git`: Boolean to only process Git-tracked files

Note: If `file_extensions` is not specified or is an empty list, the tool will process all file types.

## Development

To set up the development environment:

1. Ensure you have Python 3.8+ and Poetry installed.
2. Clone the repository and navigate to the project directory.
3. Install dependencies:
   ```
   poetry install
   ```
4. Run tests:
   ```
   poetry run pytest
   ```
5. Run tests with coverage:
   ```
   poetry run pytest --cov=code_context_compiler
   ```

## Contributing

Contributions to Code Context Compiler are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.