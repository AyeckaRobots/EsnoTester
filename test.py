from api_request import change_modcod, get_status
from NoiseFinder import get_token


ip = "192.168.15.10"

token = get_token(ip)

change_modcod(token, ip, 113)

print(signal_pls_code := get_status(token, ip)['test_pattern_pls_code'])
