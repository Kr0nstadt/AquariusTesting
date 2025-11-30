pipeline {
    agent any
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Check BMC Status') {
            steps {
                sh '''
                    curl -k https://localhost:2443/redfish/v1/ > bmc_status.log 2>&1
                    echo "=== BMC STATUS CHECK ===" >> bmc_status.log
                    date >> bmc_status.log
                '''
            }
        }
        
        stage('Run API Tests') {
            steps {
                sh '''
                    python -m pytest lab_fish_bylbyl.py -v > api_test.log 2>&1
                    echo "=== API TESTS COMPLETED ===" >> api_test.log
                    date >> api_test.log
                '''
            }
        }
        
        stage('Run WebUI Tests') {
            steps {
                sh '''
                    python -m pytest test_bebebe.py -v > webui_test.log 2>&1
                    echo "=== WEBUI TESTS COMPLETED ===" >> webui_test.log
                    date >> webui_test.log
                '''
            }
        }
        
        stage('Run Load Testing') {
            steps {
                sh '''
                    locust --headless -u 10 -r 1 --run-time 1m > load_test.log 2>&1
                    echo "=== LOAD TESTS COMPLETED ===" >> load_test.log
                    date >> load_test.log
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '*.log, *.html, *.py', fingerprint: true
        }
    }
}