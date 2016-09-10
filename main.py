#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2

form="""
<!DOCTYPE html>
<html>
    <head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required>
                        <span class="error">%(error_username)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error">%(error_password)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error">%(error_verify)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%(email)s">
                        <span class="error">%(error_email)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>
"""

def valid_username(username):
    if (len(username)< 3) or (len(username)> 20) or username.isalpha() == False:
        return False
    else:
        return True

def valid_password(password):
    if (len(password)< 3) or (len(password)> 20):
        return False
    else:
        return True

def valid_verify(password, verify):
    if password != verify:
        return False
    else:
        return True

def valid_email(email):
    if email != "" and "@" not in email:
        return False
    else:
        return True

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", error_username="", error_password="", error_verify="", email="", error_email=""):
        self.response.out.write(form % {"username": username, "error_username": error_username, "error_password": error_password,
        "error_verify": error_verify, "email": email, "error_email": error_email})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username = username,
                        email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        if not valid_verify(password, verify):
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error == True:
            self.write_form(**params)
        else:
            self.response.write("Welcome, "+username+"!")

app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
