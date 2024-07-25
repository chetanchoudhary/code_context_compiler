AI_PROMPT = """
This document contains the compiled code of an entire project. The content is organized as follows:

1. Each file's content is preceded by a line starting with "File: " followed by the file path.
2. The actual content of each file follows immediately after the "File: " line.
3. There's an empty line between each file's content for better readability.
4. Some sensitive information may have been masked and replaced with "***MASKED***".
5. Media files (images, audio, video) are represented by placeholders: [MEDIA FILE PLACEHOLDER: filepath]
6. Binary files or files that couldn't be read as text are represented by: [BINARY FILE PLACEHOLDER: filepath]
7. Only files with specific extensions (if configured) are included in full. Others may be omitted or represented by placeholders.

When analyzing or referring to this code:
- Pay attention to the file paths to understand the project structure.
- Treat each "File: " section as a separate file in the project.
- Be aware that masked information is sensitive and should not be speculated upon.
- Consider the relationships and dependencies between different files.
- Note that media and binary files are not included in their original form, only their presence is indicated.
- If you see placeholders for media or binary files, consider their potential impact on the project without their contents.

Please process this information accordingly and use it to understand the overall structure and content of the project.

The project files and their contents begin below:

"""
