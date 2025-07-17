#!/usr/bin/env python
"""
Test script to validate the crew and task setup
"""

from mysticscribe.crew import Mysticscribe
import os
import sys

def test_architect_agent():
    """Test the architect agent and outline task"""
    print("Testing architect agent and outline task...")
    
    # Initialize crew
    crew_instance = Mysticscribe()
    
    # Test architect agent
    architect = crew_instance.architect()
    assert architect is not None, "Failed to create architect agent"
    print("✓ Architect agent created successfully")
    
    # Test outline task
    outline_task = crew_instance.outline_task()
    assert outline_task is not None, "Failed to create outline task"
    print("✓ Outline task created successfully")
    
    # Validate agent tools
    assert len(architect.tools) > 0, "Architect agent has no tools"
    tool_names = [tool.name for tool in architect.tools]
    print(f"✓ Architect agent has tools: {tool_names}")
    
    # Validate OutlineManagementTool is present
    outline_tool_present = any("Outline Management" in tool.name for tool in architect.tools)
    assert outline_tool_present, "OutlineManagementTool is not available to the architect"
    print("✓ OutlineManagementTool is available to the architect")
    
    # Validate task configuration
    assert outline_task.agent == architect, "Outline task is not assigned to architect agent"
    print("✓ Outline task is properly assigned to architect agent")
    
    print("\nAll tests passed! The crew and task setup should be valid.")
    return True

if __name__ == "__main__":
    test_architect_agent()
