pipeline {
    agent any

    environment {
        APP_NAME = "aceest-fitness"
        DOCKERHUB_REPO = "2024tm93009/aceest-fitness"
        SONARQUBE_ENV = "SonarQube"    // Name configured in Manage Jenkins → System

        // Add SonarScanner and Java paths
        PATH = "C:\\sonar-scanner\\bin;${env.PATH}"
        SONAR_JAVA_PATH = "C:\\Program Files\\Java\\jdk-17.0.8\\bin\\java.exe"  // Update to your actual Java path
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
                    python -m pip install --upgrade pip
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

        stage('SonarQube Analysis') {
            steps {
                echo "🔍 Running SonarQube Code Analysis..."
                withSonarQubeEnv('SonarQube') {
                    bat """
                        C:\\sonar-scanner\\bin\\sonar-scanner ^
                        -Dsonar.projectKey=aceest-fitness ^
                        -Dsonar.projectName=aceest-fitness ^
                        -Dsonar.sources=. ^
                        -Dsonar.python.coverage.reportPaths=coverage.xml ^
                        -Dsonar.host.url=http://localhost:9000
                    """
                }
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
