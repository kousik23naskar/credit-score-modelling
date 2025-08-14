# src/utils/file_ops.py

import os
import sys
import pickle
import joblib
import yaml
import json
from typing import Any
from pathlib import Path
from src.exception import AppException


def save_object(file_path: str, obj: Any) -> None:
    """
    Save a Python object to a pickle file.
    Args:
        file_path (str): The path where the object will be saved.
        obj (Any): The Python object to save.
    Raises:
        AppException: If saving fails due to any exception.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)
    except Exception as e:
        raise AppException(e, sys)


def load_object(file_path: str) -> Any:
    """
    Load a Python object from a pickle file.
    Args:
        file_path (str): The path to the pickle file.
    Returns:
        Any: The loaded Python object.
    Raises:
        AppException: If the file does not exist or cannot be read.
    """
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise AppException(e, sys)


def save_yaml(file_path: str, content: dict) -> None:
    """
    Save a dictionary to a YAML file.
    Args:
        file_path (str): The path where the YAML file will be saved.
        content (dict): The dictionary to save.
    Raises:
        AppException: If saving fails due to any exception.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            yaml.dump(content, f)
    except Exception as e:
        raise AppException(e, sys)


def write_yaml(file_path: str, content: dict) -> None:
    """
    Write a dictionary to a YAML file, creating directories if necessary.
    Args:
        file_path (str): The path where the YAML file will be saved.
        content (dict): The dictionary to save.
    Raises:
        AppException: If writing fails due to any exception.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            yaml.dump(content, f)
    except Exception as e:
        raise AppException(e, sys)
    

def read_yaml(file_path: str) -> dict:
    """
    Load YAML config from file.
    Args:
        file_path (str): Path to the YAML file.
    Returns:
        dict: Parsed YAML content as a dictionary.
    Raises:
        AppException: If the file does not exist or cannot be read.
    """
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise AppException(e, sys)
    
def save_pickle(path: str, obj: object) -> None:
    """
    Save an object to a pickle file.
    Args:
        path (str): Path to the pickle file.
        obj (object): Object to be saved.
    """
    try:
        with open(path, "wb") as f:
            pickle.dump(obj, f)
    except Exception as e:
        raise AppException(e, sys)

def load_pickle(path: str) -> object:
    """
    Load an object from a pickle file.
    Args:
        path (str): Path to the pickle file.
    Returns:
        object: The loaded object.
    """
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise AppException(e, sys)
    
def save_joblib(file_path: str, obj: Any) -> None:
    """
    Saves a Python object to a file using joblib.

    Args:
        file_path (str): The full path where the object will be saved.
        obj (Any): The Python object to save.

    Raises:
        AppException: If saving fails due to any exception.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(obj, file_path)
    except Exception as e:
        raise AppException(e, sys)


def load_joblib(file_path: str) -> Any:
    """
    Loads a Python object from a joblib file.

    Args:
        file_path (str): The path to the joblib file.

    Returns:
        Any: The loaded Python object.

    Raises:
        AppException: If loading fails or the file doesn't exist.
    """
    try:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return joblib.load(file_path)
    except Exception as e:
        raise AppException(e, sys)


def convert_paths_to_str(obj):
    """
    Recursively convert Path objects to strings for JSON serialization.
    """
    if isinstance(obj, dict):
        return {k: convert_paths_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_paths_to_str(item) for item in obj]
    elif isinstance(obj, Path):
        return str(obj)
    else:
        return obj


def save_json(file_path: str, data: dict) -> None:
    """
    Saves a dictionary to a JSON file.
    Args:
        file_path (str): The path where the JSON file will be saved.
        data (dict): The dictionary to save.
    Raises:
        AppException: If saving fails due to any exception.
    """    
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        data_serializable = convert_paths_to_str(data) # To covert Path objects (Ex. pathlib.PosixPath) to strings
        with open(file_path, "w") as f:
            json.dump(data_serializable, f, indent=4)
    except Exception as e:
        raise AppException(e, sys)


def load_json(file_path: str) -> dict:
    """
    Loads a dictionary from a JSON file.
    Args:
        file_path (str): The path to the JSON file.
    Returns:
        dict: The loaded dictionary.
    Raises:
        AppException: If the file does not exist or cannot be read.
    """    
    try:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise AppException(e, sys)