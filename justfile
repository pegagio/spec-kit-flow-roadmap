default:
    @just --list

# Run the complete Python contract suite.
test:
    mise exec -- python -m unittest discover -s tests/python -p 'test_*.py'

# Lint and format
lint:
    pre-commit run --all-files

# Build
build:
    @echo "TODO: configure build command"

# Start dev server
dev:
    @echo "TODO: configure dev command"

# Clean build artifacts
clean:
    @echo "TODO: configure clean command"
