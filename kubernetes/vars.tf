variable "project" {
  type        = string
  description = "The GCP project to deploy to."
  default     = "steam-circlet-431420-m9"
}

variable "region" {
  type        = string
  description = "The GCP region to deploy to."
  default     = "eu-west2"
}

variable "zone" {
  type        = string
  description = "The GCP zone to deploy to."
  default     = "eu-west2-a"
}

