# Mac Disk Cleanup MCP Server Requirements

## Overview
This document outlines the requirements for the Filesystem MCP Server, which provides tools for analyzing and cleaning up disk space on macOS systems through the Model Context Protocol (MCP).

## Functional Requirements

### 1. Disk Space Analysis
- **Disk Usage Summary**: Provide an overview of total, used, and available disk space on the system
  - Report disk partitions with mount points, file system types, and usage statistics
  - Present data in human-readable format (GB, MB, etc.)
  - Display percentage of disk space used

- **Large Files Detection**: Identify and list large files that might be candidates for deletion
  - Allow configurable threshold for "large" files (default: 100MB)
  - Sort results by file size (largest first)
  - Include file modification dates
  - Limit results to a reasonable number (e.g., top 20 files)

- **Directory Size Analysis**: Calculate and report the size of key directories
  - Analyze common directories (Downloads, Documents, Desktop, etc.)
  - Allow customizable number of top directories to report
  - Sort results by directory size (largest first)
  - Handle permission errors gracefully

### 2. Cleanup Operations
- **Temporary Files Cleanup**: Identify and optionally remove temporary files and caches
  - Target system temporary directories and user cache locations
  - Calculate potential space savings before deletion
  - Provide "dry-run" option to preview changes
  - Move files to trash rather than permanent deletion when possible
  - Skip system-critical files

- **Downloads Folder Management**: Clean old files from the Downloads folder
  - Allow configurable age threshold for "old" files (default: 30 days)
  - Calculate potential space savings before deletion
  - List files that would be affected
  - Provide "dry-run" option
  - Move files to trash rather than permanent deletion

- **Application Cache Cleanup**: Clear application caches
  - Allow targeting specific applications or all applications
  - Report cache size per application
  - Calculate total potential space savings
  - Provide "dry-run" option
  - Handle permission errors gracefully

### 3. System Maintenance
- **Duplicate File Detection**: Find potential duplicate files
  - Identify files with identical sizes (initial implementation)
  - Group potential duplicates by size
  - Sort results by file size (largest potential savings first)
  - Allow configurable limit to number of files processed
  - Note limitations of size-based duplication detection

- **Application Analysis**: List installed applications with their sizes
  - Include both system and user applications
  - Report application size
  - Include last-used date when available
  - Sort by size (largest first)

## Technical Requirements

### 1. Implementation Details
- Implement using the Model Context Protocol (MCP) framework
- Follow the FastMCP pattern used in other MCP servers
- Use asynchronous functions for all tools
- Provide clear documentation for each tool function
- Return results in human-readable, well-formatted strings
- Use proper error handling throughout

### 2. Safety Considerations
- Never permanently delete files without explicit confirmation
- Use send2trash for moving files to trash when possible
- Default all deletion operations to "dry run" mode
- Include safeguards against deleting system files
- Handle permission errors gracefully
- Provide clear warnings about potential data loss

### 3. Performance Considerations
- Implement reasonable file count limits for intensive operations
- Use efficient algorithms for directory traversal
- Handle large file systems gracefully
- Provide progress indication for long-running operations when possible

### 4. Dependencies
- psutil: For system resource monitoring
- send2trash: For safely moving files to trash
- humanize: For formatting file sizes in human-readable format
- Standard Python libraries (os, shutil, etc.)

## Success Criteria
- All tool functions execute without errors on macOS
- Accurate reporting of disk usage statistics
- Successful identification of cleanup opportunities
- Safe execution of cleanup operations
- Clear and user-friendly output from all tools