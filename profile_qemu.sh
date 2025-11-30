#!/bin/bash
echo "CPU и память до теста:"
vmstat 1 1

echo "Запускаем QEMU..."
perf stat -e cycles,instructions,cache-misses qemu-system-arm \
  -m 128 -M romulus-bmc -smp 1 \
  -kernel zImage -dtb romulus-bmc.dtb \
  -drive file=./flash,format=raw,if=mtd \
  -net nic -net user,hostfwd=:0.0.0.0:2443-:443 \
  -nographic &
QEMU_PID=$!

echo "Мониторим 10 секунд..."
vmstat 1 10

sleep 10
kill $QEMU_PID 2>/dev/null
wait $QEMU_PID 2>/dev/null

echo "Профилирование завершено"