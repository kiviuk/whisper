#! /bin/sh -x

curl -X 'POST' \
  'http://localhost:8000/whisper' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F "audioFiles=@${1};type=audio/x-wav"
