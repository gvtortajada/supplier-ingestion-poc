def get_pim_schema():
    return [
		{
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

def get_supplier_schema():
	return [
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

def get_fasttrack_column():
	return [
		'SupplierFileName',
		'ManufacturerProductNumber', 
		'VendorNumber',
		'VendorName',
		'Brand',
		'ProductType',
		'DescriptionEnglish',
		'DescriptionFrench',
		'ModelNumber',
		'Collection',
		'Finish',
		'WeightLB',
		'WeightKg',
		'UniversalProductCodeUPC',
		'Image',
		'SpecsEN',
		'SpecsFR'
	]