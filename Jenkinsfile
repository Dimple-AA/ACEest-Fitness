pipeline {
    agent any
    environment {
        APP_NAME = "aceest-fitness"
        DOCKERHUB_REPO = "dimpleaa/aceest-fitness"
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
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                echo "🧪 Running tests..."
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh 'docker build -t ${APP_NAME}:latest .'
            }
        }
        stage('Push to DockerHub') {
            steps {
                echo "📤 Pushing Docker image to DockerHub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag ${APP_NAME}:latest ${DOCKERHUB_REPO}:latest
                        docker push ${DOCKERHUB_REPO}:latest
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                echo "🚀 Running container..."
                sh '''
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    docker run -d -p 5000:5000 --name ${APP_NAME} ${DOCKERHUB_REPO}:latest
                '''
            }
        }
    }
    post {
        success { echo "🎉 Deployment successful! Visit http://localhost:5000" }
        failure { echo "❌ Build failed." }
    }
}
