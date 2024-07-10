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
                git branch: 'master', credentialsId: 'jenkins', url: 'https://github.com/TeamChallenge-store/backend.git'
            }
        }

        stage('Copy Env Files') {
            steps {
                script {
                    sh 'sudo cp /var/.env_production /var/lib/jenkins/workspace/django_rest/.env_production'
                    sh 'sudo cp /var/rest.json /var/lib/jenkins/workspace/django_rest/rest.json'
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
                    sh 'sudo docker exec -it django /bin/sh -c "python manage.py test"'
                }
            }
        }
    }
}
