import json

import connexion

from APIS import start

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")


if __name__ == '__main__':
    start()
    app.run(host="0.0.0.0", port=8000, debug=True)