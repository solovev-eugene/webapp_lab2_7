#!/bin/bash

curl -G "http://127.0.0.1:5000/api/diseases" \
    -d "sort=cases" \
    -d "order=desc" \
    -d "limit=3"