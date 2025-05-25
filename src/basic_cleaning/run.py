#!/usr/bin/env python
"""
APerforms basic cleaning on the data and saves the results in W&B
"""
import argparse
import logging
import wandb

import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE #
    logger.info("Downloading input artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    df = pd.read_csv(artifact_path)

    # Set min and max price
    logger.info("Setting min and max price")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    logger.info("Setting 'last_review' column to datetime dtype")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Saving results to csv
    logger.info("Saving clean data to csv")
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    
    logger.info("Logging artifact")
    run.log_artifact(artifact)
    
    ######################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Raw data",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Cleaned data",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type for output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description for output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum value of 'price' column",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum value of 'price' column",
        required=True
    )


    args = parser.parse_args()

    go(args)
