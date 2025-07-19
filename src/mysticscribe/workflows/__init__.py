"""
Workflow management for the MysticScribe system.

This module contains different workflow implementations for chapter generation,
from simple linear workflows to complex interactive ones with approval gates.
"""

from .base_workflow import BaseWorkflow
from .architect_workflow import ArchitectWorkflow
from .complete_workflow import CompleteWorkflow
from .legacy_workflow import LegacyWorkflow

__all__ = [
    'BaseWorkflow',
    'ArchitectWorkflow', 
    'CompleteWorkflow',
    'LegacyWorkflow'
]
