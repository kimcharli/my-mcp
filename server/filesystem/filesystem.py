#!/usr/bin/env python3
"""This script provides a set of tools for managing the local filesystem."""
from typing import Dict, List, Optional
import os
import shutil
import psutil
import send2trash
import humanize
import time
import subprocess
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("filesystem")

# Constants for macOS disk cleanup
USER_HOME = os.path.expanduser("~")
"""The user's home directory."""
COMMON_CACHE_DIRS = [
    f"{USER_HOME}/Library/Caches",
    f"{USER_HOME}/Library/Logs",
    "/Library/Caches",
    "/var/log",
    f"{USER_HOME}/.cache",
]
"""A list of common cache directories on macOS."""
DOWNLOADS_DIR = f"{USER_HOME}/Downloads"
"""The user's Downloads directory."""
TEMP_DIR = "/tmp"
"""The system's temporary directory."""
SIZE_THRESHOLD_MB = 100  # Files larger than this will be flagged as large
"""The minimum size in megabytes for a file to be considered large."""

def format_size(size_bytes: int) -> str:
    """Formats a size in bytes into a human-readable string.

    Args:
        size_bytes: The size in bytes.

    Returns:
        A human-readable string representing the size.
    """
    return humanize.naturalsize(size_bytes)

def get_creation_time(path: str) -> float:
    """Gets the creation time of a file or directory.

    Args:
        path: The path to the file or directory.

    Returns:
        The creation time as a float, or 0 if the path does not exist.
    """
    try:
        return os.path.getctime(path)
    except (OSError, FileNotFoundError):
        return 0

def is_system_file(path: str) -> bool:
    """Checks if a file is a system file that should not be removed.

    Args:
        path: The path to the file.

    Returns:
        True if the file is a system file, False otherwise.
    """
    system_paths = [
        "/System",
        "/Library/Apple",
        "/bin",
        "/sbin",
        "/usr/bin",
        "/usr/sbin",
        "/usr/libexec",
    ]
    
    for sys_path in system_paths:
        if path.startswith(sys_path):
            return True
            
    return False

def is_safe_path(path: str) -> bool:
    """Checks if a path is safe to access.

    Args:
        path: The path to check.

    Returns:
        True if the path is safe, False otherwise.
    """
    return os.path.abspath(path).startswith(USER_HOME)

def get_directory_size(directory: str) -> int:
    """Calculates the total size of a directory in bytes.

    Args:
        directory: The path to the directory.

    Returns:
        The total size of the directory in bytes.
    """
    if not is_safe_path(directory):
        return 0
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.islink(file_path):
                    continue  # Skip symbolic links
                try:
                    total_size += os.path.getsize(file_path)
                except (FileNotFoundError, OSError, PermissionError):
                    continue  # Skip files that can't be accessed
    except (PermissionError, FileNotFoundError):
        pass  # Skip directories that can't be accessed
        
    return total_size

@mcp.tool()
async def disk_usage_summary() -> str:
    """Gets a summary of disk usage on the system.

    Returns:
        A string containing the disk usage summary.
    """
    partitions = psutil.disk_partitions(all=False)
    result = []
    
    for partition in partitions:
        if partition.mountpoint == '/':  # Main macOS partition
            usage = psutil.disk_usage(partition.mountpoint)
            result.append(f"Disk: {partition.device}")
            result.append(f"Mount point: {partition.mountpoint}")
            result.append(f"File system type: {partition.fstype}")
            result.append(f"Total: {format_size(usage.total)}")
            result.append(f"Used: {format_size(usage.used)} ({usage.percent}%)")
            result.append(f"Free: {format_size(usage.free)}")
            
    return "\n".join(result)

