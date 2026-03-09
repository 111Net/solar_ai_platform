#!/bin/bash

# -----------------------------
# Full integration test script
# -----------------------------

# Input files (can override)
USERS_CSV=${1:-users.csv}
PLAN_CSV=${2:-test_cases.csv}
LOG_FILE=${3:-test_results.log}
REPORT_CSV=${4:-test_report.csv}
REPORT_PDF=${5:-test_report.pdf}

> "$LOG_FILE"
> "$REPORT_CSV"

# CSV header
echo "Timestamp,User,Action,Input,Response" > "$REPORT_CSV"

# --- Activate virtual environment & start FastAPI server ---
cd ~/solar_ai_platform || { echo "Folder not found"; exit 1; }
source venv/bin/activate || { echo "Failed to activate venv"; exit 1; }

fuser -k 8000/tcp 2>/dev/null || true
python main.py &
SERVER_PID=$!
echo "FastAPI server started with PID $SERVER_PID"

# Wait for server readiness
for i in {1..10}; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health || echo "000")
    [ "$STATUS" == "200" ] && break
    sleep 1
done
if [ "$STATUS" != "200" ]; then
    echo "Server failed to start" | tee -a "$LOG_FILE"
    kill $SERVER_PID
    exit 1
fi

declare -A TOKENS

# --- User creation & login ---
tail -n +2 "$USERS_CSV" | while IFS=',' read -r EMAIL PASSWORD; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    RESPONSE=$(curl -s -X POST "http://127.0.0.1:8000/users/" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")
    echo "$TIMESTAMP,$EMAIL,Create User,\"$EMAIL\",$RESPONSE" >> "$REPORT_CSV"

    # Login via JWT
    TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$EMAIL&password=$PASSWORD" | jq -r '.access_token')
    TOKENS[$EMAIL]=$TOKEN
done

# --- Solar plan creation & listing ---
for EMAIL in "${!TOKENS[@]}"; do
    TOKEN=${TOKENS[$EMAIL]}
    tail -n +2 "$PLAN_CSV" | while IFS=',' read -r DAILY_ENERGY DAYS_AUTONOMY PANEL_EFF BATTERY_VOLT; do
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        INPUT="daily_energy_kwh=$DAILY_ENERGY,days_of_autonomy=$DAYS_AUTONOMY"
        RESPONSE=$(curl -s -X POST "http://127.0.0.1:8000/solar-plan/" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d "{
                \"daily_energy_kwh\": $DAILY_ENERGY,
                \"days_of_autonomy\": $DAYS_AUTONOMY,
                \"panel_efficiency\": $PANEL_EFF,
                \"battery_voltage\": $BATTERY_VOLT
            }")
        echo "$TIMESTAMP,$EMAIL,Create Solar Plan,\"$INPUT\",$RESPONSE" >> "$REPORT_CSV"
    done

    # List plans
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    RESPONSE=$(curl -s -X GET "http://127.0.0.1:8000/solar-plans/" \
        -H "Authorization: Bearer $TOKEN")
    echo "$TIMESTAMP,$EMAIL,List Solar Plans,,\"$RESPONSE\"" >> "$REPORT_CSV"
done

# --- Health check ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
RESPONSE=$(curl -s http://127.0.0.1:8000/health)
echo "$TIMESTAMP,ALL,Health Check,,\"$RESPONSE\"" >> "$REPORT_CSV"

# --- Stop server ---
kill $SERVER_PID
echo "$(date '+%Y-%m-%d %H:%M:%S'),ALL,Server Stop,,Server stopped" >> "$REPORT_CSV"

# --- Generate PDF report with charts ---
python generate_report.py "$REPORT_CSV" "$REPORT_PDF"
echo "PDF report generated: $REPORT_PDF"

# --- Email PDF report securely using .env ---
python email_report.py "$REPORT_PDF"
#-------------------------------------------------------------

retry_curl() {
    local url=$1
    local data=$2
    local headers=$3
    local max_attempts=3
    local attempt=1
    local response

    while [ $attempt -le $max_attempts ]; do
        response=$(curl -s -w "%{http_code}" -o /tmp/curl_response.json -X POST "$url" $headers -d "$data")
        code=$(tail -c 3 /tmp/curl_response.json)
        if [ "$code" == "200" ] || [ "$code" == "201" ]; then
            cat /tmp/curl_response.json
            return 0
        else
            echo "Attempt $attempt failed, retrying..."
            sleep 1
            attempt=$((attempt+1))
        fi
    done
    echo "Failed after $max_attempts attempts"
    return 1
}