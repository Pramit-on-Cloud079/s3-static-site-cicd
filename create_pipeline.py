import boto3
import json
import os

region = 'us-east-1'
codepipeline = boto3.client('codepipeline', region_name=region)
codebuild = boto3.client('codebuild', region_name=region)
s3 = boto3.client('s3', region_name=region)

# === CONFIG ===
GITHUB_OWNER = 'Pramit-on-Cloud079'
GITHUB_REPO = 's3-static-site-cicd'
BRANCH = 'master'
GITHUB_OAUTH_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
BUILD_PROJECT_NAME = 'StaticSiteBuildProject'
PIPELINE_NAME = 'StaticSitePipeline'

# ✅ Your buckets
ARTIFACT_BUCKET = 'codepipeline-artifacts-pramit'
DEPLOY_BUCKET = 'pramit079-static-site-hosting'

# === Check Deploy Bucket Exists ===
try:
    s3.head_bucket(Bucket=DEPLOY_BUCKET)
    print(f"✅ Deploy bucket exists: {DEPLOY_BUCKET}")
except Exception as e:
    print(f"❌ Deploy bucket {DEPLOY_BUCKET} is missing. Create it before proceeding.")
    exit(1)

# === Create CodeBuild Project ===
try:
    codebuild.create_project(
        name=BUILD_PROJECT_NAME,
        source={
            'type': 'CODEPIPELINE',
            'buildspec': 'buildspec.yml'
        },
        artifacts={'type': 'CODEPIPELINE'},
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/standard:5.0',
            'computeType': 'BUILD_GENERAL1_SMALL',
            'privilegedMode': False
        },
        serviceRole='arn:aws:iam::231299271232:role/CodeBuildServiceRole'
    )
    print(f"✅ CodeBuild project created: {BUILD_PROJECT_NAME}")
except codebuild.exceptions.ResourceAlreadyExistsException:
    print(f"ℹ️ CodeBuild project already exists: {BUILD_PROJECT_NAME}")

# === Create CodePipeline ===
pipeline_role_arn = 'arn:aws:iam::231299271232:role/CodePipelineServiceRole'

pipeline_definition = {
    'pipeline': {
        'name': PIPELINE_NAME,
        'roleArn': pipeline_role_arn,
        'artifactStore': {
            'type': 'S3',
            'location': ARTIFACT_BUCKET
        },
        'stages': [
            {
                'name': 'Source',
                'actions': [
                    {
                        'name': 'SourceAction',
                        'actionTypeId': {
                            'category': 'Source',
                            'owner': 'ThirdParty',
                            'provider': 'GitHub',
                            'version': '1'
                        },
                        'outputArtifacts': [{'name': 'SourceOutput'}],
                        'configuration': {
                            'Owner': GITHUB_OWNER,
                            'Repo': GITHUB_REPO,
                            'Branch': BRANCH,
                            'OAuthToken': GITHUB_OAUTH_TOKEN
                        },
                        'runOrder': 1
                    }
                ]
            },
            {
                'name': 'Build',
                'actions': [
                    {
                        'name': 'BuildAction',
                        'actionTypeId': {
                            'category': 'Build',
                            'owner': 'AWS',
                            'provider': 'CodeBuild',
                            'version': '1'
                        },
                        'inputArtifacts': [{'name': 'SourceOutput'}],
                        'outputArtifacts': [{'name': 'BuildOutput'}],
                        'configuration': {
                            'ProjectName': BUILD_PROJECT_NAME
                        },
                        'runOrder': 1
                    }
                ]
            },
            {
                'name': 'Deploy',
                'actions': [
                    {
                        'name': 'DeployToS3',
                        'actionTypeId': {
                            'category': 'Deploy',
                            'owner': 'AWS',
                            'provider': 'S3',
                            'version': '1'
                        },
                        'inputArtifacts': [{'name': 'BuildOutput'}],
                        'configuration': {
                            'BucketName': DEPLOY_BUCKET,
                            'Extract': 'true'
                        },
                        'runOrder': 1
                    }
                ]
            }
        ],
        'version': 1
    }
}

try:
    codepipeline.create_pipeline(**pipeline_definition)
    print(f"✅ CodePipeline created: {PIPELINE_NAME}")
except codepipeline.exceptions.PipelineNameInUseException:
    print(f"ℹ️ Pipeline already exists: {PIPELINE_NAME}")