@mcp.tool()
async def find_large_files(min_size_mb: int = SIZE_THRESHOLD_MB, directory: str = USER_HOME) -> str:
    """Finds large files in the specified directory.

    Args:
        min_size_mb: The minimum size in MB to consider a file as large.
        directory: The directory to search for large files.

    Returns:
        A string containing a list of large files found.
    """

    if not is_safe_path(directory):
        return "Error: Unsafe path specified."
    min_size_bytes = min_size_mb * 1024 * 1024
    result = ["Large files found:"]
    found_files = []
    
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            try:
                file_path = os.path.join(dirpath, filename)
                if os.path.islink(file_path):
                    continue
                    
                file_size = os.path.getsize(file_path)
                if file_size >= min_size_bytes:
                    found_files.append((file_path, file_size))
            except (FileNotFoundError, PermissionError, OSError):
                continue
    
    # Sort found files by size (largest first)
    found_files.sort(key=lambda x: x[1], reverse=True)
    
    # Format the results
    for file_path, file_size in found_files[:20]:  # Limit to 20 files
        last_modified = time.strftime(
            "%Y-%m-%d", time.localtime(os.path.getmtime(file_path))
        )
        result.append(
            f"{format_size(file_size).ljust(10)} | {last_modified} | {file_path}"
        )
    
    if found_files:
        result.append(f"\nFound {len(found_files)} files larger than {min_size_mb}MB.")
    else:
        result.append(f"No files larger than {min_size_mb}MB found in {directory}")
    
    return "\n".join(result)

@mcp.tool()
async def analyze_directory_sizes(top_n: int = 10) -> str:
    """Analyzes and reports the sizes of key directories.

    Args:
        top_n: The number of directories to report.

    Returns:
        A string containing a list of the top N largest directories.
    """
    directories_to_check = [
        USER_HOME + "/Downloads",
        USER_HOME + "/Documents",
        USER_HOME + "/Desktop",
        USER_HOME + "/Library/Application Support",
        USER_HOME + "/Library/Caches",
        USER_HOME + "/Library/Logs",
        USER_HOME + "/.npm",
        USER_HOME + "/.cache",
        USER_HOME + "/.vscode",
    ]
    
    # Add any custom user directories in the home folder
    for entry in os.listdir(USER_HOME):
        full_path = os.path.join(USER_HOME, entry)
        if not is_safe_path(full_path):
            continue
        if os.path.isdir(full_path) and not entry.startswith(".") and full_path not in directories_to_check:
            directories_to_check.append(full_path)
    
    dir_sizes = []
    for directory in directories_to_check:
        if os.path.exists(directory) and os.path.isdir(directory):
            size = get_directory_size(directory)
            dir_sizes.append((directory, size))
    
    # Sort directories by size (largest first)
    dir_sizes.sort(key=lambda x: x[1], reverse=True)
    
    result = ["Directory sizes:"]
    for directory, size in dir_sizes[:top_n]:
        result.append(f"{format_size(size).ljust(12)} | {directory}")
    
    return "\n".join(result)

@mcp.tool()
async def clean_temp_files(dry_run: bool = True) -> str:
    """Cleans temporary files from common macOS locations.

    Args:
        dry_run: If True, only reports what would be deleted without actually deleting.

    Returns:
        A string containing a summary of the cleanup operation.
    """
    temp_locations = [
        TEMP_DIR,
        f"{USER_HOME}/Library/Caches",
        f"{USER_HOME}/Library/Logs",
        f"{USER_HOME}/.cache/thumbnails",
    ]
    
    total_size = 0
    deleted_count = 0
    result = ["Temporary files cleanup:"]
    
    for location in temp_locations:
        if not is_safe_path(location):
            continue
        if not os.path.exists(location):
            continue
            
        result.append(f"\nScanning {location}...")
        
        try:
            for root, dirs, files in os.walk(location):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        if is_system_file(file_path):
                            continue
                            
                        if os.path.exists(file_path) and os.path.isfile(file_path):
                            try:
                                file_size = os.path.getsize(file_path)
                                total_size += file_size
                                
                                if not dry_run:
                                    send2trash.send2trash(file_path)
                                    
                                deleted_count += 1
                            except (OSError, PermissionError):
                                continue
                    except (OSError, PermissionError):
                        continue
        except (PermissionError, FileNotFoundError):
            result.append(f"  Skipped {location} (permission denied)")
    
    action = "Would free" if dry_run else "Freed"
    result.append(f"\n{action} {format_size(total_size)} from {deleted_count} temporary files")
    
    if dry_run:
        result.append("\nThis was a dry run. No files were actually deleted.")
        result.append("To actually delete files, call this function with dry_run=False")
    
    return "\n".join(result)

