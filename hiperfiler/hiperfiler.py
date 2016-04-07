# -*- coding: utf-8 -*-

#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

import flask


app = flask.Flask(__name__)

BASE_DIR = os.getenv('HIPERFILER_BASE_DIR') or os.path.expanduser('~')


@app.route("/files", methods=['GET'])
def get_files_list():
    files = []
    for elem in os.listdir(os.path.expanduser('~')):
        if os.path.isfile(os.path.join(BASE_DIR, elem)):
            files.append(elem)

    return flask.jsonify({"files": files})


@app.route("/files/upload", methods=['POST'])
def upload_files():
    """TO UPLOAD WITH CURL

    curl -F file=@/absolute/path/to/file.txt http://localhost:5000/files/upload
    """
    for file_ in flask.request.files.values():
        filename = file_.filename
        file_.save(os.path.join(BASE_DIR, filename))

    return "DONE"


@app.route("/files/<name>", methods=['GET'])
def download_file(name):
    return flask.send_from_directory(BASE_DIR, name)


@app.route("/files/<name>/metadata", methods=['GET'])
def get_file_metadata(name):
    path = os.path.join(BASE_DIR, name)
    data = {
        "path": path,
        "size": os.path.getsize(path),
        "mtime": os.path.getmtime(path),
        "ctime": os.path.getctime(path),
    }

    return flask.jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
