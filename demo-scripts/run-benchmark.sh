#! /bin/bash


clear
xnvmeperf cuda-run $(cat ~/git/misc/bdfs_node0.txt) --be upcie-cuda --gpu_id 0 --iopattern randread \
  --iosize 512 --qdepth 128 --runtime 20 --nqueues 4 --sq-hostmem --report-freq 0.5

xnvmeperf run $(cat ~/git/misc/bdfs_node1.txt) --be upcie --iopattern randread --iosize 512 \
  --qdepth 128 --runtime 20 --cpulist 3,5 --report-freq 0.5