@mcp.tool()
async def clean_downloads_folder(days_old: int = 30, dry_run: bool = True) -> str:
    """Cleans old files from the Downloads folder.

    Args:
        days_old: The number of days old a file must be to be deleted.
        dry_run: If True, only reports what would be deleted without actually deleting.

    Returns:
        A string containing a summary of the cleanup operation.
    """
    if not is_safe_path(DOWNLOADS_DIR):
        return "Error: Unsafe path specified."
    if not os.path.exists(DOWNLOADS_DIR):
        return f"Downloads directory not found: {DOWNLOADS_DIR}"
    
    cutoff_time = time.time() - (days_old * 86400)  # 86400 seconds in a day
    old_files = []
    
    for item in os.listdir(DOWNLOADS_DIR):
        item_path = os.path.join(DOWNLOADS_DIR, item)
        if os.path.isfile(item_path):
            try:
                mod_time = os.path.getmtime(item_path)
                if mod_time < cutoff_time:
                    file_size = os.path.getsize(item_path)
                    old_files.append((item_path, file_size, mod_time))
            except (OSError, PermissionError):
                continue
    
    total_size = sum(file[1] for file in old_files)
    result = [f"Found {len(old_files)} files older than {days_old} days in Downloads folder"]
    result.append(f"Total size: {format_size(total_size)}")
    
    if old_files:
        result.append("\nFiles that would be deleted:")
        for file_path, file_size, mod_time in old_files:
            date_str = time.strftime("%Y-%m-%d", time.localtime(mod_time))
            result.append(f"{format_size(file_size).ljust(10)} | {date_str} | {os.path.basename(file_path)}")
        
        if not dry_run:
            for file_path, _, _ in old_files:
                try:
                    send2trash.send2trash(file_path)
                except (OSError, PermissionError):
                    result.append(f"Failed to delete: {file_path}")
            
            result.append(f"\nMoved {len(old_files)} files to trash, freeing {format_size(total_size)}")
        else:
            result.append("\nThis was a dry run. No files were actually moved to trash.")
            result.append("To actually move files to trash, call with dry_run=False")
    
    return "\n".join(result)

@mcp.tool()
async def clear_application_caches(app_name: Optional[str] = None, dry_run: bool = True) -> str:
    """Clears application cache files.

    Args:
        app_name: The specific application name to clear the cache for. If None, all application caches will be cleared.
        dry_run: If True, only reports what would be deleted without actually deleting.

    Returns:
        A string containing a summary of the cleanup operation.
    """
    app_cache_dir = f"{USER_HOME}/Library/Caches"
    if not is_safe_path(app_cache_dir):
        return "Error: Unsafe path specified."
    app_cache_dir = f"{USER_HOME}/Library/Caches"
    app_support_dir = f"{USER_HOME}/Library/Application Support"
    
    result = ["Application cache cleanup:"]
    total_size = 0
    
    # Function to process a specific app cache
    def process_app_cache(cache_path: str, app: str) -> int:
        if not os.path.exists(cache_path):
            return 0
            
        app_cache_size = get_directory_size(cache_path)
        if app_cache_size > 0:
            result.append(f"{app}: {format_size(app_cache_size)}")
            
            if not dry_run:
                try:
                    for item in os.listdir(cache_path):
                        item_path = os.path.join(cache_path, item)
                        try:
                            if os.path.isfile(item_path):
                                send2trash.send2trash(item_path)
                            elif os.path.isdir(item_path):
                                send2trash.send2trash(item_path)
                        except (OSError, PermissionError):
                            continue
                except (OSError, PermissionError):
                    result.append(f"  Failed to clear some items in {app} cache")
                    
        return app_cache_size
    
    # Process specific app if specified
    if app_name:
        cache_path = os.path.join(app_cache_dir, app_name)
        app_path = os.path.join(app_support_dir, app_name)
        
        cache_size = process_app_cache(cache_path, app_name)
        total_size += cache_size
        
        # Check application support folder too
        if os.path.exists(app_path):
            app_support_cache = os.path.join(app_path, "Cache")
            if os.path.exists(app_support_cache):
                cache_size = process_app_cache(app_support_cache, f"{app_name} (App Support)")
                total_size += cache_size
    else:
        # Process all application caches
        for app in os.listdir(app_cache_dir):
            cache_path = os.path.join(app_cache_dir, app)
            if os.path.isdir(cache_path):
                cache_size = process_app_cache(cache_path, app)
                total_size += cache_size
    
    action = "Would free" if dry_run else "Freed"
    result.append(f"\n{action} {format_size(total_size)} from application caches")
    
    if dry_run:
        result.append("\nThis was a dry run. No files were actually deleted.")
        result.append("To actually delete cache files, call with dry_run=False")
    
    return "\n".join(result)

