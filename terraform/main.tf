terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }

  backend "gcs" {
    bucket = "terraform_sashka"
    prefix = "vm"
  }
}

provider "google" {
  project = "absolute-cache-433511-d3"
  region  = "europe-west3"
  zone    = "europe-west3-a"
}
