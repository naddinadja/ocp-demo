# Notes

## asciinema

In 2026, the Asciinema casts are created with the following commands:

```bash
# DIO - kernel 
asciinema rec dio.cast -c 'LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu /root/llama.cpp/build/bin/llama-cli -m /mnt/ssd0/models/llama33-70b-q6k-00001-of-00004.gguf -ngl 99 -ot token_embd.weight=CUDA0 -c 4096 -p "hello" -n 16 -st --no-warmup --load-mode dio -v 2> dio.log; awk -f /root/loadtime.awk dio.log'

# MMAP - kernel
asciinema rec mmap.cast -c 'LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu /root/llama.cpp/build/bin/llama-cli -m /mnt/ssd0/models/llama33-70b-q6k-00001-of-00004.gguf -ngl 99 -ot token_embd.weight=CUDA0 -c 4096 -p "hello" -n 16 -st --no-warmup --load-mode mmap -v 2> mmap.log; awk -f /root/loadtime.awk mmap.log'

# OPENDS - served
asciinema rec opends.cast -c 'LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu OPENDS_AISIO_IO_THREADS=8 OPENDS_AISIO_QUEUE_DEPTH=32 /root/llama.cpp/build/bin/llama-cli -m /mnt/ssd0/models/llama33-70b-q6k-00001-of-00004.gguf -ngl 99 -ot token_embd.weight=CUDA0 -c 4096 -p "hello" -n 16 -st --no-warmup --load-mode opends -v 2> opends.log; awk -f /root/loadtime.awk opends.log'

asciinema rec opends1drive.cast -c 'LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu OPENDS_AISIO_IO_THREADS=8 OPENDS_AISIO_QUEUE_DEPTH=32 /usr/bin/time -p /root/llama.cpp/build/bin/llama-cli -m /mnt/ssd0/models/Llama-3.3-70B-Instruct-Q6_K.gguf -ngl 99 -ot token_embd.weight=CUDA0 -c 4096 -p "hello" -n 16 -st --no-warmup --load-mode opends -v --log-colors off 2> opends1drive.log; awk -f /root/loadtime.awk opends1drive.log'
```

Remember to set up the environment between runs, and to clear caches with command:

```bash
sync; echo 3 > /proc/sys/vm/drop_caches
```

The load time is reported with an .awk helper, which basically just finds the time
stamps for when llama-cli begins loading the model tensors, and when the tensor
copy finished. It subtracts the two time stamps and prints the time nicely, and the
load rate, which is reported at the end line.

```bash
{ gsub(/\033\[[0-9;]*m/, "") }
/loading model tensors.*load_mode = (mmap|dio|opends)/ { t = $0; sub(/^[^0-9]*/, "", t); split(t, a, "."); s = a[1]*60 + a[2] + a[3]/1e3 + a[4]/1e6 }
/load_all_data: [0-9.]+ MiB in/ { t = $0; sub(/^[^0-9]*/, "", t); split(t, a, "."); e = a[1]*60 + a[2] + a[3]/1e3 + a[4]/1e6; split($0, b, "load_all_data: "); m = b[2] + 0 }
END { printf "load %.2f s\n", e - s }
```

## xnvmeperf benchmarking

The numbers in `xnvmeperf-run.csv`, `xnvmeperf-cuda-run.csv`, `cpu-utilization.csv`
and `gpu-utilization.csv` in the `misc` directory comes from running the following
commands:

```bash
xnvmeperf run $(cat ~/git/misc/bdfs_node1.txt) --be upcie --iopattern randread --iosize 512 --qdepth 128 --runtime 30 --cpulist 3,5 --report-freq 0.5

xnvmeperf cuda-run $(cat ~/git/misc/bdfs_node0.txt) --be upcie-cuda --gpu_id 0 --iopattern randread --iosize 512 --qdepth 128 --runtime 30 --nqueues 2 --sq-hostmem --report-freq 0.5

mpstat 1 | awk '/^[0-9]/ {print 100 - $NF}'

dcgmi dmon -d 500 -i 0 -e 1009,1010,1002,1003
```

## Pushing data to the data-server

Notice `data-server/Dockerfile`, where the data files are defined. If you decide to
have other CSV files with other columns for your grafana dashboard, these should be
added both in this Dockerfile, but also incorporated in `misc/push.py`, which is
responsible for pushing data from the local machine to the data server.

Data should be on your local machine as CSV with an empty line in the end. If you start
the push script and stop it mid-way, you might end up with the next push adding data
to the same line as where the previous run ended. This will corrupt the data file and
it will not be possible to read from it again. You can enter the Docker container and
remove the line from the file. You enter the file with the following command:

```bash
# "data" is the docker ID of the data-server container.
docker exec -it data /bin/bash
```
