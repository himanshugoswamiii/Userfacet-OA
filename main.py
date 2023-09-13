from fastapi import FastAPI, Path, Query
from typing import List, Optional
from uuid import uuid4

# local imports
from schemas import SurveyCreate, ResponseSubmit

app = FastAPI()

# Define data structures to store survey questions and candidate responses
survey_data = []  # List to store survey questions as lists of options (each question is a list)
responses = []  # List to store candidate responses as dictionaries

# 1. Endpoints for Survey Management

# a. List all available surveys
@app.get("/surveys")
def list_surveys():
    """
    Endpoint to list all available surveys.

    Returns:
        List: List of survey questions.
    """
    return survey_data

# b. Create a survey with 20 questions
@app.post("/surveys")
def create_survey(survey_create: SurveyCreate):
    """
    Endpoint to create a new survey with a name and 20 questions.

    Args:
        survey_create (SurveyCreate): Pydantic model containing survey name and questions.

    Returns:
        Dict: A message indicating the success or error along with the survey name.
    """
    if len(survey_create.questions) == 20:
        # Check if the survey name is unique
        if not any(survey["name"] == survey_create.name for survey in survey_data):
            # Store the survey along with its name
            survey_data.append({"name": survey_create.name, "questions": survey_create.questions})
            return {"message": f"Survey '{survey_create.name}' created successfully", "survey_name": survey_create.name}
        else:
            return {"error": f"Survey name '{survey_create.name}' already exists"}
    else:
        return {"error": "Survey must have 20 questions"}

# c. Submit a response for a survey from a user

# ...

# c. Submit a response for a survey from a user
@app.post("/responses/{survey_name}")
def submit_response(response_submit: ResponseSubmit, survey_name: str = Path(..., title="Name of the survey")):
    """
    Endpoint to submit a response for a survey from a candidate.

    Args:
        survey_name (str): Name of the survey (taken from the path parameter).
        response_submit (ResponseSubmit): Pydantic model containing candidate name and response.

    Returns:
        Dict: A message indicating the success or error.
    """
    # Find the survey by name
    survey = next((s for s in survey_data if s["name"] == survey_name), None)

    if survey is None:
        return {"error": f"Survey '{survey_name}' not found"}

    if len(response_submit.response) == 20:
        responses.append({
            "candidate_name": response_submit.candidate_name,
            "survey_name": survey_name,
            "response": response_submit.response
        })
        return {"message": "Response submitted successfully"}
    else:
        return {"error": "Response must have 20 answers"}

# d. Get all responses for a specific survey
@app.get("/responses/{survey_name}")
def get_responses_for_survey(survey_name: str = Path(..., title="Name of the survey")):
    """
    Endpoint to retrieve all responses for a specific survey.

    Args:
        survey_name (str): Name of the survey (taken from the path parameter).

    Returns:
        List[Dict]: List of responses for the specified survey.
    """
    # Find the survey by name
    survey = next((s for s in survey_data if s["name"] == survey_name), None)

    if survey is None:
        return {"error": f"Survey '{survey_name}' not found"}

    # Filter responses based on the survey name
    responses_for_survey = [response for response in responses if response["survey_name"] == survey_name]

    return responses_for_survey

# ...


# 2. Endpoint for Similarity Calculation
# a. Calculate similarity among different candidates
@app.get("/similarity/{survey_name}")
def calculate_similarity(survey_name: str, candidate_name: Optional[str] = None):
    """
    Endpoint to calculate similarity among candidate responses for a given survery.

    Args:
        candidate_name (str, optional): Name of the candidate to filter results.

    Returns:
        List[Dict]: Similarity results for the given candidate with all other candidates.
    """

    # Find the survey by name
    survey = next((s for s in survey_data if s["name"] == survey_name), None)
    if survey is None:
        return {"error": f"Survey '{survey_name}' not found"}

    # Filter responses based on survey -name
    responses_for_survey = [response for response in responses if response["survey_name"] == survey_name]

    similarity_results = []

    if candidate_name is None:
        # No candidate name is given then find the similarity among all candidates
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

        # Return results sorted by similarity (optional)
        similarity_results = sorted(similarity_results, key=lambda x: x["similarity"], reverse=True)

    return similarity_results

def calculate_similarity_score(response1, response2):
    """
    Function to calculate similarity score between two sets of responses.

    Args:
        response1 : List of responses for the first candidate.
        response2 : List of responses for the second candidate.

    Returns:
        string: Similarity score (% of matching answers).
    """
    if len(response1) != len(response2):
        raise ValueError("Response lengths do not match")

    # similarity_score = sum(1 for a, b in zip(response1, response2) if a == b)


    similarity_score = 0
    total = 20

    for (a, b) in zip(response1, response2):
        if a is None or b is None: # leave the none values
            total = total-1
        else:
            if a == b:
                similarity_score += 1

    if total == 0:
        return "0%" # there is no similarity 
        #(for the case when first half given by candidate 1 is None and second half given by candidate 2 is None)

    percentage = similarity_score / total * 100
    formatted_percentage = f"{percentage:.2f}%"
    return formatted_percentage

# Endpoint to find similarity between candidates with names containing a query parameter
@app.get("/{survey_name}/search")
async def search_similarity( survey_name: str, search_text: str = Query(..., title="Candidate name query to search for similarities")):
    """
    Endpoint to find similarity between candidates for a specific survey based on a candidate name query.

    Args:
        survey_name (str): Name of the survey (taken from the path parameter).
        search_text (str): Candidate name query to search for similarities.

    Returns:
        List[Dict]: Similarity results for the specified survey and candidates with names containing the query.
    """
    # Find the survey by name
    survey = next((s for s in survey_data if s["name"] == survey_name), None)

    if survey is None:
        raise HTTPException(status_code=404, detail=f"Survey '{survey_name}' not found")

    # Filter responses based on the survey name and search_text query
    responses_for_survey = [
        response for response in responses
        if response["survey_name"] == survey_name and search_text.lower() in response["candidate_name"].lower()
    ]

    # Calculate similarity with all other candidates
    similarity_results = []

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

    # Return results sorted by similarity (optional)
    similarity_results = sorted(similarity_results, key=lambda x: x["similarity"], reverse=True)
    return similarity_results

