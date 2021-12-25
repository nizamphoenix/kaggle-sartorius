import os
import re
import tempfile

import boto3
import botocore

from .common import make_dirs_for_file


def get_subfolders_in_bucket(bucket_name, folder):
    """
    Gets subfolders of a folder in an s3 bucket

    Parameters
    ----------
    bucket_name : string
        Name of S3 bucket
    folder : string
        Name of folder without leading and ending '/'
    Returns
    -------
    list of strings
        List of subfolder names
    """
    client = boto3.client("s3")
    result = client.list_objects(Bucket=bucket_name, Prefix=folder + "/", Delimiter="/")
    return [p.get("Prefix") for p in result.get("CommonPrefixes")]


def get_files_in_bucket(bucket_name, folder, suffix=None, file_contains=None):
    """
    Gets files from an S3 bucket, allows for searching of particular file types or
    containing certain keywords.

    Parameters
    ----------
    bucket_name : string
        Name of S3 bucket
    folder : string
        Name of folder, without leading and ending '/'
    suffix : string, optional
        File type of files, by default None
    file_contains : str, optional
        String contained in files, by default None

    Returns
    -------
    list of strings
        List of file keys found
    """
    # connect and get paginator
    s3_paginator = boto3.client("s3").get_paginator("list_objects_v2")
    # Get results
    file_list = []
    for page in s3_paginator.paginate(Bucket=bucket_name, Prefix=folder):
        for content in page.get("Contents", ()):
            file_key = content["Key"]
            if (suffix is None or file_key.lower().endswith(suffix)) and (
                file_contains is None or file_contains in file_key
            ):
                file_list.append(file_key)
    return file_list


def download_file(bucket_name, file_key, local_file_name=None, suffix=None):
    """
    Download a file from S3

    Parameters
    ----------
    bucket_name : string
        S3 bucket to download file from
    file_key : string
        Key of s3 file to download
    local_file_name : string, optional
        Local file location to download to, by default None. When None, a temporary file is made.
    suffix : string, optional
        Used to specify a filetype when generating a temporary file by setting file_name to None, by default None

    Returns
    -------
    file_name : string
        File path the file was downloaded to, helpful if setting as temporary file
    """
    # Set up
    if local_file_name is None:
        local_file_name = tempfile.mkstemp(suffix=suffix)[1]
    else:
        make_dirs_for_file(local_file_name)
    s3_client = boto3.client("s3")
    # download
    try:
        s3_client.download_file(
            Bucket=bucket_name, Key=file_key, Filename=local_file_name
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise FileNotFoundError
    return local_file_name


def download_file_if_needed(
    bucket_name, file_key, local_file_name, overwrite=False, verbose=False
):
    """
    Helper method for downloading a remote s3 file, but only if the local
    file doesn't already exist.

    Parameters
    ----------
    bucket_name : string
        S3 bucket to download file from
    file_key : string
        Key of s3 file to download
    local_file_name : string or None
        Key of s3 file to download. If None, the whole process is skipped
    overwrite : bool, optional
        Whether to overwrite the local file and force redownloading, by default False
    verbose : bool, optional
        Print outputs, by default False

    Return
    ------
    local_file_name : string
        Local file name for ease of re-storing in a variable
    """
    # Check arguments
    if local_file_name is None:
        raise ValueError("Local file must be provided")
    if file_key is not None and bucket_name is None:
        raise ValueError("If downloading a remote s3 file, s3_bucket must be provided")
    # Check if downloading file was requested (None indicates no remote file)
    if file_key is not None:
        file_exists = os.path.isfile(local_file_name)
        # Check if already exists
        if file_exists and not overwrite:
            if verbose:
                print("File {} already exists, using that".format(local_file_name))
            return local_file_name
        else:
            make_dirs_for_file(local_file_name)
            download_file(bucket_name, file_key, local_file_name=local_file_name)
            if verbose:
                print("Downloaded file {} to {}".format(file_key, local_file_name))

    return local_file_name


def download_folder(bucket_name, folder, output_dir, overwrite=False, verbose=False):
    """
    Download all files from a folder in s3 if they do not already exists

    Parameters
    ----------
    bucket_name : string
        S3 bucket to download the folder from
    folder : string
        Folder name in S3
    output_dir : string
        Local directory to save the files into
    overwrite : bool, optional
        Whether to overwrite the local file and force redownloading, by default False
    verbose : bool, optional
        Print outputs, by default False

    Returns
    -------
    None
    """
    # Get files to download
    files = get_files_in_bucket(bucket_name, folder)
    files = [file for file in files if file != folder + "/"]
    if verbose:
        print(
            "Found {} files in s3 folder {}: {}".format(
                len(files), folder, ", ".join(files)
            )
        )
    # Download each file
    for file in files:
        local_file = os.path.join(
            output_dir, file[len(folder) + 1 :]
        )  # Remove base folder
        # Check if its a folder, if it is we don't want to download it - just make
        if file[-1] == "/":
            os.makedirs(local_file, exist_ok=True)
        else:
            download_file_if_needed(
                local_file, file, bucket_name, overwrite=overwrite, verbose=verbose
            )


def download_folder_if_needed(
    local_dir, s3_dir=None, s3_bucket=None, overwrite=False, verbose=False
):
    """
    Downloads folder if it does not already exist at the local dir

    Parameters
    ----------
    local_dir : string
        Local directory for checking file existence
    folder : string
        Folder name in S3
    bucket_name : string
        S3 bucket to download folder from
    overwrite : bool, optional
        Whether to overwrite the local file and force redownloading, by default False
    verbose : bool
        Print outputs, by default False

    Returns
    -------
    None
    """
    # Check arguments
    if local_dir is None:
        raise ValueError("Local directory must be provided")
    if s3_dir is not None and s3_bucket is None:
        raise ValueError(
            "If downloading a remote s3 folder, s3_bucket must be provided"
        )
    # Check if downloading file was requested (None indicates no remote file)
    if s3_dir is not None:
        download_folder(
            s3_dir, local_dir, s3_bucket, overwrite=overwrite, verbose=verbose
        )


def save_pandas_df(preds, local_csv_path, s3_csv_file_key, bucket_name):
    """
    Save pandas df to local and/or s3 csv files

    Parameters
    ----------
    preds : pd.DataFrame
        DataFrame to be saved to specified locations
    local_csv_path : string
        Filename of local csv save location
    s3_csv_file_key : string
        File key of location in S3 to save csv to
    bucket_name : string
        S3 bucket to save to

    Returns
    -------
    None
    """
    # Check args
    if local_csv_path is None and s3_csv_file_key is None:
        print(
            "Both results_csv and results_s3_csv are none, at least one must be provided."
        )
    # Save
    if local_csv_path is not None:
        preds.to_csv(local_csv_path, index=False)
    if s3_csv_file_key is not None:
        str_output = preds.to_csv(None, index=False)
        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket_name, Body=str_output, Key=s3_csv_file_key)


