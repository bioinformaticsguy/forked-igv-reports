#!/usr/bin/env python3
"""
Config-driven IGV report generator.

Reads a YAML config file defining cases (VCF, BAM, regions) and generates
IGV HTML reports by:
  1. Subsetting the VCF to the specified regions (bcftools + tabix)
  2. Calling igv-reports create_report() to build the HTML

Usage:
    python generate_reports.py config.yaml
"""

import argparse
import os
import subprocess
import sys

import yaml

from igv_reports.report import create_report


def subset_vcf(vcf_path, regions, output_vcf):
    """Subset a VCF to specified regions using bcftools and index with tabix."""
    regions_str = ",".join(regions)

    cmd = f"bcftools view -r {regions_str} {vcf_path} | bgzip > {output_vcf}"
    print(f"  Subsetting VCF: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR subsetting VCF: {result.stderr}", file=sys.stderr)
        return False

    cmd_index = f"tabix -p vcf {output_vcf}"
    print(f"  Indexing: {cmd_index}")
    result = subprocess.run(cmd_index, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR indexing VCF: {result.stderr}", file=sys.stderr)
        return False

    return True


def build_report_args(case, subset_vcf_path, output_html, global_config):
    """Build an argparse.Namespace matching what create_report() expects."""
    tracks = [subset_vcf_path] + case.get("bam", [])

    args = argparse.Namespace(
        sites=subset_vcf_path,
        fasta_=None,
        fasta=case.get("fasta", global_config.get("fasta")),
        twobit=case.get("twobit", global_config.get("twobit")),
        genome=case.get("genome", global_config.get("genome")),
        type=case.get("type"),
        ideogram=case.get("ideogram"),
        tracks=tracks,
        track_config=case.get("track_config"),
        roi=case.get("roi"),
        sort=case.get("sort"),
        template=case.get("template"),
        output=output_html,
        info_columns=case.get("info_columns"),
        info_columns_prefixes=case.get("info_columns_prefixes"),
        sampleinfo=case.get("sampleinfo"),
        samples=case.get("samples"),
        sample_columns=case.get("sample_columns"),
        flanking=case.get("flanking", global_config.get("flanking", 1000)),
        window=case.get("window"),
        standalone=case.get("standalone", False),
        title=case.get("title", case["name"]),
        header=case.get("header"),
        footer=case.get("footer"),
        sequence=None,
        begin=None,
        end=None,
        zero_based=None,
        idlink=case.get("idlink"),
        exclude_flags=case.get("exclude_flags", 1536),
        no_embed=case.get("no_embed", False),
        subsample=case.get("subsample"),
        maxlen=case.get("maxlen", 10000),
        translate_sequence_track=case.get("translate_sequence_track", False),
        tabulator=case.get("tabulator", False),
        filter_config=case.get("filter_config"),
        merge_overlaps=case.get("merge_overlaps", False),
    )
    return args


def process_case(case, global_config):
    """Process a single case: subset VCF, generate report."""
    name = case["name"]
    print(f"\nProcessing case: {name}")

    output_dir = os.path.join(
        global_config.get("output_dir", "reports"),
        name
    )
    os.makedirs(output_dir, exist_ok=True)

    # Subset VCF
    subset_path = os.path.join(output_dir, f"{name}_subset.vcf.gz")
    if not subset_vcf(case["vcf"], case["regions"], subset_path):
        print(f"  Skipping case {name} due to VCF subset error.")
        return False

    # Generate report
    output_html = os.path.join(output_dir, f"{name}_report.html")
    args = build_report_args(case, subset_path, output_html, global_config)

    print(f"  Generating report: {output_html}")
    try:
        create_report(args)
        print(f"  Done: {output_html}")
        return True
    except Exception as e:
        print(f"  ERROR generating report for {name}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate IGV HTML reports from a YAML config file."
    )
    parser.add_argument("config", help="Path to YAML configuration file")
    cli_args = parser.parse_args()

    with open(cli_args.config, "r") as f:
        config = yaml.safe_load(f)

    cases = config.get("cases", [])
    if not cases:
        print("No cases defined in config file.", file=sys.stderr)
        sys.exit(1)

    success = 0
    for case in cases:
        if process_case(case, config):
            success += 1

    print(f"\nCompleted: {success}/{len(cases)} reports generated.")


if __name__ == "__main__":
    main()
