# Vision AI demo

* Vision AI text recognition from document
* Python runtime. Flask web app on Cloud Functions

# Quickstart
```shell
# Run at localhost:8080
functions_framework --target=handle

# Deploy to the Cloud
gcloud functions deploy ocrdemo --entry-point=handle \                                                                  master
--runtime python39 --trigger-http --allow-unauthenticated
```