@mcp.tool()
async def find_duplicate_files(directory: str = USER_HOME, max_files: int = 1000) -> str:
    """Finds potential duplicate files based on size.

    This is a simple implementation that only looks at file sizes.
    For true duplicate detection, file content hashing would be needed.

    Args:
        directory: The directory to search for duplicates.
        max_files: The maximum number of files to process.

    Returns:
        A string containing a list of potential duplicate files.
    """
    if not is_safe_path(directory):
        return "Error: Unsafe path specified."
    result = ["Potential duplicate files (based on size):"]
    size_dict: Dict[int, List[str]] = {}
    file_count = 0
    
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if file_count >= max_files:
                break
                
            file_path = os.path.join(dirpath, filename)
            try:
                if os.path.isfile(file_path) and not os.path.islink(file_path):
                    size = os.path.getsize(file_path)
                    if size > 0:  # Ignore empty files
                        if size not in size_dict:
                            size_dict[size] = []
                        size_dict[size].append(file_path)
                        file_count += 1
            except (OSError, PermissionError):
                continue
    
    # Filter for sizes with more than one file
    duplicates = {size: files for size, files in size_dict.items() if len(files) > 1}
    
    # Sort by size (largest first)
    sorted_sizes = sorted(duplicates.keys(), reverse=True)
    
    duplicate_count = 0
    processed_count = 0
    
    for size in sorted_sizes:
        files = duplicates[size]
        if len(files) > 1:
            duplicate_count += len(files)
            processed_count += 1
            
            # Only show the first 10 groups of duplicates
            if processed_count <= 10:
                result.append(f"\nSize: {format_size(size)}")
                for file_path in files[:5]:  # Limit to 5 examples per size
                    result.append(f"  - {file_path}")
                if len(files) > 5:
                    result.append(f"  - ... and {len(files) - 5} more")
    
    result.append(f"\nFound {duplicate_count} potential duplicate files in {processed_count} size groups")
    result.append("Note: This tool only identifies files with identical sizes.")
    result.append("For true duplicate detection, content comparison would be needed.")
    
    if file_count >= max_files:
        result.append(f"\nWarning: Only processed {max_files} files. There might be more duplicates.")
    
    return "\n".join(result)

@mcp.tool()
async def list_installed_applications() -> str:
    """Lists installed applications with their sizes.

    Returns:
        A string containing a list of installed applications and their sizes.
    """
    app_dirs = [
        "/Applications",
        f"{USER_HOME}/Applications",
    ]
    
    result = ["Installed Applications:"]
    app_info = []
    
    for app_dir in app_dirs:
        if not is_safe_path(app_dir):
            continue
        if not os.path.exists(app_dir):
            continue
            
        for app in os.listdir(app_dir):
            if app.endswith(".app"):
                app_path = os.path.join(app_dir, app)
                try:
                    app_size = get_directory_size(app_path)
                    last_used = "Unknown"
                    app_info.append((app.replace(".app", ""), app_size, last_used))
                except (OSError, PermissionError):
                    continue
    
    # Sort by size (largest first)
    app_info.sort(key=lambda x: x[1], reverse=True)
    
    for name, size, last_used in app_info:
        result.append(f"{format_size(size).ljust(12)} | {last_used.ljust(20)} | {name}")
    
    result.append(f"\nTotal: {len(app_info)} applications")
    
    return "\n".join(result)


