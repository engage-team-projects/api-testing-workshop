import os
import subprocess


def init_acceptance_tests():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ENDPOINT_URL"] = "http://localhost:4566"

    subprocess.run(["cdklocal", "bootstrap", "aws://000000000000/us-east-1"])
    subprocess.run(["cdklocal", "synth"])
    subprocess.run(["cdklocal", "deploy", "--require-approval", "never"])
