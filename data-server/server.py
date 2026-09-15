import logging as log
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from flask import Flask, Response, request
from pandas import read_csv
from pathlib import Path


app = Flask(__name__)

DATA_PATH: Path = Path(".")
TIME_COLUMN: str = "Time"


@app.route("/data")
def get_data():
    global DATA_PATH, TIME_COLUMN

    try:
        data = request.args.get("source", type=str).lower()
        if data not in ["xnvmeperf-cuda-run", "xnvmeperf-run", "cpu-utilization", "gpu-utilization"]:
            log.error("Wrong source")
            return Response(None, 500)

        CSV_PATH = DATA_PATH / f"{data}.csv"
        df = read_csv(CSV_PATH)
        res = df.tail(1)

        return Response(res.to_csv(index=False), mimetype="text/csv")
    except Exception as e:
        log.error(e)
        return Response(None, 500)


@app.route("/post", methods = [ "POST" ])
def post():
    try:
        source = request.args.get("source", type=str).lower()
        if source not in ["xnvmeperf-cuda-run", "xnvmeperf-run", "cpu-utilization", "gpu-utilization"]:
            log.error(f"Wrong source({source})")
            return Response(None, 500)

        data = request.args.get("data", type=str)

        with open(DATA_PATH / f"{source}.csv", "a") as file:
            file.writelines([data])
    
    except Exception as e:
        log.error(e)
        return Response(None, 500)

    return Response(None, 200)


def setupLogging():
    logFormatter = log.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = log.getLogger()

    fileHandler = log.FileHandler(f"./server.log")
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(log.INFO)
    rootLogger.addHandler(fileHandler)

    consoleHandler = log.StreamHandler(stream=sys.stderr)
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(log.ERROR)
    rootLogger.addHandler(consoleHandler)


def parse_args():
    global DATA_PATH, TIME_COLUMN

    parser = ArgumentParser(
        prog=Path(sys.argv[0]).stem,
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data-path", 
        "-d", 
        type=Path, 
        default=Path("."),
        help="Path to to the data source CSV"
    )
    parser.add_argument(
        "--time-column", 
        "-t", 
        type=str, 
        default="Time",
        help="Name of the CSV column indicating time in milliseconds"
    )
    parser.add_argument(
        "--port", 
        "-p", 
        type=int, 
        default=4000,
        help="Port to host the Flask server on"
    )

    args = parser.parse_args()

    DATA_PATH = args.data_path.resolve()
    log.info(f"Path to data source: {DATA_PATH}")

    TIME_COLUMN = args.time_column
    log.info(f"Using column({args.time_column}) as time column")

    return args


if __name__ == "__main__":
    setupLogging()
    args = parse_args()

    app.run(host="0.0.0.0", port=args.port)
