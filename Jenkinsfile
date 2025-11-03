pipeline {
    agent any

    environment {
        APP_NAME = "aceest-fitness"
        DOCKERHUB_REPO = "yourdockerhubusername/aceest-fitness"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Pytest unit tests..."
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t ${APP_NAME}:latest .'
            }
        }

        stage('Push to DockerHub') {
            when {
                expression { return env.DOCKERHUB_REPO != "" }
            }
            steps {
                echo "Pushing Docker image to DockerHub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag ${APP_NAME}:latest ${DOCKERHUB_REPO}:latest
                        docker push ${DOCKERHUB_REPO}:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying Docker container..."
                sh 'docker run -d -p 5000:5000 ${APP_NAME}:latest'
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment successful! Visit http://localhost:5000/"
        }
        failure {
            echo "❌ Build or tests failed. Please check logs."
        }
    }
}
