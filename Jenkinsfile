pipeline {
    agent any

    environment {
        APP_NAME = "aceest-fitness"
        DOCKERHUB_REPO = "2024tm93009/aceest-fitness"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📦 Checking out source code..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "🐍 Installing dependencies..."
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "🧪 Running tests..."
                bat '''
                    call venv\\Scripts\\activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                bat "docker build -t %APP_NAME%:latest ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo "📤 Pushing Docker image to DockerHub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker tag %APP_NAME%:latest %DOCKERHUB_REPO%:latest
                        docker push %DOCKERHUB_REPO%:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Running container..."
                bat '''
                    docker stop %APP_NAME% || echo Container not running
                    docker rm %APP_NAME% || echo Container not found
                    docker run -d -p 5000:5000 --name %APP_NAME% %DOCKERHUB_REPO%:latest
                '''
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment successful! Visit http://localhost:5000"
        }
        failure {
            echo "❌ Build failed."
        }
    }
}
