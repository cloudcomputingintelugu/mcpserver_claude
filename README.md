pip install mcp

Install Claude Desktop



Install uv by running pip install uv

Run "uv init my-first-mcp-server" to create a project directory

cat /etc/os-release

python3 --version

python3.11 --version

# Install UV
# -------------------
curl -LsSf https://astral.sh/uv/install.sh | sh

source ~/.bashrc

uv run --python 3.11 python --version


# Go to the MCP project

cd ~/my-first-mcp-server

uv sync

uv pip show fastmcp

uv pip show mcp

uv sync

uv pip show boto3

uv run python test_dynamodb.py

uv run python main.py
