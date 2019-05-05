if (-NOT (Test-Path ".\data\accounts.csv")) {
    copy ".\bin\sources\accounts.csv" ".\data\accounts.csv"
}

if (-NOT (Test-Path ".\data\config.json")) {
    copy ".\bin\sources\config.json" ".\data\config.json"
}
