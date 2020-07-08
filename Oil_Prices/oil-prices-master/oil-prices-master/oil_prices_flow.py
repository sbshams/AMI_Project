from dataflows import (
    Flow,
    PackageWrapper,
    validate,
)
from dataflows import add_metadata, dump_to_path, load, set_type, printer


def rename_resources(package: PackageWrapper):
    package.pkg.descriptor["resources"][0]["name"] = "brent-daily"
    package.pkg.descriptor["resources"][0]["path"] = "data/brent-daily.csv"
    package.pkg.descriptor["resources"][1]["name"] = "brent-week"
    package.pkg.descriptor["resources"][1]["path"] = "data/brent-weekly.csv"
    package.pkg.descriptor["resources"][2]["name"] = "brent-month"
    package.pkg.descriptor["resources"][2]["path"] = "data/brent-monthly.csv"
    package.pkg.descriptor["resources"][3]["name"] = "brent-year"
    package.pkg.descriptor["resources"][3]["path"] = "data/brent-year.csv"
    package.pkg.descriptor["resources"][4]["name"] = "wti-daily"
    package.pkg.descriptor["resources"][4]["path"] = "data/wti-daily.csv"
    package.pkg.descriptor["resources"][5]["name"] = "wti-week"
    package.pkg.descriptor["resources"][5]["path"] = "data/wti-weekly.csv"
    package.pkg.descriptor["resources"][6]["name"] = "wti-month"
    package.pkg.descriptor["resources"][6]["path"] = "data/wti-monthly.csv"
    package.pkg.descriptor["resources"][7]["name"] = "wti-year"
    package.pkg.descriptor["resources"][7]["path"] = "data/wti-year.csv"

    yield package.pkg
    res_iter = iter(package)
    for res in res_iter:
        yield res.it
    yield from package


def filter_out_empty_rows(rows):
    for row in rows:
        if row["Date"]:
            yield row


OIL_PRICES = Flow(
    add_metadata(
        name="oil-prices",
        title="Brent and WTI Spot Prices",
        descriptor=(
            "A variety of temporal granularities for Europe Brent and WTI "
            "(West Texas Intermediate) Spot Prices."
        ),
        sources=[
            {
                "name": "Daily Europe Brent Spot Price",
                "path": "https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls",
                "title": "Daily Europe Brent Spot Price",
            },
            {
                "name": "Weekly Europe Brent Spot Price",
                "path": "https://www.eia.gov/dnav/pet/hist_xls/RBRTEw.xls",
                "title": "Weekly Europe Brent Spot Price",
            },
            {
                "name": "Monthly Europe Brent Spot Price",
                "path": "https://www.eia.gov/dnav/pet/hist_xls/RBRTEm.xls",
                "title": "Monthly Europe Brent Spot Price",
            },
            {
                "name": "Annual Europe Brent Spot Price",
                "path": "https://www.eia.gov/dnav/pet/hist_xls/RBRTEa.xls",
                "title": "Annual Europe Brent Spot Price",
            },
            {
                "name": "Daily Cushing, OK WTI Spot Price",
                "path": "http://www.eia.gov/dnav/pet/hist_xls/RWTCd.xls",
                "title": "Daily Cushing, OK WTI Spot Price",
            },
            {
                "name": "Weekly Cushing, OK WTI Spot Price",
                "path": "http://www.eia.gov/dnav/pet/hist_xls/RWTCw.xls",
                "title": "Weekly Cushing, OK WTI Spot Price",
            },
            {
                "name": "Monthly Cushing, OK WTI Spot Price",
                "path": "http://www.eia.gov/dnav/pet/hist_xls/RWTCm.xls",
                "title": "Monthly Cushing, OK WTI Spot Price",
            },
            {
                "name": "Annual Cushing, OK WTI Spot Price",
                "path": "http://www.eia.gov/dnav/pet/hist_xls/RWTCa.xls",
                "title": "Annual Cushing, OK WTI Spot Price",
            },
        ],
        licenses=[
            {
                "name": "ODC-PDDL-1.0",
                "path": "http://opendatacommons.org/licenses/pddl/",
                "title": "Open Data Commons Public Domain Dedication and License v1.0",
            }
        ],
        keywords=["Oil", "Brent", "WTI", "Oil Prices", "eia", "oil eia"],
        views=[
            {
                "name": "graph",
                "title": "Europe Brent Spot Price FOB (Dollars per Barrel)",
                "resourceName": "brent-day",
                "specType": "simple",
                "spec": {
                    "type": "line",
                    "group": "Date",
                    "series": ["Brent Spot Price"],
                },
            }
        ],
    ),
    load(
        load_source="https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    load(
        load_source="https://www.eia.gov/dnav/pet/hist_xls/RBRTEw.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    load(
        load_source="https://www.eia.gov/dnav/pet/hist_xls/RBRTEm.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    load(
        load_source="https://www.eia.gov/dnav/pet/hist_xls/RBRTEa.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    load(
        load_source="http://www.eia.gov/dnav/pet/hist_xls/RWTCd.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    load(
        load_source="http://www.eia.gov/dnav/pet/hist_xls/RWTCw.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    load(
        load_source="http://www.eia.gov/dnav/pet/hist_xls/RWTCm.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    load(
        load_source="http://www.eia.gov/dnav/pet/hist_xls/RWTCa.xls",
        format="xls",
        sheet=2,
        skip_rows=[1, 2, 3],
        headers=["Date", "Price"],
    ),
    rename_resources,
    set_type("Date", resources=None, type="date", format="any"),
    validate(),
    printer(),
    filter_out_empty_rows,
    dump_to_path(),
)


if __name__ == "__main__":
    OIL_PRICES.process()
