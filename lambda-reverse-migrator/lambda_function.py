import os
import yaml
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # New: Redpanda is now the input, Confluent Kafka is output
    config = {
        "input": {
            "redpanda_migrator": {
                "seed_brokers": [os.getenv("REDPANDA_BROKER")],
                "topics": os.getenv("KAFKA_TOPICS", "").split(","),
                "regexp_topics": True,
                "consumer_group": "redpanda_migrator_group",
                "start_from_oldest": True,
                "tls": {
                    "enabled": True,
                    "root_cas_file": "/etc/ssl/certs/ca-certificates.crt"
                },
                "sasl": [{
                    "mechanism": "SCRAM-SHA-512",
                    "username": os.getenv("REDPANDA_USERNAME"),
                    "password": os.getenv("REDPANDA_PASSWORD")
                }]
            }
        },
        "pipeline": {
            "processors": [{
                "try": [
                    {
                        "schema_registry_decode": {
                            "avro": {
                                "raw_unions": False,
                                "preserve_logical_types": False
                            },
                            "url": os.getenv("SCHEMA_REGISTRY_URL"),
                            "basic_auth": {
                                "enabled": True,
                                "username": os.getenv("SCHEMA_USERNAME"),
                                "password": os.getenv("SCHEMA_PASSWORD")
                            }
                        }
                    },
                    {
                        "catch": [
                            {
                                "log": {
                                    "level": "WARN",
                                    "message": "Failed to decode as Avro, falling back to raw JSON"
                                }
                            },
                            {
                                "bloblang": "root = this"
                            }
                        ]
                    }
                ]
            }]
        },
        "output": {
            "redpanda_migrator": {
                "seed_brokers": [os.getenv("CONFLUENT_BROKER")],
                "topic": "${! meta(\"kafka_topic\") }",
                "key": "${! meta(\"kafka_key\") }",
                "sasl": [{
                    "mechanism": "PLAIN",
                    "username": os.getenv("CONFLUENT_USERNAME"),
                    "password": os.getenv("CONFLUENT_PASSWORD")
                }],
                "tls": {
                    "enabled": True
                }
            }
        }
    }

    # Convert to YAML
    yaml_str = yaml.dump(config, sort_keys=False)

    # Upload to S3
    bucket = os.getenv("S3_BUCKET")
    key = "config.yaml"

    try:
        s3.put_object(Bucket=bucket, Key=key, Body=yaml_str.encode("utf-8"))
        logger.info(f"Successfully updated s3://{bucket}/{key}")
    except Exception as e:
        logger.error(f"Failed to upload config to S3: {str(e)}")
        raise

    return {
        'statusCode': 200,
        'body': f"Config uploaded to s3://{bucket}/{key}"
    }
