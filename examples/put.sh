#!/bin/bash

curl -X PUT "http://127.0.0.1:5000/api/diseases/61" \
    -H "Content-Type: application/json" \
    -d '{
        "country": "abc",
        "region": "deg",
        "population": 15,
        "cases": 15,
        "deaths": 14,
        "recovered": 1
    }'