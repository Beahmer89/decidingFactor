# decidingFactor

This project is aimed at indecisive people such as myself when you need someone to make the final decision.

## What this program does
This program will be used to:
- Pick a restaurant at random in your area, based on your parameters using the yelp API
- Keep track of places that were a success
  - Choose from those places that were a success when you dont want a new place

# Getting Started

## Import Environment variables
|Variable Name      | Definition
|-------------------|------------
|**YELP\_API\_HOST**| Yelp url used to retrieve restaurants from Yelp
|**YELP\_API\_KEY** | API key generaged from Yelp to be able to authorize use

## How to contribute
    virtualenv --python=python3 env
    pip install -r requires/testing.txt -i https://pypi.python.org/simple/
    python manage.py test restaurant
