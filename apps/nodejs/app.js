/**
 * AWS Elastic Beanstalk Node.js Reference Application.
 *
 * EB Node.js platform expects the app to listen on process.env.PORT (default 8080).
 * nginx reverse proxy forwards requests to this port.
 *
 * Reference: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_nodejs_express.html
 */

const express = require("express");
const os = require("os");

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    application: "aws-eb-nodejs-reference",
    status: "running",
    timestamp: new Date().toISOString(),
  });
});

/**
 * Health check endpoint.
 *
 * Configure this path in Elastic Beanstalk environment:
 * - Namespace: aws:elasticbeanstalk:environment:process:default
 * - Option: HealthCheckPath
 * - Value: /health
 */
app.get("/health", (req, res) => {
  res.json({ status: "healthy" });
});

app.get("/info", (req, res) => {
  res.json({
    node_version: process.version,
    platform: os.platform(),
    arch: os.arch(),
    environment: process.env.ENV_NAME || "local",
    region: process.env.AWS_REGION || "not-set",
    port: PORT,
    uptime_seconds: Math.floor(process.uptime()),
  });
});

/**
 * Demonstrate reading environment properties.
 *
 * In EB, set environment properties via:
 * - Console: Configuration > Software > Environment properties
 * - CLI: eb setenv KEY=VALUE
 * - .ebextensions: option_settings namespace
 */
app.get("/demo/env", (req, res) => {
  const safeKeys = ["ENV_NAME", "APP_VERSION", "LOG_LEVEL"];
  const envVars = {};
  safeKeys.forEach((key) => {
    envVars[key] = process.env[key] || "not-set";
  });
  res.json({ environment_properties: envVars });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
