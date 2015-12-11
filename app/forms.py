from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField
from werkzeug.datastructures import MultiDict

class ContactForm(Form):
  name = TextField("Name")
  email = TextField("Email")
  subject = TextField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")

  def reset(self):
      blankData = MultiDict([])
      self.process(blankData)
