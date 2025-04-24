"""
Utility functions for the trading system.
"""
import os
import json
import uuid
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("trading-mcp.utils")

def generate_id(prefix: str) -> str:
    """Generate a unique ID with prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def format_money(amount: float) -> str:
    """Format a monetary value."""
    if amount < 0:
        return f"-${abs(amount):.2f}"
    return f"${amount:.2f}"

def load_json_file(path: Any, default: Any = None) -> Any:
    """Load data from a JSON file."""
    try:
        # Ensure path is a Path object
        if isinstance(path, str):
            path = Path(path)
        if not path.exists():
            logger.info(f"File not found: {path}")
            return default
        
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {path}: {e}")
        return default

def save_json_file(file_path: Path, data: Any) -> bool:
    """Save data to a JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {e}")
        return False

def get_env_var(name: str, default: Any = None, required: bool = False) -> Any:
    """Get environment variable with type conversion."""
    value = os.getenv(name)
    
    if value is None:
        if required:
            raise ValueError(f"Required environment variable {name} not set")
        return default
    
    # Convert to appropriate type based on default
    if isinstance(default, bool):
        return value.upper() in ("TRUE", "YES", "1")
    elif isinstance(default, int):
        return int(value)
    elif isinstance(default, float):
        return float(value)
    
    return value