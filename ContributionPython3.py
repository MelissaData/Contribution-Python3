"""
Contribution lets you submit a correction to Melissa's data. This sample calls the
changeGeoPoint endpoint to propose a new latitude/longitude for an address identified
by its Melissa Address Key (MAK), along with a reason and a contact to respond to.

High-level flow of this sample:
  1. ARGS    - main reads any --flag values off the command line with argparse.
  2. INPUT   - call_api fills in whatever wasn't supplied via interactive prompts.
  3. REQUEST - call_api builds the REST query string (license + input fields).
  4. CALL    - get_contents issues the GET request and pretty-prints the JSON response.

This sample is a thin HTTP client: it builds a query string, sends a GET request to
the Contribution Cloud API, and prints the JSON response.

Reference:
  - Documentation: https://docs.melissa.com/cloud-api/contribution/contribution-index.html
  - Release notes: https://releasenotes.melissa.com/cloud-api/contribution/
  - Result codes:  https://docs.melissa.com/melissa/result-codes/result-codes-index.html
"""

import json
import requests
import argparse
import urllib.parse

def main():
  """
  Entry point. Reads the optional command-line arguments, then hands control to
  call_api, which performs the actual request/response cycle.

  Recognized flags (each followed by its value, e.g. --mak "8008006245"):
  --license/-l, --lat, --long, --mak, --reason, --respondTo.
  Any flag not supplied is None, and call_api prompts for it interactively.
  """
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

  # Run the contribution with whatever values were passed on the command line.
  call_api(base_service_url, service_endpoint, license, latitude, longitude, mak, reason, respondTo)

def get_contents(base_service_url, request_query):
    """
    Issues the GET request against the Contribution endpoint and pretty-prints
    the API call and the JSON response to the console.

    Args:
        base_service_url: The Contribution Cloud API base URL.
        request_query: The endpoint path plus query string built by call_api.
    """
    url = urllib.parse.urljoin(base_service_url, request_query)
    response = requests.get(url)

    # Re-serialize with indentation so the raw response is easier to read.
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
    """
    Drives the interactive/CLI loop: gathers the contribution fields, builds and
    submits the REST query, prints the result, and optionally repeats for another record.

    It runs a single pass and exits only when all five fields (latitude, longitude, MAK,
    reason and respond-to) were supplied on the command line. Otherwise it loops, asking
    for a new record each pass until the user answers "N".

    Args:
        base_service_url: The Contribution Cloud API base URL.
        service_endpoint: The specific Contribution endpoint path to call.
        license: The Melissa license string sent with every request.
        latitude: The proposed latitude, or None to prompt for it.
        longitude: The proposed longitude, or None to prompt for it.
        mak: The Melissa Address Key of the address to correct, or None to prompt for it.
        reason: The reason for the change, or None to prompt for it.
        respondTo: A contact (e.g. an email address) to respond to, or None to prompt for it.
    """
    print("\n=================== WELCOME TO MELISSA CONTRIBUTION CLOUD API ==================\n")

    should_continue_running = True
    while should_continue_running:
        input_latitude = ""
        input_longitude = ""
        input_mak = ""
        input_reason = ""
        input_respondTo = ""
        # No values were supplied via command line, so prompt for every field.
        if not latitude and not longitude and not mak and not reason and not respondTo:
            print("\nFill in each value to see results")
            input_latitude = input("Latitude: ")
            input_longitude = input("Longitude: ")
            input_mak = input("MAK Number: ")
            input_reason = input("Reason: ")
            input_respondTo = input("Respond To: ")
        else:
            # At least one field was supplied via command line; use those values as-is.
            input_latitude = latitude
            input_longitude = longitude
            input_mak = mak
            # Reason and respond-to are optional here, so an omitted flag (None) becomes "".
            input_reason = reason or ""
            input_respondTo = respondTo or ""

        # Prompt for missing fields until latitude, longitude and MAK are all filled in.
        # Only those three are required to leave this loop; a missing reason or
        # respond-to is asked for on each pass but may be left blank.
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

        # Map input fields to the API's expected query parameter names and
        # request a JSON response.
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

        # If all five fields came from the command line, treat this as a one-shot
        # run rather than looping for additional records.
        if (latitude is not None) and (longitude is not None) and (mak is not None) and (reason is not None) and (respondTo is not None):
            concat = str(latitude) + str(longitude) + str(mak) + str(reason) + str(respondTo)
        else:
            concat = None

        if concat is not None and concat != "":
            is_valid = True
            should_continue_running = False

        # Otherwise ask whether to add another record. Keep prompting until we get a
        # valid Y/N. "N" ends the program; "Y" falls through to another pass.
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
