terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project     = "essential-rider-449020-n1"
  region      = "us-central1"
  # Configuration options
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "essential-rider-449020-n1"
  location      = "US"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 1  // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = "test_dataset_449020"
  project     = "essential-rider-449020-n1"
  location   = "US"
}