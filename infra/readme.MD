## Create infrastructure

Replace <project_id> placeholder by your project id
```
./create_state_bucket.sh <project_id>
terraform init
terraform plan
terraform apply -auto-approve
```