## To Create a virtual environment

python -m venv venv

## Using Conda Windows

conda create -p venv python==3.12

conda activate venv/

pip install -r requirements.txt

## To Activate the environment MAC

source venv/bin/activate

source venv/bin/deactivate

## To Download the dependencies

pip install -r requirements.txt

## Create a Crew

crewai create crew ${name of crew}

## Docker build command

docker build -t crewai_example:latest .

docker run -d -p 8000:8000 -e OPENAI_API_KEY="" -e TAVILY_API_KEY="" --name crewai_example-container crewai_example:latest

docker tag crewai_example:latest hiteshs0lanki/crewai_example:latest

docker push hiteshs0lanki/crewai_example:latest
