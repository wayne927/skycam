#!/bin/bash

export FLASK_APP=main.py
export FLASK_RUN_PORT=80
export FLASK_ENV=development

flask run --host=0.0.0.0
