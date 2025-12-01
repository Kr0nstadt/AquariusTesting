pipeline {
    agent any
    
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                echo "=== SETUP ==="
                # Создаем папку для результатов
                rm -rf test_results
                mkdir -p test_results
                
                # Записываем информацию о запуске
                echo "Build: ${BUILD_NUMBER}" > test_results/build_info.txt
                echo "Job: ${JOB_NAME}" >> test_results/build_info.txt
                echo "Start time: $(date)" >> test_results/build_info.txt
                '''
            }
        }
        
        stage('Start BMC') {
            steps {
                sh '''
                echo "=== STARTING BMC ==="
                cd romulus
                
                # Запускаем QEMU с TCP вместо UDP для проблемного порта
                qemu-system-arm -m 256 -M romulus-bmc -nographic \\
                  -drive file=obmc-phosphor-image-romulus-20250902012112.static.mtd,format=raw,if=mtd \\
                  -net nic \\
                  -net user,hostfwd=tcp:0.0.0.0:2222-:22,hostfwd=tcp:0.0.0.0:2443-:443,hostfwd=tcp:0.0.0.0:2623-:623 &
                
                echo $! > ../test_results/qemu_pid.txt
                echo "QEMU PID: $(cat ../test_results/qemu_pid.txt)"
                
                # Ждем загрузки
                echo "Waiting 200 seconds for BMC..."
                sleep 200
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                echo "=== RUNNING TESTS ==="
                
                # Функция для запуска теста
                run_test() {
                    local test_name=$1
                    local test_file=$2
                    
                    echo "Running $test_name ($test_file)..."
                    echo "=== $test_name ===" > test_results/${test_name}.log
                    echo "Start: $(date)" >> test_results/${test_name}.log
                    
                    python3 $test_file >> test_results/${test_name}.log 2>&1
                    local exit_code=$?
                    
                    echo "Exit code: $exit_code" >> test_results/${test_name}.log
                    echo "End: $(date)" >> test_results/${test_name}.log
                    
                    return $exit_code
                }
                
                # Запускаем тесты
                run_test "lab_fish_bylbyl" "lab_fish_bylbyl.py" || true
                run_test "test_bebebe" "test_bebebe.py" || true
                
                # Проверяем locust
                if command -v locust &> /dev/null; then
                    echo "Running Locust..."
                    echo "=== Locust Test ===" > test_results/locust.log
                    timeout 30 locust -f locustfile.py --headless --users 1 --run-time 15s >> test_results/locust.log 2>&1 || true
                fi
                '''
            }
        }
        
        stage('Stop BMC') {
            steps {
                sh '''
                echo "=== STOPPING BMC ==="
                if [ -f test_results/qemu_pid.txt ]; then
                    QPID=$(cat test_results/qemu_pid.txt)
                    echo "Stopping QEMU (PID: $QPID)..."
                    kill $QPID 2>/dev/null || true
                    sleep 2
                    kill -9 $QPID 2>/dev/null || true
                    echo "QEMU stopped at: $(date)" >> test_results/build_info.txt
                fi
                '''
            }
        }
        
        stage('Generate Report') {
            steps {
                sh '''
                echo "=== GENERATING REPORT ==="
                
                # Создаем простой HTML отчет
                cat > test_results/report.html << EOF
                <html>
                <head>
                    <title>OpenBMC Test Report</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; }
                        .test { border: 1px solid #ccc; padding: 10px; margin: 10px 0; }
                        .success { background-color: #d4edda; }
                        .failed { background-color: #f8d7da; }
                        pre { background: #f4f4f4; padding: 10px; overflow: auto; }
                    </style>
                </head>
                <body>
                    <h1>OpenBMC Test Report</h1>
                    <p><strong>Build:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Date:</strong> $(date)</p>
                    <p><strong>Job:</strong> ${JOB_NAME}</p>
                    
                    <h2>Test Results</h2>
                EOF
                
                # Добавляем результаты каждого теста
                for test_file in test_results/*.log; do
                    test_name=$(basename "$test_file" .log)
                    last_line=$(tail -1 "$test_file" 2>/dev/null || echo "No output")
                    
                    echo "<div class='test'>" >> test_results/report.html
                    echo "<h3>$test_name</h3>" >> test_results/report.html
                    echo "<p><strong>Last line:</strong> $last_line</p>" >> test_results/report.html
                    echo "<details><summary>Show full log</summary><pre>" >> test_results/report.html
                    cat "$test_file" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' >> test_results/report.html
                    echo "</pre></details></div>" >> test_results/report.html
                done
                
                echo "</body></html>" >> test_results/report.html
                
                # Создаем текстовый отчет
                echo "=== FINAL REPORT ===" > test_results/final_report.txt
                echo "Build: ${BUILD_NUMBER}" >> test_results/final_report.txt
                echo "Date: $(date)" >> test_results/final_report.txt
                echo "" >> test_results/final_report.txt
                
                for test_file in test_results/*.log; do
                    test_name=$(basename "$test_file" .log)
                    echo "Test: $test_name" >> test_results/final_report.txt
                    echo "Last 3 lines:" >> test_results/final_report.txt
                    tail -3 "$test_file" >> test_results/final_report.txt 2>/dev/null || echo "No output" >> test_results/final_report.txt
                    echo "---" >> test_results/final_report.txt
                done
                '''
            }
        }
    }
    
    post {
        always {
            
            archiveArtifacts artifacts: 'test_results/**/*', allowEmptyArchive: true
            
            publishHTML(target: [
                reportName: 'Test Report',
                reportDir: 'test_results',
                reportFiles: 'report.html',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])
            
            sh '''
            echo "=== BUILD COMPLETED ==="
            echo "Results saved in: test_results/"
            echo ""
            echo "Test files:"
            ls -la test_results/
            '''
        }
        
        success {
            echo ' ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!'
        }
    }
}