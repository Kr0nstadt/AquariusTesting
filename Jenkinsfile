pipeline {
    agent any
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Start QEMU OpenBMC') {
            steps {
                sh '''
                    cd romulus
                    qemu-system-arm -m 256 -M romulus-bmc -nographic -drive file=obmc-phosphor-image-romulus-20250902012112.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623 &
                    echo $! > /tmp/qemu_pid.txt
                    sleep 90
                '''
            }
        }
        
        stage('Run API Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest lab_fish_bylbyl.py -v > api_test_results.log 2>&1
                    echo "<html><body><h1>API Test Results</h1>" > api_report.html
                    echo "<pre>" >> api_report.html
                    cat api_test_results.log >> api_report.html
                    echo "</pre></body></html>" >> api_report.html
                '''
            }
        }
        
        stage('Run WebUI Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_bebebe.py -v > webui_test_results.log 2>&1
                    echo "<html><body><h1>WebUI Test Results</h1>" > webui_report.html
                    echo "<pre>" >> webui_report.html
                    cat webui_test_results.log >> webui_report.html
                    echo "</pre></body></html>" >> webui_report.html
                '''
            }
        }
        
        stage('Run Load Testing') {
            steps {
                sh '''
                    . venv/bin/activate
                    locust --headless -u 10 -r 1 --run-time 1m > load_test_results.log 2>&1
                    echo "<html><body><h1>Load Test Report</h1>" > load_test_report.html
                    echo "<pre>" >> load_test_report.html
                    cat load_test_results.log >> load_test_report.html
                    echo "</pre></body></html>" >> load_test_report.html
                '''
            }
        }
        
        stage('Cleanup') {
            steps {
                sh '''
                    if [ -f /tmp/qemu_pid.txt ]; then
                        kill $(cat /tmp/qemu_pid.txt)
                        rm /tmp/qemu_pid.txt
                    fi
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '*.log, *.html', fingerprint: true
        }
    }
}