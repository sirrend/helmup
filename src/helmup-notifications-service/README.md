Example message + payload:

curl -X POST "helmup-notifications-service/event" -H "Content-Type: application/json" -d '{
  "message": "This is a test message"
}'