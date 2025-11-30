pipeline {
    agent any
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Start QEMU OpenBMC') {
            steps {
                sh '''
                    cd romulus
                    qemu-system-arm -m 256 -M romulus-bmc -nographic -drive file=obmc-phosphor-image-romulus-20250902012112.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623 &
                    echo $! > /tmp/qemu_pid.txt
                    sleep 90
                    curl -k https://localhost:2443/redfish/v1/ > qemu_start.log 2>&1 || echo "QEMU starting..." > qemu_start.log
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
        
        stage('Cleanup') {
            steps {
                sh '''
                    if [ -f /tmp/qemu_pid.txt ]; then
                        kill $(cat /tmp/qemu_pid.txt) 2>/dev/null || true
                        rm /tmp/qemu_pid.txt
                        echo "QEMU stopped" > cleanup.log
                    fi
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