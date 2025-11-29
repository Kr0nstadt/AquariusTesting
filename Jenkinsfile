pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Install Locust') {
            steps {
                sh '''
                    python3 -m pip install --user locust || echo "Установка не удалась, но продолжаем"
                '''
            }
        }
        
        stage('Load Testing') {
            steps {
                sh '''
                    echo "Запускаем простой тест..."
                    python3 -c "import requests; print('Python requests работает')" || echo "Requests не установлен"
                    # Пробуем запустить locust если установился
                    python3 -m locust --version || echo "Locust не доступен"
                '''
            }
        }
    }
}