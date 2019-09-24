"""Manages boxes available for constructing flows"""
import subprocess
import sys
from typing import Dict, List

from pymongo import MongoClient


def install(package_name: str, box_spec: Dict) -> int:
    """Installs package by given name in the current environment

    Args:
        package_name: Name of the package to install

    Returns:
        pip return code

    """
    try:
        subprocess.check_call(sys.executable, '-m', 'pip', 'install', package_name)
    except subprocess.CalledProcessError as exc:
        return exc.returncode

    connection = MongoClient()
    db = connection.box_flow
    collection = db.box_info
    collection.insert_one({'packageName': package_name, 'boxSpec': box_spec})

    return 0


def list_boxes() -> List[str]:
    """Lists all the boxes installed in the current environment"""
    connection = MongoClient()
    db = connection.box_flow
    collection = db.box_info

    box_list = list()
    for box in collection.find():
        box_list.append(box['boxSpec'])

    return box_list
