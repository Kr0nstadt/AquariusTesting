pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                sh '''
                # 1. Проверяем код
                git clone https://github.com/Kr0nstadt/AquariusTesting.git
                cd AquariusTesting
                
                # 2. Запускаем QEMU (если нужно)
                cd romulus
                qemu-system-arm -m 256 -M romulus-bmc -nographic \
                  -drive file=obmc-phosphor-image-romulus-20250902012112.static.mtd,format=raw,if=mtd \
                  -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623 &
                sleep 180
                
                # 3. Запускаем тесты
                cd ..
                python3 lab_fish_bylbyl.py || echo "Test 1 done"
                python3 test_bebebe.py || echo "Test 2 done"
                
                # 4. Останавливаем QEMU
                pkill qemu-system-arm
                '''
            }
        }
    }
}