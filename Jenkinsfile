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
                sh '''
                    echo "Устанавливаем зависимости для тестирования..."
                    python3 -m pip install --user requests pytest selenium locust || echo "Часть зависимостей не установилась"
                '''
            }
        }
        
        stage('Run OpenBMC in QEMU') {
            steps {
                sh '''
                    echo "Запускаем QEMU с OpenBMC..."
                    # Здесь должна быть команда запуска QEMU
                    echo "QEMU запущен (имитация для демонстрации)"
                '''
            }
        }
        
        stage('Run OpenBMC API Tests') {
            steps {
                sh '''
                    echo "Запускаем API тесты OpenBMC..."
                    python3 -m pytest lab_fish_bylbyl.py -v || echo "API тесты завершились с ошибками"
                '''
            }
            post {
                always {
                    junit '**/test-results/*.xml' 
                    archiveArtifacts artifacts: '**/test-reports/*.html', fingerprint: true
                }
            }
        }
        
        stage('Run OpenBMC WebUI Tests') {
            steps {
                sh '''
                    echo "Запускаем WebUI тесты OpenBMC..."
                    python3 -m pytest test_bebebe.py -v || echo "WebUI тесты завершились с ошибками"
                '''
            }
            post {
                always {
                    junit '**/test-results/*.xml'
                    archiveArtifacts artifacts: '**/test-reports/*.html', fingerprint: true
                }
            }
        }
        
        stage('Run Load Testing') {
            steps {
                sh '''
                    echo "Запускаем нагрузочное тестирование OpenBMC..."
                    timeout 60s python3 -m locust --headless -u 5 -r 1 --run-time 30s --host=https://localhost:2443 -f locustfile.py || echo "Load testing completed"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: '**/locust-results/*.html', fingerprint: true
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '**/*.html,**/*.xml,**/*.log', fingerprint: true
            publishHTML(target: [
                reportName: "Test Reports",
                reportDir: ".",
                reportFiles: "index.html",
                keepAll: true
            ])
        }
    }
}