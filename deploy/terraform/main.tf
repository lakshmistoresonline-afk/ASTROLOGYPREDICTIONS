# Terraform Manifest for Astrological Intelligence Engine Infrastructure
provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" { default = "astrology-predictions-prod" }
variable "region"     { default = "us-central1" }

# Managed Redis Instance
resource "google_redis_instance" "ephemeris_cache" {
  name           = "ephemeris-cache-redis"
  memory_size_gb = 2
  tier           = "BASIC"
  region         = var.region

  redis_config = {
    maxmemory-policy = "volatile-lru"
  }
}

# Auto-Scaling Cloud Run / Kubernetes API Service
resource "google_cloud_run_service" "astro_api" {
  name     = "astro-predictions-api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/astro-predictions-api:v3.36"
        resources {
          limits = {
            cpu    = "2000m"
            memory = "2Gi"
          }
        }
        env {
          name  = "REDIS_URL"
          value = google_redis_instance.ephemeris_cache.host
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
