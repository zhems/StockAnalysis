import yaml

def get_api_key(): # each API key is rate limited on how many API calls can be made per minute; therefore, use rotation of keys to prevent throttling
    with open("../keys/api_keys.yaml","r") as file_object:
        api_keys = yaml.load(file_object,Loader=yaml.SafeLoader)
    api_key = api_keys[0]
    with open('../keys/api_keys.yaml', 'w') as outfile:
        yaml.dump(api_keys[1:]+api_keys[:1], outfile, default_flow_style=False)
    return api_key
def get_prev_api_key():
    with open("../keys/api_keys.yaml","r") as file_object:
        api_keys = yaml.load(file_object,Loader=yaml.SafeLoader)
    return api_keys[-1]