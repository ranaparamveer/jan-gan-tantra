#!/bin/bash

# Setup pre-commit hooks
# Run this after cloning the repository

echo "🔧 Setting up pre-commit hooks..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
fi

# Install the git hooks
pre-commit install

# Run against all files to test
echo "🧪 Running pre-commit checks on all files..."
pre-commit run --all-files

echo "✅ Pre-commit hooks installed!"
echo ""
echo "Hooks will now run automatically on git commit."
echo "To run manually: pre-commit run --all-files"
