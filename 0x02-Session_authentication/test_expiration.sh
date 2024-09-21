#!/bin/bash

session_id=$( curl -XPOST  "localhost:5000/api/v1/auth_session/login" -d "email=alien@hbtn.io" -d "password=123" -vvv 2>&1 | grep "Set-Cookie" | cut -d= -f2 | cut -d';' -f1) 
echo $session_id

# curl -XGET -s -w "%{http_code}\n" "localhost:5000/api/v1/users/me" --cookie "_my_session_id=$session_id" 
Counter=1
status_code=200
time while [[ "$status_code" -eq 200 ]]; do
    sleep 1
    echo "Hello $Counter"
    ((Counter++))
    echo "DB size: $(cat .db_UserSession.json | wc -c)"
    status_code=$(curl -XGET -o /dev/null -s -w "%{http_code}\n" "localhost:5000/api/v1/users/me" --cookie "_my_session_id=$session_id" )
    # curl -XGET -s -w "%{http_code}\n" "localhost:5000/api/v1/users/me" --cookie "_my_session_id=$session_id" 
done
cat .db_UserSession.json
