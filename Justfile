# Start Chatbot
start-bot:
    @echo "Starting Chatbot"
    docker compose -f compose.yaml --profile core up -d
    @echo "Chatbot started"

# Stop bot
stop-bot:
    @echo "Stopping entire stack"
    @docker compose --profile core down

# Stop Containers, Delete Images and Volumes
clean:
    @echo "Deleting all project images and volumes"
    @docker compose --profile core down --rmi all --volumes

# Follow logs for a specific service
follow-logs bot:
    docker logs -f grievance-filing-system-bot-1; \
