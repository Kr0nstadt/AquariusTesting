pipeline {
    agent any
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    parameters {
        string(name: 'TEST_TIMEOUT', defaultValue: '600', description: 'Timeout for tests in seconds')
        string(name: 'BMC_BOOT_WAIT', defaultValue: '180', description: 'Time to wait for BMC boot in seconds')
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Kr0nstadt/AquariusTesting.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    // Устанавливаем необходимые зависимости
                    sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install pytest locust
                    '''
                    
                    // Проверяем наличие qemu
                    sh '''
                    which qemu-system-arm || echo "QEMU not found, installing..."
                    '''
                }
            }
        }
        
        stage('Start OpenBMC') {
            steps {
                script {
                    dir('romulus') {
                        // Запускаем OpenBMC в фоне
                        sh '''
                        echo "Starting OpenBMC emulation..."
                        nohup qemu-system-arm \
                          -m 256 \
                          -M romulus-bmc \
                          -nographic \
                          -drive file=obmc-phosphor-image-romulus-20250902012112.static.mtd,format=raw,if=mtd \
                          -net nic \
                          -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623 \
                          > qemu.log 2>&1 &
                        
                        echo $! > qemu.pid
                        echo "QEMU started with PID: $(cat qemu.pid)"
                        '''
                        
                        // Ждем загрузки OpenBMC
                        sh """
                        echo "Waiting ${params.BMC_BOOT_WAIT} seconds for OpenBMC to boot..."
                        sleep ${params.BMC_BOOT_WAIT}
                        
                        echo "Checking if BMC is responsive..."
                        # Проверяем доступность SSH (порт 2222)
                        timeout 60 bash -c 'until nc -z localhost 2222; do sleep 5; echo "Waiting for SSH..."; done'
                        echo "BMC SSH is up!"
                        
                        # Проверяем доступность HTTPS (порт 2443)
                        timeout 60 bash -c 'until nc -z localhost 2443; do sleep 5; echo "Waiting for HTTPS..."; done'
                        echo "BMC HTTPS is up!"
                        """
                    }
                }
            }
        }
        
        stage('Run Python Tests') {
            steps {
                script {
                    // Создаем директорию для отчетов
                    sh 'mkdir -p test-reports'
                    
                    dir('.') {
                        // Запускаем pytest тесты
                        sh '''
                        echo "Running pytest tests..."
                        python3 -m pytest lab_fish_bylbyl.py \
                            -v \
                            --junitxml=test-reports/pytest-results.xml \
                            --html=test-reports/pytest-report.html \
                            --self-contained-html \
                            --timeout=${TEST_TIMEOUT} || true
                        
                        echo "Running test_bebebe.py..."
                        python3 -m pytest test_bebebe.py \
                            -v \
                            --junitxml=test-reports/pytest-bebebe-results.xml \
                            --html=test-reports/pytest-bebebe-report.html \
                            --self-contained-html \
                            --timeout=${TEST_TIMEOUT} || true
                        '''
                    }
                }
            }
        }
        
        stage('Run Locust Tests') {
            steps {
                script {
                    dir('.') {
                        // Запускаем Locust тесты в фоне, собираем статистику и завершаем
                        sh '''
                        echo "Starting Locust tests..."
                        nohup locust \
                            -f locustfile.py \
                            --headless \
                            --users 10 \
                            --spawn-rate 1 \
                            --run-time 2m \
                            --csv=test-reports/locust \
                            --html=test-reports/locust-report.html \
                            > test-reports/locust.log 2>&1 &
                        
                        echo $! > locust.pid
                        echo "Locust started with PID: $(cat locust.pid)"
                        
                        # Ждем завершения тестов
                        sleep 130
                        
                        # Проверяем, работает ли еще locust
                        if kill -0 $(cat locust.pid) 2>/dev/null; then
                            echo "Stopping Locust gracefully..."
                            kill $(cat locust.pid)
                            sleep 5
                        fi
                        '''
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    // Останавливаем QEMU
                    sh '''
                    echo "Cleaning up..."
                    
                    # Останавливаем Locust если еще работает
                    if [ -f locust.pid ] && kill -0 $(cat locust.pid) 2>/dev/null; then
                        kill -9 $(cat locust.pid) 2>/dev/null || true
                        rm -f locust.pid
                    fi
                    
                    # Останавливаем QEMU
                    if [ -f romulus/qemu.pid ]; then
                        echo "Stopping QEMU..."
                        kill -9 $(cat romulus/qemu.pid) 2>/dev/null || true
                        rm -f romulus/qemu.pid
                    fi
                    
                    # Удаляем временные файлы
                    rm -f nohup.out
                    '''
                }
            }
        }
    }
    
    post {
        always {
            // Сохраняем артефакты
            archiveArtifacts artifacts: 'test-reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'romulus/qemu.log', allowEmptyArchive: true
            
            // Публикуем отчеты
            junit 'test-reports/*.xml'
            
            // Публикуем HTML отчеты
            publishHTML(target: [
                reportName: 'Pytest Report',
                reportDir: 'test-reports',
                reportFiles: 'pytest-report.html',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])
            
            publishHTML(target: [
                reportName: 'Locust Report',
                reportDir: 'test-reports',
                reportFiles: 'locust-report.html',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])
            
            // Очистка
            cleanWs()
        }
        
        success {
            echo 'All tests completed successfully!'
        }
        
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}