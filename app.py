from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db.init_app(app)


class Notes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }

# with app.app_context():
#     db.create_all()


@app.route('/notes', methods=['GET'])
def get_notes():
    notes = db.session.execute(db.select(Notes)).scalars()
    data = [note.to_dict() for note in notes]
    return jsonify(data), 200


@app.route('/notes/<int:id>', methods=['GET'])
def get_note_by_id(id):
    note = db.session.execute(db.select(Notes).where(Notes.id == id)).scalar()
    if not note:
        return jsonify({'error': 'Note not found.'}), 404

    return jsonify(note.to_dict()), 200


@app.route('/notes', methods=['POST'])
def create_notes():
    data = request.get_json()
    # print(data)
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'Error': 'Invalid data'}), 404

    new_note = Notes(
        title=data['title'],
        content=data['content']
    )
    db.session.add(new_note)
    db.session.commit()

    return jsonify(new_note.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True)
