# Grafana dashboard for benchmark results

This is a small setup for animating a benchmarking dashboard for AiSiO, GDS, POSIX and
BaM. The `docker-compose.yaml` hosts multiple docker containers with Grafana, the
dashboard, and a data-server. It is all behind a reverse proxy and can be accessed on
port 80.

This repository is reused and overwritten when new demos are needed. Git tags are used
to reference older demos.

## Run

To view the dashboard, run

```sh
docker compose up --build
```

and go to `http://localhost`.

## Data

The data server has no data to begin with, but has an endpoint on `/post`, wich expects
2 parameters:

- `source`: the CSV file that you want to save the data to. See the Dockerfile for the
  data server (`./data-server/Dockerfile`) for which files are available (or add more).
- `data`: a single CSV line with comma-separated columns.

Examples:

- `http://localhost/post?source=posix&data=0,0,0,0\n`
- `http://localhost/post?source=gpu-utilization&data=0.0,0,0,0,0,0\n`

The `misc/push.py` script can be used to push data from a local file to the data server
endpoint at the correct intervals.

## Grafana

Grafana dashboards are saved as JSON files in `./grafana/dashboards`. To modify
them, start the docker compose and go to `http://localhost/grafana`. From here, you
can modify or create new dashboards. To save modified dashboards, click the "Save"
button and copy the JSON object into the correct file in `./grafana/dashboards`. To
save a created dashboard, you need to find the JSON object in the settings and
create the JSON file in `./grafana/dashboards`.

### Live updating

The following settings must be set on each dahsboard in order to enable live
updating of the dashboard when embedded in the demo webpage.

```json
{
  // ...
  "liveNow": true,
  // ...
  "refresh": "500ms",
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {
    "hidden": true,
    "refresh_intervals": [
      "500ms",
      "1s",
      "5s"
    ]
  },
  "timezone": "",
  // ...
}
```