def main():
    """Run the MCP server."""
    import sys
    import argparse
    import asyncio

    # Check if any CLI arguments provided
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Mac Disk Cleanup Tools")
        subparsers = parser.add_subparsers(dest="command", help="Command to run")
        
        # disk_usage_summary command
        disk_usage_parser = subparsers.add_parser("disk-usage", help="Get disk usage summary")
        
        # find_large_files command
        large_files_parser = subparsers.add_parser("large-files", help="Find large files")
        large_files_parser.add_argument("--min-size", type=int, default=SIZE_THRESHOLD_MB,
                                       help=f"Minimum file size in MB (default: {SIZE_THRESHOLD_MB})")
        large_files_parser.add_argument("--directory", type=str, default=USER_HOME,
                                       help=f"Directory to search (default: {USER_HOME})")
        
        # analyze_directory_sizes command
        dir_sizes_parser = subparsers.add_parser("dir-sizes", help="Analyze directory sizes")
        dir_sizes_parser.add_argument("--top", type=int, default=10,
                                     help="Number of directories to report (default: 10)")
        
        # clean_temp_files command
        temp_files_parser = subparsers.add_parser("clean-temp", help="Clean temporary files")
        temp_files_parser.add_argument("--execute", action="store_true",
                                      help="Actually delete files (default: dry-run)")
        
        # clean_downloads_folder command
        downloads_parser = subparsers.add_parser("clean-downloads", help="Clean old files from Downloads folder")
        downloads_parser.add_argument("--days", type=int, default=30,
                                     help="Files older than this many days (default: 30)")
        downloads_parser.add_argument("--execute", action="store_true",
                                     help="Actually move files to trash (default: dry-run)")
        
        # clear_application_caches command
        app_cache_parser = subparsers.add_parser("clear-app-cache", help="Clear application caches")
        app_cache_parser.add_argument("--app", type=str, default=None,
                                     help="Specific application name (default: all applications)")
        app_cache_parser.add_argument("--execute", action="store_true",
                                     help="Actually delete cache files (default: dry-run)")
        
        # find_duplicate_files command
        duplicates_parser = subparsers.add_parser("find-dupes", help="Find duplicate files")
        duplicates_parser.add_argument("--directory", type=str, default=USER_HOME,
                                      help=f"Directory to search (default: {USER_HOME})")
        duplicates_parser.add_argument("--max-files", type=int, default=1000,
                                      help="Maximum number of files to process (default: 1000)")
        
        # list_installed_applications command
        apps_parser = subparsers.add_parser("list-apps", help="List installed applications")
        
        args = parser.parse_args()
        
        async def run_command():
            try:
                if args.command == "disk-usage":
                    print(await disk_usage_summary())
                    
                elif args.command == "large-files":
                    print(await find_large_files(min_size_mb=args.min_size, directory=args.directory))
                    
                elif args.command == "dir-sizes":
                    print(await analyze_directory_sizes(top_n=args.top))
                    
                elif args.command == "clean-temp":
                    # Default is dry-run (True), execute flag sets dry_run to False
                    print(await clean_temp_files(dry_run=not args.execute))
                    
                elif args.command == "clean-downloads":
                    # Default is dry-run (True), execute flag sets dry_run to False
                    print(await clean_downloads_folder(days_old=args.days, dry_run=not args.execute))
                    
                elif args.command == "clear-app-cache":
                    # Default is dry-run (True), execute flag sets dry_run to False
                    print(await clear_application_caches(app_name=args.app, dry_run=not args.execute))
                    
                elif args.command == "find-dupes":
                    print(await find_duplicate_files(directory=args.directory, max_files=args.max_files))
                    
                elif args.command == "list-apps":
                    print(await list_installed_applications())
                
            except Exception as e:
                print(f"Error: {str(e)}")
        
        asyncio.run(run_command())
        sys.exit(0)
    
    # If no CLI args, start MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()