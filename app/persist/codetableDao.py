
def get_code_table(session, codetable):

    all_data = session.query(codetable).order_by(codetable.description).all()

    return all_data
