import requests
from bs4 import BeautifulSoup
import pytest

def test_page_load(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")
    assert response.status_code == 200, f"Page {url} did not load successfully"

def test_conqt_pages_load():
    urls = [
        "https://www.conqt.com/",
        "https://www.conqt.com/view-all-product",
        "https://www.conqt.com/AWS-Cloud-Storage",
        "https://www.conqt.com/faqs",
        "https://www.conqt.com/conqt-university"
    ]
    for url in urls:
        test_page_load(url)

def test_api_endpoint(url, expected_status=200):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API request to {url} failed: {e}")
    assert response.status_code == expected_status, f"API {url} returned {response.status_code}"

def test_all_api_endpoints():
    api_urls = [
        "https://www.conqt.com/api/products",
        "https://www.conqt.com/api/aws-cloud-storage",
        "https://www.conqt.com/api/faqs",
        "https://www.conqt.com/api/conqt-university"
    ]
    for url in api_urls:
        test_api_endpoint(url)

def test_data_consistency(page_url, api_url):
    try:
        page_response = requests.get(page_url)
        page_response.raise_for_status()
        api_response = requests.get(api_url)
        api_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {page_url} or {api_url} failed: {e}")

    page_content = page_response.content
    api_data = api_response.json()

    soup = BeautifulSoup(page_content, 'html.parser')

    # Example validation for product names
    page_product_names = [element.text for element in soup.select('.product-name')]
    api_product_names = [product['name'] for product in api_data]

    assert page_product_names == api_product_names, "Data mismatch between page and API"

def test_conqt_data_consistency():
    tests = [
        ("https://www.conqt.com/view-all-product", "https://www.conqt.com/api/products"),
        ("https://www.conqt.com/AWS-Cloud-Storage", "https://www.conqt.com/api/aws-cloud-storage"),
        ("https://www.conqt.com/faqs", "https://www.conqt.com/api/faqs"),
        ("https://www.conqt.com/conqt-university", "https://www.conqt.com/api/conqt-university")
    ]
    for page_url, api_url in tests:
        test_data_consistency(page_url, api_url)

def test_contrast_ratio(html_content):
    # Implement the contrast ratio check logic here
    pass

def test_conqt_contrast_ratios():
    urls = [
        "https://www.conqt.com/",
        "https://www.conqt.com/view-all-product",
        "https://www.conqt.com/AWS-Cloud-Storage",
        "https://www.conqt.com/faqs",
        "https://www.conqt.com/conqt-university"
    ]
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request to {url} failed: {e}")
        test_contrast_ratio(response.content)

def test_discernible_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        assert link.text.strip(), f"Link with href {link.get('href')} does not have a discernible name"

def test_conqt_discernible_links():
    urls = [
        "https://www.conqt.com/",
        "https://www.conqt.com/view-all-product",
        "https://www.conqt.com/AWS-Cloud-Storage",
        "https://www.conqt.com/faqs",
        "https://www.conqt.com/conqt-university"
    ]
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request to {url} failed: {e}")
        test_discernible_links(response.content)

@pytest.mark.parametrize("url", [
    "https://www.conqt.com/",
    "https://www.conqt.com/view-all-product",
    "https://www.conqt.com/AWS-Cloud-Storage",
    "https://www.conqt.com/faqs",
    "https://www.conqt.com/conqt-university"
])
def test_pages(url):
    test_page_load(url)

@pytest.mark.parametrize("api_url", [
    "https://www.conqt.com/api/products",
    "https://www.conqt.com/api/aws-cloud-storage",
    "https://www.conqt.com/api/faqs",
    "https://www.conqt.com/api/conqt-university"
])
def test_apis(api_url):
    test_api_endpoint(api_url)

@pytest.mark.parametrize("page_url, api_url", [
    ("https://www.conqt.com/view-all-product", "https://www.conqt.com/api/products"),
    ("https://www.conqt.com/AWS-Cloud-Storage", "https://www.conqt.com/api/aws-cloud-storage"),
    ("https://www.conqt.com/faqs", "https://www.conqt.com/api/faqs"),
    ("https://www.conqt.com/conqt-university", "https://www.conqt.com/api/conqt-university")
])
def test_data_consistency_pages(page_url, api_url):
    test_data_consistency(page_url, api_url)

@pytest.mark.parametrize("url", [
    "https://www.conqt.com/",
    "https://www.conqt.com/view-all-product",
    "https://www.conqt.com/AWS-Cloud-Storage",
    "https://www.conqt.com/faqs",
    "https://www.conqt.com/conqt-university"
])
def test_contrast(url):
    response = requests.get(url)
    assert response.status_code == 200
    test_contrast_ratio(response.content)

@pytest.mark.parametrize("url", [
    "https://www.conqt.com/",
    "https://www.conqt.com/view-all-product",
    "https://www.conqt.com/AWS-Cloud-Storage",
    "https://www.conqt.com/faqs",
    "https://www.conqt.com/conqt-university"
])
def test_links(url):
    response = requests.get(url)
    assert response.status_code == 200
    test_discernible_links(response.content)
