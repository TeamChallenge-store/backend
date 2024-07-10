pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker_compose/docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', credentialsId: 'jenkins', url: 'https://github.com/TeamChallenge-store/backend.git'
            }
        }

        stage('Copy Env Files') {
            steps {
                script {
                    sh 'cp /var/.env_production /var/lib/jenkins/workspace/django_rest/.env_production'
                    sh 'cp /var/rest.json /var/lib/jenkins/workspace/django_rest/rest.json'
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    sh 'docker-compose -f $COMPOSE_FILE build'
                    sh 'docker-compose -f $COMPOSE_FILE up -d'
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    sh 'docker-compose -f $COMPOSE_FILE ps'
                }
            }
        }
    }

    post {
        always {
            script {
                sh 'docker-compose -f $COMPOSE_FILE logs'
            }
        }

        cleanup {
            script {
                sh 'docker-compose -f $COMPOSE_FILE down'

                sh 'sudo docker rm -f $(sudo docker ps -aq) || true'

                sh 'sudo docker rmi -f $(sudo docker images -aq) || true'
            }
        }
    }
}
