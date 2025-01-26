terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = "keys/my-creds.json"
  project     = "essential-rider-449020-n1"
  region      = "us-central1"
  # Configuration options
}