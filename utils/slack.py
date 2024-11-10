import requests


class SlackAPI:
    def __init__(self, slack_api_token):
        self.slack_api = slack_api_token
        self.base_endpoint = 'https://slack.com/api/'
        self.channel = 'C02EYDMFCQ1'


    def send_api_call(self, endpoint, payload):
        header = {
            'Authorization': f'Bearer {self.slack_api}',
            'Content-Type': 'application/json'
        }

        request_response = requests.post(endpoint, json=payload, headers=header)
        return request_response

    # Send Message
    def send_channel_message(self, message):
        endpoint = self.base_endpoint + 'chat.postMessage'
        channel_message = {
            'channel': self.channel,
            'text': f':cin: :: {message}'
        }
        api_response = SlackAPI.send_api_call(self, endpoint, channel_message)
        
        
        if api_response.status_code == '200':
            print('Successfully sent')
            
        else:
            print(api_response.status_code,'\n')
            print(api_response.content,'\n')
            print('Error')


