# Filesystem MCP Server

An MCP (Model Context Protocol) server that provides tools for analyzing and cleaning up disk space on macOS systems.

## Features

- Disk space analysis and reporting
- Large file detection
- Directory size analysis
- Temporary file cleanup
- Application cache management
- Duplicate file detection
- Log file management

## Installation

```bash
# Install dependencies
uv add mcp psutil send2trash humanize
# Or install the package directly
uv add -e .
```

## Usage

This MCP server exposes several tools that can be used to analyze disk usage and clean up unnecessary files on macOS systems.

### Running the Server

```bash
# Run directly
uv run filesystem.py

# Or if installed as a package
filesystem-mcp
```

### Command Line Interface

The filesystem tool can also be used directly from the command line. By default, all operations that could modify files are in dry-run mode (they only report what would be done without actually modifying anything).

```bash
# Get disk usage summary
uv run filesystem.py disk-usage

# Find large files (default: >100MB) in your home directory
uv run filesystem.py large-files
uv run filesystem.py large-files --min-size 500 --directory /Users/username/Documents

# Analyze directory sizes (default: top 10)
uv run filesystem.py dir-sizes
uv run filesystem.py dir-sizes --top 20

# Clean temporary files (dry-run by default)
uv run filesystem.py clean-temp
# Add --execute to actually delete files
uv run filesystem.py clean-temp --execute

# Clean old files from Downloads folder (default: 30 days, dry-run)
uv run filesystem.py clean-downloads
uv run filesystem.py clean-downloads --days 60 --execute

# Clear application caches (dry-run by default)
uv run filesystem.py clear-app-cache
uv run filesystem.py clear-app-cache --app Chrome --execute

# Find duplicate files
uv run filesystem.py find-dupes
uv run filesystem.py find-dupes --directory /Users/username/Documents --max-files 2000

# List installed applications
uv run filesystem.py list-apps
```

All destructive commands (clean-temp, clean-downloads, clear-app-cache) are in dry-run mode by default and require the `--execute` flag to actually perform deletions.

### Available MCP Tools

#### Disk Analysis Tools

1. **disk_usage_summary**
   - Gets overall disk usage statistics for the system
   - Example: `await disk_usage_summary()`

2. **find_large_files**
   - Finds files larger than a specified size
   - Parameters:
     - `min_size_mb`: Minimum size in MB (default: 100)
     - `directory`: Directory to search (default: user's home directory)
   - Example: `await find_large_files(min_size_mb=500, directory="/Users/username/Documents")`

3. **analyze_directory_sizes**
   - Reports the sizes of key directories
   - Parameters:
     - `top_n`: Number of directories to report (default: 10)
   - Example: `await analyze_directory_sizes(top_n=15)`

#### Cleanup Tools

1. **clean_temp_files**
   - Cleans temporary files from common macOS locations
   - Parameters:
     - `dry_run`: Only report files without deleting (default: True)
   - Example: `await clean_temp_files(dry_run=False)`

2. **clean_downloads_folder**
   - Manages old files in the Downloads folder
   - Parameters:
     - `days_old`: Delete files older than this many days (default: 30)
     - `dry_run`: Only report files without deleting (default: True)
   - Example: `await clean_downloads_folder(days_old=60, dry_run=False)`

3. **clear_application_caches**
   - Clears application caches
   - Parameters:
     - `app_name`: Specific application to clean (optional)
     - `dry_run`: Only report caches without deleting (default: True)
   - Example: `await clear_application_caches(app_name="Chrome", dry_run=False)`

#### System Maintenance Tools

1. **find_duplicate_files**
   - Finds potential duplicate files based on size
   - Parameters:
     - `directory`: Directory to search (default: user's home directory)
     - `max_files`: Maximum number of files to process (default: 1000)
   - Example: `await find_duplicate_files(directory="/Users/username/Documents", max_files=2000)`

2. **list_installed_applications**
   - Lists installed applications with their sizes and usage dates
   - Example: `await list_installed_applications()`

### Safety Note

All delete operations include safeguards:
- Files are moved to trash rather than permanently deleted when possible
- Dry-run options are available to preview changes (enabled by default)
- System critical files are protected

## Requirements

- macOS
- Python 3.10 or higher
- Dependencies:
  - mcp>=0.2.0
  - psutil>=5.9.0
  - send2trash>=1.8.0
  - humanize>=4.0.0

## Documentation

For detailed requirements and specifications, see [REQUIREMENTS.md](./REQUIREMENTS.md)