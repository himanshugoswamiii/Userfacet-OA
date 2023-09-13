## Task of the project
Task : https://github.com/himanshugoswamiii/Userfacet-OA/blob/main/assets/Backend-Develoment-Assessment.pdf


---

This project is made using **FastAPI**
Currently this is not using any external database for data storage. Everything is done by using list and dictionaries to replicate the behavior
of the database

## Configuration of the Project

Go to your project folder:

**Creating a virtual environment:**
```sh
python -m venv venv
```
> this command may differ based on your OS 

**Starting the Virtual environment:**
```sh
source venv/bin/activate
```

**Installing dependencies**

```sh
pip install requirements.txt
```

## Running the project

Go to the root of your project then run this command to open a live server on your localhost : `http://127.0.0.1:8000/`

```sh
uvicorn main:app --reload
```

## Documentation for the project
To see the *interactive documentation* for your api endpoints you can go to : `http://127.0.0.1:8000/docs`

---

## SAMPLE USAGE 
- You can create multiple surveys of 20 questions
- You can get the similarity for particular survey

Use interactive documentation

#### 1. Create a survey (We need atleast 1 survey to work with)

![Create-surveys](https://github.com/himanshugoswamiii/Userfacet-OA/blob/main/assets/01-create-surveys.png)

Example input :

```json
{
  "name": "survey-1",
  "questions" : [
      "question 1",
      "question 2",
      "question 3",
      "question 4",
      "question 5",
      "question 6",
      "question 7",
      "question 8",
      "question 9",
      "question 10",
      "question 11",
      "question 12",
      "question 13",
      "question 14",
      "question 15",
      "question 16",
      "question 17",
      "question 18",
      "question 10",
      "question 20"
    ]
}


```

#### 2. Add responses for the available surveys

Here you'll add the response user by user

![Adding-response](https://github.com/himanshugoswamiii/Userfacet-OA/blob/main/assets/02-adding-response-for-survey.png)

```json
{
  "candidate_name": "Himanshu",
  "response": [
    0,
    null,
    1,
    2,
    3,
    4,
    1,
    2,
    3,
    4,
    1,
    2,
    3,
    4,
    1,
    2,
    3,
    4,
    5,
    6
  ]
}
```

> `null` represents no response for that question

Add more response to see the similarity

#### 3. Calculate the similarities

![Calc-similarity](https://github.com/himanshugoswamiii/Userfacet-OA/blob/main/assets/03-calculate-similarity-for-all.png)

You've 3 methods for calculating similarities

> Note: I've not covered everything in this sample usage. Please see the interactive documentation for all the options
