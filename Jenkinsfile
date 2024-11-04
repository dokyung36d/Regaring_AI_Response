pipeline {
    agent any
    environment {
        OPENAI_KEY = credentials('openai_key')
        MONGODB_USERNAME = credentials('mongodb_username')
        MONGODB_PASSWORD = credentials('mongodb_password')
    }
    stages {
        stage('Clone Repository') {
            steps {
                // Git 리포지토리에서 최신 코드 가져오기
                git 'https://github.com/dokyung36d/Regaring_AI_Response.git'
            }
        }
        stage('Create .env File') {
            steps {
                script {
                    writeFile file: '.env', text: """
                    openai_key=${env.OPENAI_KEY}
                    mongodb_username=${env.MONGODB_USERNAME}
                    mongodb_password=${env.MONGODB_PASSWORD}
                    """
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Docker 이미지 빌드
                    sh 'docker build -t rag_image .'
                }
            }
        }
        stage('Stop and Remove Old Container') {
            steps {
                script {
                    // 이미 실행 중인 컨테이너 중지 및 삭제
                    sh 'docker stop rag_container || true' // 중지 시도, 없는 경우 무시
                    sh 'docker rm rag_container || true' // 삭제 시도, 없는 경우 무시
                }
            }
        }
        stage('Run New Container') {
            steps {
                script {
                    // 새로운 Docker 컨테이너 실행
                    sh 'docker run -d -p 8000:8000 --env-file .env --name rag_container'
                }
            }
        } 
    }
}
