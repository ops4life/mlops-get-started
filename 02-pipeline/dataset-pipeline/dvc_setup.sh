# Initialize DVC in your ML project repo
git init ml-project
cd ml-project
dvc init
git add .dvc
git commit -m "chore: initialize DVC"

# Configure MinIO as remote storage (S3-compatible)
dvc remote add -d myremote s3://dvc/cache
dvc remote modify myremote endpointurl https://s3.ops4life.com
git add .dvc/config
git commit -m "chore: configure DVC MinIO remote"

# Track a dataset directory
dvc add data/raw/events/
git add data/raw/events.dvc .gitignore
git commit -m "data: add raw events dataset v1"
dvc push

# After pipeline runs and data updates:
dvc add data/raw/events/   # Updates the .dvc metadata
git add data/raw/events.dvc
git commit -m "data: update raw events dataset 2024-01-15"
dvc push

# To reproduce a past experiment with exact dataset:
git checkout <commit-hash>
dvc pull   # Downloads the exact dataset version from that commit
