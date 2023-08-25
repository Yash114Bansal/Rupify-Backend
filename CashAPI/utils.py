import requests

otp_api_key = "5bf09b65-4327-11ee-addf-0200cd936042"
def SendOTP(otp,mobile_number):
    r = requests.get(f"https://2factor.in/API/V1/{otp_api_key}/SMS/{mobile_number}/{otp}/RupifyOTP")