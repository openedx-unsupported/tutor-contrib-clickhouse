echo "Initialising Clickhouse..."
ch_connection_max_attempts=10
ch_connection_attempt=0
until clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" --port {{ CLICKHOUSE_PORT }} -q 'exit'
do
    ch_connection_attempt=$(expr $ch_connection_attempt + 1)
    echo "    [$ch_connection_attempt/$ch_connection_max_attempts] Waiting for Clickhouse service (this may take a while)..."
    if [ $ch_connection_attempt -eq $ch_connection_max_attempts ]
    then
      echo "Clickhouse initialisation error" 1>&2
      exit 1
    fi
    sleep 10
done
echo "Clickhouse is up and running"

# Create the xapi database if it doesn't exist
clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" --port {{ CLICKHOUSE_PORT }} -q "CREATE DATABASE IF NOT EXISTS {{ CLICKHOUSE_XAPI_DATABASE }};"

# Create the LRS and reporting users
clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" --port {{ CLICKHOUSE_PORT }} -q "CREATE USER IF NOT EXISTS {{ CLICKHOUSE_LRS_USER}} IDENTIFIED WITH sha256_password BY '{{ CLICKHOUSE_LRS_PASSWORD }}';"
clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" --port {{ CLICKHOUSE_PORT }} -q "CREATE USER IF NOT EXISTS {{ CLICKHOUSE_REPORT_USER}} IDENTIFIED WITH sha256_password BY '{{ CLICKHOUSE_REPORT_PASSWORD }}';"

# Grant basic permissions to the users
clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" --port {{ CLICKHOUSE_PORT }} -q "GRANT ALL ON {{ CLICKHOUSE_XAPI_DATABASE }}.* TO '{{ CLICKHOUSE_LRS_USER }}';"
clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" --port {{ CLICKHOUSE_PORT }} -q "GRANT SELECT ON {{ CLICKHOUSE_XAPI_DATABASE }}.* TO '{{ CLICKHOUSE_REPORT_USER }}';"
