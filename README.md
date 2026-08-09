pip install mcp

Install Claude Desktop



Install uv by running pip install uv

Run "uv init my-first-mcp-server" to create a project directory

Run "uv add "mcp[cli]"" to add mcp cli in your project

Few folks may get type errors for which you can run pip install --upgrade typer to upgrade typer library to its latest version

Write code in main.py for leave management server

Install this server inside Claude desktop by running uv run mcp install main.py in the project directory

Kill any running instance of Claude from Task Manager. Restart Claude Desktop
In Claude desktop, now you will see tools from this server