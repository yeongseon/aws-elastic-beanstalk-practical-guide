# Define a Java Elastic Beanstalk Environment with CloudFormation

This tutorial shows how to provision a Spring Boot Elastic Beanstalk environment with AWS CloudFormation.
The focus is a reproducible environment definition that sets the platform branch, instance profile, application version source bundle, and health path.

## Prerequisites

- Spring Boot application already packaged and uploaded through your deployment workflow.
- Familiarity with Elastic Beanstalk applications, environment names, and service roles.
- IAM permissions for CloudFormation, Elastic Beanstalk, EC2, IAM, and S3.

## What You'll Build

You will build a CloudFormation stack that creates:

- An Elastic Beanstalk application.
- An application version backed by an S3 source bundle.
- A web server environment using Corretto 17 on Amazon Linux 2023.
- Option settings for instance profile, health path, and environment properties.

```mermaid
flowchart TD
    A[CloudFormation Stack] --> B[EB Application]
    A --> C[Application Version from S3]
    A --> D[EB Environment]
    D --> E[Corretto 17 AL2023 Platform]
    D --> F[EC2 Instances with Instance Profile]
    D --> G[/health Check Path]
```

## Steps

1. Create a parameters-driven CloudFormation template.

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Parameters:
    ApplicationName:
        Type: String
    EnvironmentName:
        Type: String
    SolutionStackName:
        Type: String
        Default: 64bit Amazon Linux 2023 v4.3.1 running Corretto 17
    InstanceProfile:
        Type: String
        Default: aws-elasticbeanstalk-ec2-role
    ServiceRole:
        Type: String
        Default: aws-elasticbeanstalk-service-role
    SourceBucket:
        Type: String
    SourceKey:
        Type: String
Resources:
    EbApplication:
        Type: AWS::ElasticBeanstalk::Application
        Properties:
            ApplicationName: !Ref ApplicationName
    EbVersion:
        Type: AWS::ElasticBeanstalk::ApplicationVersion
        Properties:
            ApplicationName: !Ref ApplicationName
            SourceBundle:
                S3Bucket: !Ref SourceBucket
                S3Key: !Ref SourceKey
    EbEnvironment:
        Type: AWS::ElasticBeanstalk::Environment
        Properties:
            ApplicationName: !Ref ApplicationName
            EnvironmentName: !Ref EnvironmentName
            SolutionStackName: !Ref SolutionStackName
            VersionLabel: !Ref EbVersion
            OptionSettings:
                - Namespace: aws:autoscaling:launchconfiguration
                  OptionName: IamInstanceProfile
                  Value: !Ref InstanceProfile
                - Namespace: aws:elasticbeanstalk:environment
                  OptionName: ServiceRole
                  Value: !Ref ServiceRole
                - Namespace: aws:elasticbeanstalk:environment:process:default
                  OptionName: HealthCheckPath
                  Value: /health
                - Namespace: aws:elasticbeanstalk:application:environment
                  OptionName: SPRING_PROFILES_ACTIVE
                  Value: prod
Outputs:
    EnvironmentUrl:
        Value: !GetAtt EbEnvironment.EndpointURL
```

2. Package and upload the source bundle.

```bash
mvn clean package
zip --recurse-paths java-eb-bundle.zip pom.xml Procfile .ebextensions src target
aws s3 cp java-eb-bundle.zip "s3://$APP_NAME-artifacts/java-eb-bundle.zip" --region "$REGION"
```

3. Deploy the stack.

```bash
aws cloudformation deploy --stack-name "$APP_NAME-eb-java" --template-file infrastructure/elastic-beanstalk-java.yaml --capabilities CAPABILITY_NAMED_IAM --parameter-overrides ApplicationName="$APP_NAME" EnvironmentName="$ENV_NAME" SourceBucket="$APP_NAME-artifacts" SourceKey="java-eb-bundle.zip" --region "$REGION"
```

4. Inspect stack outputs and environment health.

```bash
aws cloudformation describe-stacks --stack-name "$APP_NAME-eb-java" --region "$REGION"
eb health "$ENV_NAME"
```

## Verification

Use these checks after stack deployment:

```bash
aws elasticbeanstalk describe-environments --application-name "$APP_NAME" --environment-names "$ENV_NAME" --region "$REGION"
aws cloudformation describe-stack-events --stack-name "$APP_NAME-eb-java" --region "$REGION"
curl --verbose "http://$CNAME/health"
```

Expected outcomes:

- CloudFormation creates or updates the Elastic Beanstalk environment successfully.
- The environment runs the Corretto 17 Amazon Linux 2023 platform branch.
- `/health` is the configured health endpoint.
- Stack events provide a complete audit trail for infrastructure changes.

## See Also

- [Configuration](./03-configuration.md)
- [CI/CD](./06-ci-cd.md)
- [Custom Domain and SSL](./07-custom-domain-ssl.md)

## Sources

- [AWS::ElasticBeanstalk::Application](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-application.html)
- [AWS::ElasticBeanstalk::Environment](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-environment.html)
- [AWS::ElasticBeanstalk::ApplicationVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-applicationversion.html)
