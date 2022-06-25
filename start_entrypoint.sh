#!/usr/bin/env bash
uvicorn main:app --host 0.0.0.0 --port 8800 --log-config conf/uvicorn.log.yaml --reload
