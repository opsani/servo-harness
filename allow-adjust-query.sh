#!/bin/sh

APPLICATION=$1
URL=$2
RESULTS=`curl -sS -H 'Content-type: application/json' -H 'Accept: application/json' -X POST -k ${URL}/${APPLICATION} -d '{"deployType": "Harness","desc": "opsani-servo blackout window check", "noOfHours": 1}'`
APPROVED=`echo $RESULTS | jq .approved`
MESSAGE=`echo $RESULTS | jq .message`

if [ "$APPROVED" == '"true"' ]; then
  echo $MESSAGE
  exit 0
else
  echo $MESSAGE
  exit 1
fi
