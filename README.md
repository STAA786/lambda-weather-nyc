# lambda-weather-nyc
AWS Lambda function for NYC weather data

# 🌤️ AWS Lambda Weather Function - NYC Real-Time Weather Data

## Project Overview

This project implements an automated serverless solution for retrieving real-time weather data for New York City using AWS Lambda, integrated with a complete CI/CD pipeline.

## Architecture

┌─────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT ENVIRONMENT                       │
│                                                                  │
│  ┌──────────────┐         ┌─────────────────┐                  │
│  │  Developer   │────────>│  GitHub Repo    │                  │
│  │  Workstation │  Push   │  (Source Code)  │                  │
│  └──────────────┘         └────────┬────────┘                  │
└──────────────────────────────────────┼──────────────────────────┘
                                      │
                    Webhook Trigger   │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS CLOUD ENVIRONMENT                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              AWS CodePipeline (Orchestrator)           │    │
│  └────────────────────────────────────────────────────────┘    │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐         │
│  │  Source  │        │  Build   │        │  Deploy  │         │
│  │  Stage   │───────>│  Stage   │───────>│  Stage   │         │
│  │ (GitHub) │        │(CodeBuild│        │(CodeDeploy│        │
│  └──────────┘        └────┬─────┘        └────┬─────┘         │
│                           │                    │                │
│                           ▼                    ▼                │
│                    ┌─────────────┐     ┌──────────────┐        │
│                    │   Amazon    │     │    AWS       │        │
│                    │     S3      │────>│   Lambda     │        │
│                    │  (Artifacts)│     │  Function    │        │
│                    └─────────────┘     └──────┬───────┘        │
│                                               │                 │
│                                               ▼                 │
│                                        ┌─────────────┐          │
│                                        │   Amazon    │          │
│                                        │ API Gateway │          │
│                                        └──────┬──────┘          │
└───────────────────────────────────────────────┼─────────────────┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │  End Users   │
                                        │ Applications │
                                        └──────────────┘
## Technology/Tool Used

| Component              | Technology             | Version | Purpose                               |
|------------------------|------------------------|---------|----------------------------------------|
| Source Control         | GitHub                 | -       | Version control and collaboration      |
| Programming Language   | Python                 | 3.9     | Lambda function development            |
| Build Automation       | AWS CodeBuild          | -       | Automated build process                |
| Deployment Automation  | AWS CodeDeploy         | -       | Lambda function deployment             |
| Pipeline Orchestration | AWS CodePipeline       | -       | End-to-end workflow automation         |
| Compute Platform       | AWS Lambda             | -       | Serverless function execution          |
| Storage                | Amazon S3              | -       | Artifact storage                       |
| API Gateway            | Amazon API Gateway     | REST API| HTTP endpoint                          |
| Identity Management    | AWS IAM                | -       | Security and permissions               |
| External API           | OpenWeatherMap API     | 2.5     | Weather data source                    |
                                        


                                        
