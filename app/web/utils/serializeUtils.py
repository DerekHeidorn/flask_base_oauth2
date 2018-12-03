

def serialize_authority(authorities):
    data = []
    for a in authorities:
        data.append(a.key)
    return data
