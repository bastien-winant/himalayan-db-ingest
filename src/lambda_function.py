import json
import logging

logger = logging.getLogger()

def lambda_handler(event, context):
	print("value1 = " + event['key1'])
	print("value1 = " + event['key2'])
	print("value1 = " + event['key3'])

	logger.info("Inside the handler function")

	return {
		"statusCode": 200,
		"body": json.dumps({'message': event['key1']})
	}