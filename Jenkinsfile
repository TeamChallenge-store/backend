pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker_compose/docker-compose.yml'
    }

    stages {
        stage('Clean Up Old Containers and Images') {
            steps {
                script {
                    sh 'sudo docker-compose -f $COMPOSE_FILE down'
                    sh 'sudo docker rm -f $(sudo docker ps -aq) || true'
                    sh 'sudo docker rmi -f $(sudo docker images -aq) || true'
                }
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'master', credentialsId: 'lox', url: 'https://github.com/TeamChallenge-store/backend.git'
            }
        }
        stage('Debug') {
            steps {
                script {
                    sh 'ls -l /var'
                    sh 'ls -l /var/lib/jenkins/workspace/backend'
                    sh 'sudo touch /var/lib/jenkins/workspace/backend/rest.json'
                    sh 'sudo touch /var/lib/jenkins/workspace/backend/.env_production'
                }
            }
        }

        stage('Copy Env Files') {
            steps {
                script {
                    sh 'sudo cp /var/.env_production /var/lib/jenkins/workspace/backend/.env_example'
                    sh 'sudo cp /var/rest.json /var/lib/jenkins/workspace/backend/rest.json'
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    sh 'sudo docker-compose -f $COMPOSE_FILE build'
                    sh 'sudo docker-compose -f $COMPOSE_FILE up -d'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'sudo docker exec django python manage.py test'
                }
            }
        }
    }
}
