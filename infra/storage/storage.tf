variable "project_id" {}
variable "region" {}

resource "google_storage_bucket" "pim-import" {
  name          = "pim-import-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "pim-import-completed" {
  name          = "pim-import-completed-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "supplier-catalogs-import" {
  name          = "supplier-catalogs-import-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "supplier-catalogs-in-progress" {
  name          = "supplier-catalogs-in-progress-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "supplier-catalogs-completed" {
  name          = "supplier-catalogs-completed-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "supplier-catalogs-error" {
  name          = "supplier-catalogs-error-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "supplier-product-images" {
  name          = "supplier-product-images-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "supplier-product-manual" {
  name          = "supplier-product-manual-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "supplier-column-mapping" {
  name          = "supplier-column-mapping-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "translation-glossary" {
  name          = "translation-glossary-${var.project_id}"
  location      = var.region
  project       = var.project_id
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "fasttract" {
  dataset_id                  = "fasttract"
  project = var.project_id
  location = var.region
}

resource "google_bigquery_table" "pim-extract" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.fasttract.dataset_id
  table_id   = "pim-extract"
  schema     = <<EOF
[{
		"name": "PIMKey",
		"type": "STRING",
		"mode": "REQUIRED"
	},
	{
		"name": "CorporateItemNumber",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "GlobalTradeItemNumberGTIN",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "UniversalProductCodeUPC",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "InternalItemNum",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "ManufacturerProductNumber",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "ManufacturerProductNumberWO",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "MultiVendorApproved",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "VendorNumber",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "VendorName",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "ItemHazardousMaterial",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "AllpriserCode",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "ItemType",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "CorporateDescEN",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "CorporateDescFR",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "OriginalBankDescEN",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "OriginalBankDescFR",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "AttribStructID",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "AttribStructDescEN",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "AttribStructDescFR",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "WebDescEN",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "WebDescFR",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "CreatedDate",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "LastUpdateDate",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "ReportRunDate",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "fileName",
		"type": "STRING",
		"mode": "NULLABLE"
	},
	{
		"name": "importDate",
		"type": "DATETIME",
		"mode": "NULLABLE"
	}
]
EOF

}

resource "google_bigquery_table" "suppliers_catalogs_raw" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.fasttract.dataset_id
  table_id   = "suppliers-catalogs-raw"
  schema     = <<EOF
[
    {
        "name": "SupplierFileName",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "ManufacturerProductNumber",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "VendorNumber",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "VendorName",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "Brand",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "ProductType",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "DescriptionEnglish",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "DescriptionFrench",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "ModelNumber",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "Collection",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "Finish",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "WeightLB",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "WeightKg",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "UniversalProductCodeUPC",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "Image",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "SpecsEN",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "SpecsFR",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "creationDate",
        "type": "DATETIME",
        "mode": "REQUIRED"
    }
]
EOF
}

resource "google_bigquery_table" "suppliers_catalogs" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.fasttract.dataset_id
  table_id   = "suppliers-catalogs"
  view {
        query = <<EOF
            select array_agg(t order by creationDate desc limit 1)[offset(0)].*
            from `${var.project_id}.fasttract.suppliers-catalogs-raw` t
            group by t.ManufacturerProductNumber
        EOF
        use_legacy_sql = false
  }
}