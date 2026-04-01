import pytest
import json
from unittest.mock import MagicMock, patch
# Import the class from the evaluation folder
from evaluation.fuse_scorer import FUSEScoringSystem

@pytest.fixture
def evaluator():
    """Initialize the test object with a mock API key."""
    return FUSEScoringSystem(api_key="sk-mock-key-for-testing")

def test_evaluation_logic_6_dimensions(evaluator):
    """
    Core Test: Verify that the average score is calculated correctly 
    when the LLM returns exactly 6 dimensions.
    """
    # 1. Mock the 6-dimension standard JSON string returned by the LLM
    mock_llm_json = {
        "SS": 8, "NII": 7, "CS": 6, "STS": 9, "TS": 5, "PD": 7
    }
    mock_content = json.dumps(mock_llm_json)

    # 2. Patch the OpenAI network request to return our mock data
    with patch.object(evaluator.client.chat.completions, 'create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=mock_content))]
        mock_create.return_value = mock_response

        # Execute the function under test
        results = evaluator.evaluate_news("original news text", "evolved news text")

        # 3. Assertions to verify logic
        # Verify result contains the 6 original dimensions plus 'Total_Deviation'
        assert len(results) == 7 
        
        # Verify calculation logic: (8+7+6+9+5+7) / 6 = 42 / 6 = 7.0
        expected_avg = round(sum(mock_llm_json.values()) / len(mock_llm_json), 2)
        assert results['Total_Deviation'] == expected_avg
        
        # Verify critical keys exist in the output dictionary
        assert "SS" in results
        assert "STS" in results
        print(f"\n✅ 6-Dimension logic verified! Total Deviation: {results['Total_Deviation']}")

def test_error_handling(evaluator):
    """Verify the system returns an empty dictionary gracefully if the API fails."""
    with patch.object(evaluator.client.chat.completions, 'create', side_effect=Exception("API Timeout")):
        results = evaluator.evaluate_news("original", "evolved")
        assert results == {}
        print("✅ Error handling verified successfully!")