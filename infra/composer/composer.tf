variable "project_id" {}
variable "region" {}
variable "network" {}
variable "subnetwork" {}
variable "sa" {}
variable "composer_image_version" {}
variable "composer_cron_scheduler" {}

resource "google_composer_environment" "composer" {
  name      = "fasttrack-composer"
  project   = var.project_id 
  region    = var.region
  config {

    software_config {
        image_version = var.composer_image_version
        pypi_packages = {
            "pandas"=""
            "fsspec"=""
            "gcsfs"=""
            "aiohttp"="==3.8.1"
            "openpyxl"=""
            "requests"=""
            "validators"=""
            "retrying"=""
            "numpy"=""
        }
        airflow_config_overrides = {
            core-dags_are_paused_at_creation = "True"
        }
        env_variables = {
            PROJECT_ID      = var.project_id
            CRON_SCHEDULER  = var.composer_cron_scheduler
        }
    }

    workloads_config {
      scheduler {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        count      = 1
      }
      web_server {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
      }
      worker {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        min_count  = 1
        max_count  = 3
      }


    }
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    node_config {
      network               = var.network.id
      subnetwork            = var.subnetwork.id
      service_account       = var.sa.name
    }

    private_environment_config {
        enable_private_endpoint = false
    }
  }
}

