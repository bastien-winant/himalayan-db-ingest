import json
import logging

def lambda_handler(event, context):
	print("value1 = " + event['key1'])
	print("value1 = " + event['key2'])
	print("value1 = " + event['key3'])

	return {
		"statusCode": 200,
		"body": json.dumps({'message': event['key1']})
	}