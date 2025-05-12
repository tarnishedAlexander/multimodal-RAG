#!/bin/bash
set -e

rm -rf /tmp/lambda_package /tmp/lambda_function.zip
mkdir -p /tmp/lambda_package/src/lambdaf
mkdir -p /tmp/lambda_package/utils
mkdir -p /tmp/lambda_package/config

cp src/lambdaf/*.py /tmp/lambda_package/src/lambdaf/
cp utils/*.py /tmp/lambda_package/utils/
cp config/*.py /tmp/lambda_package/config/

pip install --target /tmp/lambda_package -r requirements_lambda.txt

cd /tmp/lambda_package
zip -r /tmp/lambda_function.zip .

aws lambda update-function-code \
    --function-name rag-lambda \
    --region us-east-2 \
    --zip-file fileb:///tmp/lambda_function.zip

rm -rf /tmp/lambda_package /tmp/lambda_function.zip
echo "Lambda function deployed."