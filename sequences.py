from sqlalchemy import Sequence

sequence = Sequence("sequence")
batch_sequence = Sequence("batch_sequence")
image_sequence = Sequence("image_sequence")
json_sequence = Sequence("json_sequence")


def create_sequences(engine):
    sequence.create(bind=engine)
    batch_sequence.create(bind=engine)
    json_sequence.create(bind=engine)
    image_sequence.create(bind=engine)
