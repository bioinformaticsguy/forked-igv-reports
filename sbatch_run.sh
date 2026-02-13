python3 igv_reports/report.py \
    input_data/case_A5020_DNA_88_KIGS37_snv.subset.vcf.gz \
    --genome hg38  \
    --flanking 1000 \
    --info-columns GENE \
    --sample-columns DP GQ \
    --tracks input_data/case_A5020_DNA_88_KIGS37_snv.subset.vcf.gz /data/humangen_sfb1665_seqdata/short_read/processed_data/analysis_complete/A5020_DNA_88_KIGS37/alignment/A5020_DNA_88_KIGS37_sorted_md.bam \
    --title "IGV Variant Inspector" \
    --output example_vcf.html

# Could you send me a screenshot of an IGV view of this region so that 
# I can have a look if these variants are on different alleles?


## Generate the subset using the following command:
## bcftools view -r chr1:155660850-155660851 case_A5020_DNA_88_KIGS37_snv.vcf.gz | bgzip > two_variants_subset.vcf.gz && tabix -p vcf two_variants_subset.vcf.gz

# /data/humangen_kircherlab/Users/hassan/run_rare/rare-disease-pipeline/outputs/batch_mix_size6/A5020_DNA_98_GS467/alignment/A5020_DNA_98_GS467_sorted_md.bam


# python3 igv_reports/report.py \
#     test/data/variants/variants.vcf.gz \
#     --genome hg38  \
#     --flanking 1000 \
#     --info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
#     --sample-columns DP GQ \
#     --tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam \
#     --title "IGV Variant Inspector" \
#     --header test/example_header.html \
#     --footer test/example_footer.html \
#     --output example_vcf.html