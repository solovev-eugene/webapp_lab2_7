#!/bin/bash

curl -G "http://127.0.0.1:5000/api/diseases/metrics" \
    -d "field=cases" \
    -d "func=avg"