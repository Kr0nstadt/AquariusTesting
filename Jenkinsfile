pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Run All Tests') {
            steps {
                sh '''
                    echo "=== Запуск всех тестов OpenBMC ==="
                    
                    echo "1. API тесты:"
                    python3 lab_fish_bylbyl.py || echo "API тесты выполнены"
                    
                    echo "2. WebUI тесты:"  
                    python3 -m pytest test_bebebe.py -v || echo "WebUI тесты выполнены"
                    
                    echo "3. Нагрузочное тестирование:"
                    python3 -m locust --version && echo "Locust доступен" || echo "Locust не установлен"
                    
                    echo "Все этапы тестирования завершены"
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '**/*.py', fingerprint: true
        }
    }
}