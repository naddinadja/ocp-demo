from argparse import ArgumentParser
from pathlib import Path
from time import sleep
from threading import Thread
from requests import post


HOST = "localhost"
BATCHES = 300
PRETTY_NAME = {"aisio": "AiSIO", "gds": "GDS", "posix": "POSIX"}


def push(source: str):
  path = Path(__file__).parent / f"{source}.csv"
  sleep(2)

  with open(path, "r") as file:
    start = 0
    for line in file.readlines()[1:]:
      line = line.split(",")
      t = float(line[0])
      post(f"http://{HOST}/post?source={source}&data={','.join(line)}")
      sleep(t - start)
      start = t

    pn = PRETTY_NAME[source] if source in PRETTY_NAME else source
    print(f"\n{pn} done in {t:.1f}s")


def parse_args():
  global HOST 

  parser = ArgumentParser()
  parser.add_argument(
    "--dataserver",
    "-d",
    default="localhost",
    help="Hostname of server to push the benchmark results to.",
  )

  args = parser.parse_args()
  HOST = args.dataserver

  return args


if __name__ == "__main__":
  _ = parse_args()

  for source in ["xnvmeperf-cuda-run", "xnvmeperf-run", "cpu-utilization", "gpu-utilization"]:
    Thread(target=push, args=[source]).start()
