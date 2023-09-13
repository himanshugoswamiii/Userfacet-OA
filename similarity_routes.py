from fastapi import APIRouter, status, HTTPException, Query, Path
from typing import List, Optional

# Local imports
from utils import pagination, calculate_similarity_score
from globals import *

# 2. Endpoint for Similarity Calculation
similarity_router = APIRouter(
    prefix="/similarity",
    tags=["similarity"]
)

# 2.a : Calculate similarity among different candidates
# 2.b. Filter : Calculating similarity between the passed candidate and everyone else
# Here : candidate_name is optional
@similarity_router.get("/{survey_name}")
def calculate_similarity(survey_name: str, candidate_name: Optional[str] = None, page: int = 1, page_size: int = 5):
    """
    2.a : Calculate similarity among different candidates (If you don't give the candidate_name, it'll calculate similarities between all)

    2.b. Filter : Calculating similarity between the passed candidate and everyone else if a candidate_name is passed

    Args:

        candidate_name (str, optional): Name of the candidate to filter results.

    Returns:

        List[Dict]: Similarity results for the given candidate with all other candidates.
    """

    # Find the survey by name
    survey = next((s for s in survey_data if s["name"] == survey_name), None)
    if survey is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Survey '{survey_name}' not found")

    # Filter responses based on survey -name
    responses_for_survey = [response for response in responses if response["survey_name"] == survey_name]

    similarity_results = []

    if candidate_name is None:
        # No candidate name is given then find the similarity among all candidates
        similarity_results = find_similarity(responses_for_survey)

    else:
        # When candidate name is given
        candidate_response = None
        # Filter responses based on candidate_name (case-insensitive)
        # filtered_responses = [r for r in responses if r["name"].lower().startswith(candidate_name.lower())]
        for r in responses_for_survey:
            if r["candidate_name"].lower().startswith(candidate_name.lower()):
                candidate_response = r
                break
        # print(candidate_response)
        if candidate_response is None:
            raise HTTPException(status_code=404, detail="candidates name doesn't exist")


        for response in responses_for_survey:
            if candidate_response != response: # leaving comparison with itself
                candidate_similarity = {
                    "name": response["candidate_name"],
                    "similarity": calculate_similarity_score(candidate_response["response"], response["response"])
                }
                similarity_results.append(candidate_similarity)

    paginated_results = pagination(page, page_size, similarity_results)
    return paginated_results


# 2.d : Endpoint to find similarity between candidates with names containing a query parameter
@similarity_router.get("/{survey_name}/search")
async def search_similarity( survey_name: str, search_text: str = Query(..., title="Candidate name query to search for similarities"), page: int = 1, page_size: int = 5):
    """
    2.c : Endpoint to find similarity between candidates for a specific survey based on a candidate name query.

    Args:

        survey_name (str): Name of the survey (taken from the path parameter).
        search_text (str): Candidate name query to search for similarities.

    Returns:

        List[Dict]: Similarity results for the specified survey and candidates with names containing the query.
    """
    # Find the survey by name
    survey = next((s for s in survey_data if s["name"] == survey_name), None)

    if survey is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Survey '{survey_name}' not found")

    # Filter responses based on the survey name and search_text query
    responses_for_survey = [
        response for response in responses
        if response["survey_name"] == survey_name and search_text.lower() in response["candidate_name"].lower()
    ]

    # Calculate similarity with all other candidates
    similarity_results = find_similarity(responses_for_survey)

    paginated_results = pagination(page, page_size, similarity_results) # pagination is in utils.py
    return paginated_results

def find_similarity(responses_for_survey):
    """
    Returns :

        List : list of similarities among all the values in responses_for_survey (i.e : Similarities among all the unique combinations)
    """
    similarity_results = list()
    for i in range(0, len(responses_for_survey)):
        for j in range(i+1, len(responses_for_survey)):
            first_candidate = responses_for_survey[i]
            second_candidate = responses_for_survey[j]
            candidate_similarity = {
                "first Candidate" : first_candidate["candidate_name"],
                "second Candidate" : second_candidate["candidate_name"],
                "similarity": calculate_similarity_score(first_candidate["response"], second_candidate["response"])
            }

            similarity_results.append(candidate_similarity)
            
    return similarity_results