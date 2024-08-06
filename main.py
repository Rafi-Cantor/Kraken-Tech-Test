import requests
import os
from dotenv import load_dotenv
import pendulum

load_dotenv()

API_BASE_URL = 'https://api.krakenflex.systems/interview-tests-mock-api/v1'

API_KEY = os.environ["API_KEY"]

HEADERS = {
    'x-api-key': API_KEY
}
OUTAGES_BEFORE = "2022-01-01T00:00:00.000Z"


def get_outages():
    url = f"{API_BASE_URL}/outages"
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError(f"Unexpected return from get outages: {str(response)}.")
    return response.json()


def get_site_info(site_id: str):
    url = f"{API_BASE_URL}/site-info/{site_id}"
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError(f"Unexpected return from get site info: {str(response)}.")
    return response.json()


def post_site_outages(site_id: str, outages: list):
    url = f"{API_BASE_URL}/site-outages/{site_id}"
    response = requests.post(url=url, headers=HEADERS, json=outages)
    if response.status_code != 200:
        raise ValueError(f"Unexpected return from post site outages: {str(response)}.")
    return response.status_code


def filtered_outages(outages, site_info):
    site_device_ids = {device['id']: device['name'] for device in site_info['devices']}
    filtered_outages = []
    for outage in outages:
        if outage['id'] in site_device_ids:
            begin_date = pendulum.parse(outage['begin'])
            if begin_date >= pendulum.parse(OUTAGES_BEFORE):
                outage['name'] = site_device_ids[outage['id']]
                filtered_outages.append(outage)
    return filtered_outages


if __name__ == "__main__":
    site_id = "norwich-pear-tree"
    outages = get_outages()
    site_info = get_site_info(site_id=site_id)
    filtered_outages = filtered_outages(outages=outages, site_info=site_info)
    post_site_outages(site_id=site_id, outages=filtered_outages)
    print("The program ran successfully!")
