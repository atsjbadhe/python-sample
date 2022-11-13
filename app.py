import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/keyvault')
def mykeyvault():
        
    #keyVaultName = os.environ["KEY_VAULT_NAME"]
    keyVaultName = "ISP-keyvault"
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    #KVUri = f"https://ddd.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    #secretName = input("Input a name for your secret > ")
    #secretValue = input("Input a value for your secret > ")
    secretName = "sample1"
    secretValue = "samplevalue"

    print(f"Creating a secret in ddd called '{secretName}' with the value '{secretValue}' ...")

    client.set_secret(secretName, secretValue)

    print(" done.")

    print(f"Retrieving your secret from ddd.")

    retrieved_secret = client.get_secret(secretName)

    print(f"Your secret is '{retrieved_secret.value}'.")
    #print(f"Deleting your secret from ddd ...")

    #poller = client.begin_delete_secret(secretName)
    #deleted_secret = poller.result()

    print(" done.")
    return ("success")

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       mykeyvault()
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()