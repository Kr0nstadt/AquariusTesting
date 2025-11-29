pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Устанавливаем зависимости..."
                    pip3 install locust
                '''
            }
        }
        
        stage('Load Testing') {
            steps {
                sh '''
                    echo "Запускаем нагрузочное тестирование Locust..."
                    locust --headless -u 10 -r 2 --run-time 1m --host=https://jsonplaceholder.typicode.com -f locustfile.py
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '**/*.html', fingerprint: true
        }
    }
}