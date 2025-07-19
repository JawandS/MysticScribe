"""
Test the refactored workflow system.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from src.mysticscribe.workflows import ArchitectWorkflow, CompleteWorkflow, LegacyWorkflow


class TestBaseWorkflowFunctionality:
    """Test base workflow functionality common to all workflows."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create knowledge directory with some test files
        knowledge_dir = temp_dir / "knowledge"
        knowledge_dir.mkdir()
        (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
        (knowledge_dir / "plot.txt").write_text("Test plot")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_chapter_number_auto_detection(self, temp_project_root):
        """Test automatic chapter number detection."""
        workflow = LegacyWorkflow(temp_project_root)
        
        # No outlines exist, should return 1
        assert workflow.get_chapter_number() == 1
        
        # Create some outline files
        outlines_dir = temp_project_root / "outlines"
        outlines_dir.mkdir()
        (outlines_dir / "chapter_1.txt").touch()
        (outlines_dir / "chapter_2.txt").touch()
        
        # Should return 3 (next after 2)
        assert workflow.get_chapter_number() == 3
    
    def test_chapter_number_explicit(self, temp_project_root):
        """Test explicit chapter number specification."""
        workflow = LegacyWorkflow(temp_project_root)
        
        # Explicit number should override auto-detection
        assert workflow.get_chapter_number(5) == 5
        assert workflow.get_chapter_number("7") == 7
    
    def test_base_inputs_preparation(self, temp_project_root):
        """Test preparation of base inputs for crew execution."""
        workflow = LegacyWorkflow(temp_project_root)
        inputs = workflow.prepare_base_inputs(1)
        
        assert "chapter_number" in inputs
        assert inputs["chapter_number"] == "1"
        assert "current_year" in inputs
        assert "knowledge_context" in inputs
        assert "previous_chapter_context" in inputs
        
        # For chapter 1, should indicate no previous chapters
        assert "Chapter 1" in inputs["previous_chapter_context"]
    
    def test_prerequisites_validation(self, temp_project_root):
        """Test validation of workflow prerequisites."""
        workflow = LegacyWorkflow(temp_project_root)
        
        # Should pass with our test knowledge files
        assert workflow.validate_prerequisites(1) is True
        
        # Test with empty knowledge directory
        knowledge_dir = temp_project_root / "knowledge"
        shutil.rmtree(knowledge_dir)
        
        # Should fail with no knowledge files
        assert workflow.validate_prerequisites(1) is False


class TestArchitectWorkflow:
    """Test the Architect Workflow specifically."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create knowledge directory
        knowledge_dir = temp_dir / "knowledge"
        knowledge_dir.mkdir()
        (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @patch('src.mysticscribe.workflows.architect_workflow.Mysticscribe')
    def test_architect_workflow_new_outline(self, mock_mysticscribe, temp_project_root):
        """Test architect workflow creating new outline."""
        # Mock the crew and its components
        mock_crew_instance = Mock()
        mock_mysticscribe.return_value = mock_crew_instance
        
        mock_architect = Mock()
        mock_outline_task = Mock()
        mock_crew_instance.architect.return_value = mock_architect
        mock_crew_instance.outline_task.return_value = mock_outline_task
        
        # Mock the crew execution
        mock_outline_result = "=== CHAPTER 1 OUTLINE ===\n\nTest outline content"
        
        workflow = ArchitectWorkflow(temp_project_root)
        
        # Mock user input for new outline creation
        with patch('builtins.input', return_value='y'):  # Approve outline
            with patch('src.mysticscribe.workflows.architect_workflow.Crew') as mock_crew_class:
                mock_crew = Mock()
                mock_crew_class.return_value = mock_crew
                mock_crew.kickoff.return_value = mock_outline_result
                
                # Mock the outline management tool
                with patch('src.mysticscribe.workflows.architect_workflow.OutlineManagementTool') as mock_outline_tool_class:
                    mock_outline_tool = Mock()
                    mock_outline_tool_class.return_value = mock_outline_tool
                    mock_outline_tool._run.side_effect = [
                        "NOT EXISTS",  # No existing outline
                        "Outline saved successfully",  # Save result
                        mock_outline_result  # Load approved outline
                    ]
                    
                    result = workflow.execute(1)
        
        assert result['chapter_number'] == 1
        assert result['workflow_type'] == 'architect'
        assert 'approved_outline' in result
        assert mock_outline_result in result['approved_outline']


class TestCompleteWorkflow:
    """Test the Complete Workflow."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create knowledge directory
        knowledge_dir = temp_dir / "knowledge"
        knowledge_dir.mkdir()
        (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_complete_workflow_initialization(self, temp_project_root):
        """Test complete workflow initialization."""
        workflow = CompleteWorkflow(temp_project_root)
        assert workflow.project_root == temp_project_root
        assert workflow.chapter_manager.project_root == temp_project_root


class TestLegacyWorkflow:
    """Test the Legacy Workflow."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create knowledge directory
        knowledge_dir = temp_dir / "knowledge"
        knowledge_dir.mkdir()
        (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_legacy_workflow_initialization(self, temp_project_root):
        """Test legacy workflow initialization."""
        workflow = LegacyWorkflow(temp_project_root)
        assert workflow.project_root == temp_project_root
        assert workflow.chapter_manager.project_root == temp_project_root
    
    def test_legacy_inputs_preparation(self, temp_project_root):
        """Test legacy-specific input preparation."""
        workflow = LegacyWorkflow(temp_project_root)
        
        # Mock the tools
        with patch('src.mysticscribe.workflows.legacy_workflow.ChapterAnalysisTool') as mock_chapter_tool:
            with patch('src.mysticscribe.workflows.legacy_workflow.OutlineManagementTool') as mock_outline_tool:
                mock_chapter_instance = Mock()
                mock_chapter_tool.return_value = mock_chapter_instance
                mock_chapter_instance._run.return_value = "not found"
                
                mock_outline_instance = Mock()
                mock_outline_tool.return_value = mock_outline_instance
                mock_outline_instance._run.return_value = "NOT EXISTS"
                
                inputs = workflow._prepare_legacy_inputs(1)
        
        assert "existing_draft" in inputs
        assert "existing_outline" in inputs
        assert "approved_outline" in inputs
        assert "outline_action" in inputs
        
        # Should be empty since no existing content
        assert inputs["existing_draft"] == ""
        assert inputs["existing_outline"] == ""
        assert inputs["outline_action"] == "create_new"


if __name__ == "__main__":
    pytest.main([__file__])
