FROM public.ecr.aws/lambda/python:3.11

# Install git
RUN yum install -y git

COPY lambda_function.py ./

CMD ["lambda_function.handler"]
