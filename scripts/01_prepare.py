from src.prepare import prepare
import argparse
ap=argparse.ArgumentParser()
ap.add_argument("--input",required=True)
ap.add_argument("--output",default="data/processed/apple_pairs.csv")
ap.add_argument("--brand",default="AppleSupport")
ap.add_argument("--max-pairs",type=int,default=60000)
a=ap.parse_args()
prepare(a.input,a.output,a.brand,a.max_pairs)
