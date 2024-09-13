export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

cdklocal bootstrap aws://000000000000/us-east-1
cdklocal synth
cdklocal deploy --require-approval never