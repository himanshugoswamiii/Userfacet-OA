from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import List, Optional

# local imports
from schemas import SurveyCreate, ResponseSubmit
from similarity_routes import similarity_router
from globals import * # global data structures

app = FastAPI()

app.include_router(similarity_router)


# 1. Endpoints for Survey Management

# 1.a : List all available surveys
@app.get("/surveys")
def list_surveys():
    """
    list all available surveys.

    Returns:

        List: List of survey questions.
    """
    if len(survey_data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No surveys available")
    return survey_data

# 1.b : Create a survey with 20 questions
@app.post("/surveys")
def create_survey(survey_create: SurveyCreate):
    """
    Endpoint to create a new survey with a name and 20 questions.

    Returns:

        Dict: A message indicating the success or error along with the survey name.
    """
    if len(survey_create.questions) != 20:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Survey must have 20 questions")

   # Check if the survey name is unique
    if any(survey["name"] == survey_create.name for survey in survey_data):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Survey name '{survey_create.name}' already exists")

    # Store the survey along with its name
    survey_data.append({"name": survey_create.name, "questions": survey_create.questions})
    return {"message": f"Survey '{survey_create.name}' created successfully", "survey_name": survey_create.name}


# 1.c : Submit a response for a survey from a user
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Survey '{survey_name}' not found")

    if len(response_submit.response) != 20:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Response must have 20 answers")

    responses.append({
        "candidate_name": response_submit.candidate_name,
        "survey_name": survey_name,
        "response": response_submit.response
    })
    return {"message": "Response submitted successfully", "candidate_name": response_submit.candidate_name}

# Get all responses for a specific survey
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Survey '{survey_name}' not found")

    # Filter responses based on the survey name
    responses_for_survey = [response for response in responses if response["survey_name"] == survey_name]

    return responses_for_survey


