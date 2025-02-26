# Deploying to Posit Connect

This document provides instructions for deploying the Gen AI Exploration Zone application to Posit Connect.

## Prerequisites

1. Access to a Posit Connect server
2. Appropriate permissions to deploy applications
3. An OpenAI API key with access to GPT-4o and GPT-4o-mini models

## Deployment Steps

### 1. Prepare the Application

Ensure your application files are ready:
- All Python dependencies are listed in `requirements.txt`
- `manifest.yml` is present in the root directory
- Configuration is set to detect Posit Connect environment

### 2. Configure Environment Variables in Posit Connect

In the Posit Connect dashboard, navigate to your application settings and add the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: A secure random string for Flask session encryption

### 3. Deploy the Application

Deploy using one of these methods:

#### Using rsconnect-python CLI

```bash
# Install the client
pip install rsconnect-python

# Authenticate with your Posit Connect server
rsconnect add --server https://your-connect-server.com --api-key YOUR_API_KEY --name my-connect

# Deploy the application
rsconnect deploy flask -n my-connect /path/to/app
```

#### Using Git Integration

If your Posit Connect server supports Git integration:

1. Push your code to a Git repository
2. In the Posit Connect dashboard, choose "New Content" > "From Git Repository"
3. Enter your repository details and select the branch to deploy
4. Choose "Manifest" as the deployment method

### 4. Verify Deployment

1. Check that the application is listed as "Running" in the Posit Connect dashboard
2. Access the application URL provided by Posit Connect
3. Test the functionality to ensure it's working as expected

## Troubleshooting

### Application Not Starting

Check the application logs in the Posit Connect dashboard for error messages.

Common issues:
- Missing dependencies in `requirements.txt`
- Environment variables not properly set
- Insufficient resources allocated (memory/CPU)

### File Upload Issues

- Verify the `uploads` directory has proper permissions
- Check if the maximum file size limit is enforced by Posit Connect

### API Connection Issues

- Verify the OpenAI API key is correct
- Check network connectivity between Posit Connect and OpenAI's servers

## Maintenance

### Updating the Application

1. Make changes to your code locally
2. Update version number in `manifest.yml` if desired
3. Redeploy using the same method as initial deployment

### Monitoring

Use the Posit Connect dashboard to:
- Monitor application usage
- Check resource consumption
- View application logs