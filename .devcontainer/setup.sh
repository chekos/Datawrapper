#!/bin/bash
set -e

echo "🚀 Setting up Datawrapper development environment..."

# Install uv package manager
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Install all project dependencies
echo "📚 Installing project dependencies..."
uv sync --all-groups

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
uv run pre-commit install
