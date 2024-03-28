import uuid


#function to generate unique id
def generate_unique_id() -> str:
    return str(uuid.uuid4()).replace("-", "")
