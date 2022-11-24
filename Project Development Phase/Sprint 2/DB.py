from cloudant.client import Cloudant

client = Cloudant.iam(
    "1ead8cb5-ab6b-4f2e-94cf-05f5c276902f-bluemix",
    "xpf_6VVXQ9fx0ofkwxQMMdzHzT_bHWx4OYgK8D80bLrL",
    connect=True,
)
db = client.create_database("users")
