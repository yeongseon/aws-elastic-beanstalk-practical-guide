"""
AWS Elastic Beanstalk Python Reference Application.

EB expects the WSGI callable to be named `application` in a file named `application.py`.
Reference: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
"""

from flask import Flask, jsonify, request
import os
import platform
import datetime

application = Flask(__name__)


@application.route("/")
def index():
    """Root endpoint with application info."""
    return jsonify({
        "application": "aws-eb-python-reference",
        "status": "running",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    })


@application.route("/health")
def health():
    """Health check endpoint.

    Configure this path in Elastic Beanstalk environment:
    - Namespace: aws:elasticbeanstalk:environment:process:default
    - Option: HealthCheckPath
    - Value: /health
    """
    return jsonify({"status": "healthy"}), 200


@application.route("/info")
def info():
    """Environment information endpoint for debugging."""
    return jsonify({
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "environment": os.environ.get("ENV_NAME", "local"),
        "region": os.environ.get("AWS_REGION", "not-set"),
        "port": os.environ.get("PORT", "5000"),
    })


@application.route("/demo/env")
def demo_env():
    """Demonstrate reading environment properties.

    In EB, set environment properties via:
    - Console: Configuration > Software > Environment properties
    - CLI: eb setenv KEY=VALUE
    - .ebextensions: option_settings namespace
    """
    safe_keys = ["ENV_NAME", "APP_VERSION", "LOG_LEVEL"]
    env_vars = {k: os.environ.get(k, "not-set") for k in safe_keys}
    return jsonify({"environment_properties": env_vars})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port, debug=True)
