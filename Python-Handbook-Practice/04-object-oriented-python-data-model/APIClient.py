"""
Implement a APIClient.from_url() alternative constructor.
"""
class APIClient:

    url: str

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"APIClient: {self.url}"

    def __repr__(self):
        return f"{self.url}"

    @classmethod 
    def from_url(cls, url):
        return cls(url)

client = APIClient.from_url("http://openai.test.com/123")
print(repr(client))


