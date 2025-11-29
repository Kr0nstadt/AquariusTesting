pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install locust'
            }
        }
        
        stage('Load Testing') {
            steps {
                sh 'locust --headless -u 5 -r 1 --run-time 30s --host=https://jsonplaceholder.typicode.com -f locustfile.py'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '**/*.html', fingerprint: true
        }
    }
}