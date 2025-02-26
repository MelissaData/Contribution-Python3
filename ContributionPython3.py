
import json
import requests
import argparse
import urllib.parse

def main():
  base_service_url = "https://contribution.melissadata.net/"
  service_endpoint = "/V4/WEB/changeGeoPoint"; 

  # Create an ArgumentParser object
  parser = argparse.ArgumentParser(description='Contribution command line arguments parser')

  # Define the command line arguments
  parser.add_argument('--license', '-l', type=str, help='License key')
  parser.add_argument('--lat', type=str, help='Latitude')
  parser.add_argument('--long', type=str, help='Longitude')
  parser.add_argument('--mak', type=str, help='MAK number')
  parser.add_argument('--reason', type=str, help='Reason')
  parser.add_argument('--respondTo', type=str, help='Respond To')

  # Parse the command line arguments
  args = parser.parse_args()

  # Access the values of the command line arguments
  license = args.license
  latitude = args.lat
  longitude = args.long
  mak = args.mak
  reason = args.reason
  respondTo = args.respondTo

  call_api(base_service_url, service_endpoint, license, latitude, longitude, mak, reason, respondTo)

def get_contents(base_service_url, request_query):
    url = urllib.parse.urljoin(base_service_url, request_query)
    response = requests.get(url)
    obj = json.loads(response.text)
    pretty_response = json.dumps(obj, indent=4)

    print("\n==================================== OUTPUT ====================================\n")

    print("API Call: ")
    for i in range(0, len(url), 70):
        if i + 70 < len(url):
            print(url[i:i+70])
        else:
            print(url[i:len(url)])
    print("\nAPI Response:")
    print(pretty_response)

def call_api(base_service_url, service_endpoint, license, latitude, longitude, mak, reason, respondTo):
    print("\n=================== WELCOME TO MELISSA CONTRIBUTION CLOUD API ==================\n")

    should_continue_running = True
    while should_continue_running:
        input_latitude = ""
        input_longitude = ""
        input_mak = ""
        input_reason = ""
        input_respondTo = ""
        if not latitude and not longitude and not mak and not reason and not respondTo:
            print("\nFill in each value to see results")
            input_latitude = input("Latitude: ")
            input_longitude = input("Longitude: ")
            input_mak = input("MAK Number: ")
            input_reason = input("Reason: ")
            input_respondTo = input("Respond To: ")
        else:
            input_latitude = latitude
            input_longitude = longitude
            input_mak = mak
            input_reason = reason
            input_respondTo = respondTo

        while not input_latitude or not input_longitude or not input_mak:
            print("\nFill in each value to see results")
            if not input_latitude:
                input_latitude = input("\nLatitude: ")
            if not input_longitude:
                input_longitude = input("\nLongitude: ")
            if not input_mak:
                input_mak = input("\nMAK Number: ")
            if not input_reason:
                input_reason = input("\nReason: ")
            if not input_respondTo:
                input_respondTo = input("\nRespond To: ")

        inputs = {
            "format": "json",
            "lat": input_latitude,
            "long": input_longitude,
            "mak": input_mak,
            "reason": input_reason,
            "respondTo": input_respondTo
        }

        print("\n===================================== INPUTS ===================================\n")
        print(f"\t   Base Service Url: {base_service_url}")
        print(f"\t  Service End Point: {service_endpoint}")
        print(f"\t           Latitude: {input_latitude}")
        print(f"\t          Longitude: {input_longitude}")
        print(f"\t                MAK: {input_mak}")
        print(f"\t             Reason: {input_reason}")
        print(f"\t         Respond To: {input_respondTo}")

       # Create Service Call
        # Set the License String in the Request
        rest_request = f"&id={urllib.parse.quote_plus(license)}"

        # Set the Input Parameters
        for k, v in inputs.items():
            rest_request += f"&{k}={urllib.parse.quote_plus(v)}"

        # Build the final REST String Query
        rest_request = service_endpoint + f"?{rest_request}"

        # Submit to the Web Service.
        success = False
        retry_counter = 0

        while not success and retry_counter < 5:
            try: #retry just in case of network failure
                get_contents(base_service_url, rest_request)
                print()
                success = True
            except Exception as ex:
                retry_counter += 1
                print(ex)
                return

        is_valid = False

        if (latitude is not None) and (longitude is not None) and (mak is not None) and (reason is not None) and (respondTo is not None):
            concat = str(latitude) + str(longitude) + str(mak) + str(reason) + str(respondTo)
        else:
            concat = None

        if concat is not None and concat != "":
            is_valid = True
            should_continue_running = False

        while not is_valid:
            test_another_response = input("\nAdd another record? (Y/N)")
            if test_another_response != '':
                test_another_response = test_another_response.lower()
                if test_another_response == 'y':
                    is_valid = True
                elif test_another_response == 'n':
                    is_valid = True
                    should_continue_running = False
                else:
                    print("Invalid Response, please respond 'Y' or 'N'")

    print("\n===================== THANK YOU FOR USING MELISSA CLOUD API ====================\n")

main()
