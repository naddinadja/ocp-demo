# syntax=docker/dockerfile:1
FROM python:3.11.13-bookworm

WORKDIR /app

COPY . .
RUN echo "Time,Batches,IOPS,MiB/s\n0,0,0,0" > xnvmeperf-run.csv
RUN echo "Time,Batches,IOPS,MiB/s\n0,0,0,0" > xnvmeperf-cuda-run.csv
RUN echo "Time,Util\n0,0" > cpu-utilization.csv
RUN echo "Time,Entity,PCITX,PCIRX,SMACT,SMOCC\n0,0,0,0,0,0" > gpu-utilization.csv

RUN pip install -r requirements.txt

EXPOSE 4000
CMD ["python3", "-u", "server.py"]