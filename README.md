# Haystack AI Skills

A curated collection of AI agent skills designed for building retrieval-augmented generation (RAG) systems and advanced search applications with the Haystack framework.

## What are Skills?

Skills are structured definitions that empower AI agents to execute specific tasks. Each skill includes:
- **Instructions**: Comprehensive guidance on when and how to apply the skill
- **Examples**: Reference implementations and usage patterns
- **Scripts**: Reusable code components for common operations

This repository adheres to the [AgentSkills](https://agentskills.io/home) specification for skill definitions and organization.

> [!TIP]
> If your agent lacks skill support, you can use [`agents/AGENTS.md`](agents/AGENTS.md) as an alternative.


## Available Skills
This repository includes the following skills:

| Name | Description | Installation |
| --- | --- | --- |
| [haystack](skills/haystack/SKILL.md) | Contains core haystack skill | `npx skills add srini047/haystack-skills@haystack` |

Note: `npx skills add <owner/repo@skill>` is standard command for installing skills from any public repository. 

### Haystack
- **Directory**: `skills/haystack/`
- **Purpose**: Construct RAG systems, implement semantic search, and develop document processing pipelines

## Installation

These Haystack skills are compatible with Claude Code, Gemini CLI, and Cursor.

### Claude Code

1. Register this repository as a plugin marketplace:
   ```
   /plugin marketplace add haystack/skills
   ```

2. Install a specific skill:
   ```
   /plugin install <skill-name>@haystack/skills
   ```

   Example:
   ```
   /plugin install haystack@haystack/skills
   ```

### Gemini CLI

1. This repository includes a `gemini-extension.json` file for seamless Gemini CLI integration.

2. Install locally:
   ```
   gemini extensions install . --consent
   ```

   Or install directly from GitHub:
   ```
   gemini extensions install https://github.com/srini047/haystack-skills.git --consent
   ```

### Cursor

This repository provides Cursor plugin manifests:

- `.cursor-plugin/plugin.json`

Install via the Cursor plugin interface using either the repository URL or a local checkout.
