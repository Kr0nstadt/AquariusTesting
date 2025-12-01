pipeline {
    agent any
    
    stages {
        stage('Run All') {
            steps {
                sh '''
                # 1. Убедимся что мы в правильной директории
                pwd
                ls -la
                
                # 2. Запускаем QEMU в romulus папке
                cd romulus
                echo "Starting QEMU..."
                qemu-system-arm -m 256 -M romulus-bmc -nographic \\
                  -drive file=obmc-phosphor-image-romulus-20250902012112.static.mtd,format=raw,if=mtd \\
                  -net nic \\
                  -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623 &
                QPID=$!
                echo "QEMU PID: $QPID" > /tmp/qemu_info.txt
                
                # 3. Ждем
                sleep 200
                
                # 4. Запускаем тесты
                cd ..
                echo "Test 1 output:" > my_results.txt
                python3 lab_fish_bylbyl.py >> my_results.txt 2>&1 || echo "Test 1 done" >> my_results.txt
                echo "" >> my_results.txt
                echo "Test 2 output:" >> my_results.txt
                python3 test_bebebe.py >> my_results.txt 2>&1 || echo "Test 2 done" >> my_results.txt
                
                # 5. Убиваем QEMU
                kill $QPID 2>/dev/null || true
                '''
            }
        }
    }
    
    post {
        always {
            // Сохраняем
            archiveArtifacts artifacts: 'my_results.txt, /tmp/qemu_info.txt', allowEmptyArchive: true
        }
    }
}