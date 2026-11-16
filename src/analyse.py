from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dataset.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA)


# KPI outputs and chart
summary = df.groupby("quality_status").size().rename("records").reset_index()
summary["share_pct"] = (100*summary.records/len(df)).round(2)
source = df.groupby("source_system").agg(
    records=("record_id","count"),
    missing_email_pct=("email_present",lambda x:100*(1-x.mean())),
    invalid_postcode_pct=("postcode_valid",lambda x:100*(1-x.mean())),
    duplicate_pct=("duplicate_flag",lambda x:100*x.mean()),
    pii_format_failure_pct=("pii_format_valid",lambda x:100*(1-x.mean()))
).reset_index().round(2)
daily = df.groupby("ingestion_date").apply(lambda x:(x.quality_status!="PASS").sum(),include_groups=False).rename("exception_records").reset_index()
summary.to_csv(OUT/"quality_summary.csv",index=False)
source.to_csv(OUT/"source_quality.csv",index=False)
daily.to_csv(OUT/"daily_exceptions.csv",index=False)
plt.figure(figsize=(8,4)); plt.bar(summary.quality_status,summary.records); plt.title("Record quality status — synthetic data"); plt.ylabel("Records"); plt.tight_layout(); plt.savefig(OUT/"quality_status.png",dpi=150)
print(source.to_string(index=False))
