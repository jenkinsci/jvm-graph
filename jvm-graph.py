import argparse
import datetime
import json
import matplotlib.pyplot
import matplotlib.ticker
import numpy
import os
import pandas
import urllib.request
import webbrowser

LTS_RELEASES = {6, 7, 8, 11, 17, 21, 25}


def determine_jvms(data_json):
    jvms = set()
    for report_data in data_json.values():
        for versions in report_data.values():
            for jvm in versions.keys():
                jvm = int(jvm.replace("1.", ""))
                jvms.add(jvm)
    return jvms


def parse(data_json, jvms):
    parsed = {}
    for jvm in sorted(jvms):
        parsed[jvm] = {}
        parsed[jvm]["entries"] = []
    report_data = data_json["jvmStatsPerMonth"]
    for ts_millis, versions in report_data.items():
        date = datetime.datetime.utcfromtimestamp(int(ts_millis) / 1000.0)
        for jvm, installations in versions.items():
            jvm = int(jvm.replace("1.", ""))
            entry = {"date": date, "installations": installations}
            parsed[jvm]["entries"].append(entry)
    for jvm in sorted(jvms):
        if jvm not in LTS_RELEASES:
            continue
        date_to_installations = {}
        for entry in sorted(parsed[jvm]["entries"], key=lambda x: x["date"]):
            if entry["date"] in date_to_installations:
                raise ValueError("duplicate")
            else:
                date_to_installations[entry["date"]] = entry["installations"]
        parsed[jvm]["dates"] = []
        parsed[jvm]["installations"] = []
        for date in sorted(date_to_installations):
            parsed[jvm]["dates"].append(date)
            parsed[jvm]["installations"].append(date_to_installations[date])
    return parsed


def display(parsed, jvms, output):
    matplotlib.pyplot.figure(dpi=300)
    for jvm in sorted(jvms):
        if jvm not in LTS_RELEASES:
            continue
        df = pandas.DataFrame(
            {
                "date": numpy.array(parsed[jvm]["dates"]),
                jvm: parsed[jvm]["installations"],
            }
        )
        matplotlib.pyplot.plot(df["date"].values, df[jvm].values, label=jvm)
    matplotlib.pyplot.gca().get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    matplotlib.pyplot.title("JVMs by Date", fontweight="bold")
    matplotlib.pyplot.xlabel("Date", fontweight="bold")
    matplotlib.pyplot.ylabel("# of Installations", fontweight="bold")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.savefig(output, format="png", dpi=300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-o",
        "--output",
        default="jvm-graph.png",
        help="The name of the output file to create.",
    )
    parser.add_argument(
        "-j",
        "--jvms-json",
        default="https://stats.jenkins.io/plugin-installation-trend/jvms.json",
        help="The plugin installation trend JVMs JSON file to fetch.",
    )
    parser.add_argument(
        "--open",
        action=argparse.BooleanOptionalAction,
        default="CI" not in os.environ,
        help="Open the output file after creating it.",
    )
    args = parser.parse_args()
    with urllib.request.urlopen(args.jvms_json) as url:
        data = json.load(url)
        jvms = determine_jvms(data)
        parsed = parse(data, jvms)
        display(parsed, jvms, args.output)
        if args.open:
            webbrowser.open_new_tab(args.output)
