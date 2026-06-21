import requests
from minsearch import Index

def get_faqs():
    root_url = 'https://datatalks.club/faq/json/courses.json'
    base_url = 'https://datatalks.club/faq'
    faqs = []

    res = requests.get(root_url)
    for course in res.json():
        res = requests.get(f'{base_url}{course['path']}')
        faqs.extend(res.json())
    
    return faqs

def build_index(faqs):
    index = Index(
        text_fields=['section', 'question', 'answer'],
        keyword_fields=['course'],
    )
    index.fit(faqs)
    
    return index