#!/bin/bash

set -euo pipefail

export DATABASE_URL="postgresql://user:password@host:port/database"

start_database() {
  echo "Starting database..."
  pg_ctl start -D /var/lib/postgresql/data -l /var/log/postgresql/postgresql.log
  wait_for_service postgresql 5432
  store_pid "database"
}

start_backend() {
  echo "Starting backend..."
  uvicorn main:app --host 0.0.0.0 --port 8000
  wait_for_service backend 8000
  store_pid "backend"
}

store_pid() {
  local service_name=$1
  local pid=$(pgrep -f "$service_name")
  if [[ -n "$pid" ]]; then
    echo "$pid" > "/var/run/$service_name.pid"
  fi
}

wait_for_service() {
  local service_name=$1
  local port=$2
  local timeout=30
  local attempts=0
  until nc -z "$HOST" "$port" 2>/dev/null; do
    ((attempts++))
    if [[ $attempts -gt $timeout ]]; then
      echo "Error: Timeout waiting for $service_name on port $port"
      exit 1
    fi
    sleep 1
  done
}

cleanup() {
  echo "Stopping services and cleaning up..."
  for pid_file in /var/run/*.pid; do
    service_name=$(basename "$pid_file" .pid)
    if [[ -f "$pid_file" ]]; then
      local pid=$(cat "$pid_file")
      if [[ -n "$pid" ]]; then
        kill "$pid" 2>/dev/null
      fi
      rm "$pid_file"
    fi
  done
}

trap cleanup EXIT ERR

start_database
start_backend

echo "Application started successfully"