def upload_file_to_bucket(local_file, file_key, bucket_name):
    """
    Upload file to s3 bucket

    Parameters
    ----------
    local_file : string
        Local file path to upload from
    file_key : string
        S3 key to upload file to
    bucket_name : string
        S3 bucket to upload file to

    Returns
    -------
    None
    """
    s3 = boto3.client("s3")
    s3.upload_file(local_file, bucket_name, file_key)


def upload_folder_to_s3_folder(local_folder, bucket_name, folder_prefix):
    """
    Upload folder to s3 folder preserving subdirectory structure

    Parameters
    ----------
    local_folder : string
        Local folder to upload to S3
    bucket_name : string
        S3 bucket to upload folder to
    folder_prefix : string
        Folder prefix to upload local folder to
    Returns
    -------
    None
    """
    folder_prefix = folder_prefix.rstrip("/")
    folder_prefix = folder_prefix + "/" if len(folder_prefix) > 0 else ""
    # Set up client connection
    s3 = boto3.client("s3")
    # Walk to get files
    for path, subdirs, files in os.walk(local_folder):
        path = path.replace("\\", "/")
        directory_name = re.sub(local_folder, "", path, 1)
        directory_name = directory_name.strip("/")
        directory_name = directory_name + "/" if len(directory_name) > 0 else ""
        # Upload each file
        for file in files:
            local_file = os.path.join(path, file)
            bucket_file = folder_prefix + directory_name + file
            print(
                f"Uploading {local_file} to {bucket_file}".format(
                    local_file, bucket_file
                )
            )
            s3.upload_file(local_file, bucket_name, bucket_file)


def get_s3_object_contents(bucket_name, file_key):
    """
    Get contents of a file in s3 bucket

    Parameters
    ----------
    bucket_name : string
        S3 bucket to get file contents from
    file_key : string
        File key to get contents of

    Returns
    -------
    body : byte string
        byte string representation of the object contents
    """
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket_name, file_key)
    body = obj.get()["Body"].read()
    return body


def check_file_exists(bucket_name, file_key):
    """
    Check if file is stored in s3 bucket

    Parameters
    ----------
    bucket_name : string
        S3 bucket name to check file existence within
    file_key : string
        File key to check existence of

    Returns
    -------
    bool
        True if file exists, False otherwise
    """
    s3 = boto3.resource("s3")
    try:
        s3.Object(bucket_name, file_key).load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            # The object does not exist.
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        return True
