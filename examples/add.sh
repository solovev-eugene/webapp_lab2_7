#!/bin/bash

curl -X POST "http://127.0.0.1:5000/api/diseases" \
    -H "Content-Type: application/json" \
    -d '{
        "country": "ABC",
        "region": "DEG",
        "population": 10,
        "cases": 5,
        "deaths": 2,
        "recovered": 3
    }'