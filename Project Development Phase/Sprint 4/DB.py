from cloudant.client import Cloudant

client = Cloudant.iam(
    "1ead8cb5-ab6b-4f2e-94cf-05f5c276902f-bluemix",
    "xpf_6VVXQ9fx0ofkwxQMMdzHzT_bHWx4OYgK8D80bLrL",
    connect=True,
)
patient_db = client.create_database("users")


def insert_document(name, email, password):
    data = {"username": email, "name": name, "password": password}
    patient_db.create_document(data)


def retrieve_document():
    all_docs = patient_db.all_docs()
    print(all_docs)


def check_document(username, password):
    query_1 = {"username": {"$eq": username}}
    query_2 = {"password": {"$eq": password}}
    if (
        len(patient_db.get_query_result(query_1).all()) > 0
        and len(patient_db.get_query_result(query_2).all()) > 0
    ):
        return True
    else:
        return False
