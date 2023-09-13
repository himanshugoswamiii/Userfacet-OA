## Task of the project

[Backend Task](https://github.com/himanshugoswamiii/Userfacet-OA/assets/Backend Develoment Assessment.pdf)

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