# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request
from google.appengine.api import mail
from google.appengine.api import wrap_wsgi_app

app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)


@app.route('/send_invalid_mail', methods=['GET'])
def send_invalid_mail():
    mail.send_mail(
        sender='test-python-user@shreejad-knative-dev.appspotmail.com',
        to='Invalid Address <random-bounce@gmail.com>',
        subject='Test Email Subject sd',
        body='Test Email Body sd')

    print('Successfully sent a mail to random-bounce@gmail.com.')
    print('This should trigger a bounce notification.')

    return 'Success'


@app.route('/_ah/bounce', methods=['POST'])
def receive_bounce():
    bounce_message = mail.BounceNotification(dict(request.form.lists()))

    # Do something with the message
    print('Bounce original: ', bounce_message.original)
    print('Bounce notification: ', bounce_message.notification)

    return 'Success'


@app.route('/_ah/mail/<path>', methods=['POST'])
def receive_mail(path):
    mail_message = mail.InboundEmailMessage(request.get_data())

    # Do something with the message
    print(
        'Received greeting at %s from %s: %s' %
        (mail_message.to, mail_message.sender, mail_message.bodies('text/plain')))

    return 'Success'