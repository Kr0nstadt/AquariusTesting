echo "CPU и память до теста:"
vmstat 1 1

echo "Запускаем QEMU и мониторим 30 сек..."
vmstat 1 30 > vmstat_log.txt &

perf stat -e cycles,instructions,cache-misses qemu-system-arm \
  -m 256 -M romulus-bmc \
  -drive file=obmc-phosphor-image-romulus.static.mtd,format=raw,if=mtd \
  -net nic -net user,hostfwd=:0.0.0.0:2443-:443 \
  -nographic &
QEMU_PID=$!

sleep 30
kill $QEMU_PID

echo "Метрики за время теста:"
tail -n 30 vmstat_log.txt