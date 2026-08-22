#!/bin/bash

curl -X PATCH "http://127.0.0.1:5000/api/diseases/61" \
    -H "Content-Type: application/json" \
    -d '{
        "population": 20
    }'