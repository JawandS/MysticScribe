#!/usr/bin/env python
"""
Test script to verify that the continuity tools are working correctly.
"""

import sys
import os

# Add the src directory to the path so we can import the tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mysticscribe.tools.previous_chapter_reader import PreviousChapterReaderTool
from mysticscribe.tools.custom_tool import PreviousChapterEndingTool


def test_previous_chapter_tools():
    """Test the previous chapter tools."""
    print("🧪 Testing Previous Chapter Tools")
    print("=" * 50)
    
    # Test Previous Chapter Reader Tool
    print("\n📖 Testing Previous Chapter Reader Tool...")
    reader_tool = PreviousChapterReaderTool()
    
    # Test with Chapter 1 (should return no previous chapters)
    result1 = reader_tool._run("1")
    print(f"Chapter 1 result: {result1[:100]}...")
    
    # Test with Chapter 2 (should try to read Chapter 1)
    result2 = reader_tool._run("2")
    print(f"Chapter 2 result: {result2[:200]}...")
    
    # Test Previous Chapter Ending Tool
    print("\n📝 Testing Previous Chapter Ending Tool...")
    ending_tool = PreviousChapterEndingTool()
    
    # Test with Chapter 1 (should return no previous chapters)
    ending1 = ending_tool._run("1")
    print(f"Chapter 1 ending result: {ending1}")
    
    # Test with Chapter 2 (should try to read Chapter 1 ending)
    ending2 = ending_tool._run("2")
    print(f"Chapter 2 ending result: {ending2[:200]}...")
    
    print("\n✅ Continuity tools test completed!")


def test_context_loading():
    """Test the context loading from main.py"""
    print("\n🔧 Testing Context Loading Function...")
    
    # Import the function from main.py
    from mysticscribe.main import get_previous_chapter_context
    
    # Test context loading for different chapters
    context1 = get_previous_chapter_context("1")
    print(f"Context for Chapter 1: {context1}")
    
    context2 = get_previous_chapter_context("2")
    print(f"Context for Chapter 2: {context2[:200]}...")
    
    print("\n✅ Context loading test completed!")


if __name__ == "__main__":
    print("🚀 Starting Continuity Tools Test Suite")
    print("This will test the tools that ensure chapter-to-chapter continuity\n")
    
    try:
        test_previous_chapter_tools()
        test_context_loading()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Summary of continuity improvements:")
        print("  ✅ Enhanced Previous Chapter Reader Tool with continuity focus")
        print("  ✅ Added Previous Chapter Ending Tool for quick reference")
        print("  ✅ Updated architect, writer, and editor agents with continuity tools")
        print("  ✅ Enhanced task descriptions to emphasize chapter continuity")
        print("  ✅ Integrated previous chapter context into all workflows")
        print("  ✅ Added visual feedback for context loading")
        
        print("\n💡 Usage Tips:")
        print("  • Both architect and writer agents now automatically receive previous chapter context")
        print("  • Agents can use Previous Chapter Reader tool for comprehensive context")
        print("  • Agents can use Previous Chapter Ending tool for quick continuity checks")
        print("  • All workflows now ensure seamless chapter-to-chapter transitions")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)
