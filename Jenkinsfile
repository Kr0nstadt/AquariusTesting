pipeline {
    agent any
    
    stages {
        stage('Run All') {
            steps {
                sh '''
                echo "=== STARTING TESTS ==="
                pwd
                
                # 1. Запускаем QEMU
                echo "=== Starting BMC emulation ==="
                cd romulus
                qemu-system-arm -m 256 -M romulus-bmc -nographic \
                  -drive file=obmc-phosphor-image-romulus-20250902012112.static.mtd,format=raw,if=mtd \
                  -net nic \
                  -net user,hostfwd=tcp:0.0.0.0:2222-:22 &
                QPID=$!
                echo "QEMU PID: $QPID" > qemu_info.txt
                
                # 2. Ждем загрузки
                echo "Waiting 200 seconds..."
                sleep 200
                
                # 3. Запускаем тесты
                cd ..
                echo "=== Running tests ===" > test_report.txt
                echo "Start time: $(date)" >> test_report.txt
                echo "" >> test_report.txt
                
                # Тест 1
                echo "--- Test 1: lab_fish_bylbyl.py ---" >> test_report.txt
                python3 lab_fish_bylbyl.py 2>&1 >> test_report.txt || echo "Exit code: $?" >> test_report.txt
                echo "" >> test_report.txt
                
                # Тест 2
                echo "--- Test 2: test_bebebe.py ---" >> test_report.txt
                python3 test_bebebe.py 2>&1 >> test_report.txt || echo "Exit code: $?" >> test_report.txt
                echo "" >> test_report.txt
                
                # Locust тест (если есть файл)
                echo "--- Test 3: Locust load test ---" >> test_report.txt
                if [ -f locustfile.py ]; then
                    timeout 30 locust -f locustfile.py --headless --users 1 --run-time 10s 2>&1 >> test_report.txt || echo "Locust finished" >> test_report.txt
                else
                    echo "Locust file not found, skipping" >> test_report.txt
                fi
                echo "" >> test_report.txt
                
                # 4. Останавливаем QEMU
                echo "=== Stopping QEMU ===" >> test_report.txt
                kill $QPID 2>/dev/null || echo "QEMU already stopped" >> test_report.txt
                echo "End time: $(date)" >> test_report.txt
                
                # 5. Выводим краткий отчет
                echo ""
                echo "=== TEST COMPLETED ==="
                echo "See test_report.txt for details"
                '''
            }
        }
    }
    
    post {
        always {
            // Сохраняем только нужные файлы
            archiveArtifacts artifacts: 'test_report.txt, romulus/qemu_info.txt'
            
            // Показываем результат в консоли
            sh '''
            echo "=== FINAL REPORT ==="
            cat test_report.txt
            '''
        }
    }
}