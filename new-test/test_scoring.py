# This file contains unit tests for the scoring logic.
# Pytest will automatically discover and run these functions
# because the filename and function names start with "test_".

from services.score import _rating_to_score, credibility_score

def test_rating_to_score_logic():
    """
    Tests the helper function that converts a string rating to a numeric score.
    It checks all expected rating strings and a default case.
    """
    assert _rating_to_score("True") == 90
    assert _rating_to_score("partly true") == 45
    assert _rating_to_score("False") == 15
    assert _rating_to_score("unverified") == 55
    assert _rating_to_score("some other string") == 50
    assert _rating_to_score(None) == 50

def test_credibility_score_calculation_without_image():
    """
    Tests the main credibility_score function with only a fact-check result.
    """
    # A fact-check result indicating a "False" rating
    fact_result = {"rating": "False"}
    
    # The initial score should be low because the rating is "False"
    assert credibility_score(fact_result) == 15

def test_credibility_score_with_image_suspicion():
    """
    Tests that a high image suspicion score correctly lowers the final credibility score.
    """
    # A fact-check result that is "True" (which normally yields a high score)
    fact_result = {"rating": "True"}
    
    # An image analysis result with a significant suspicion score
    image_info = {"suspicion_score": 50} 
    
    # The final score should be reduced from the base of 90. 
    # The calculation is: 90 - (50 * 0.5) = 65
    assert credibility_score(fact_result, image_info) == 65
