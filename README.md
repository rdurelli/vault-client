
# Vault client para criar path, groups e members

Para testar localmente esse repo, deve seguir os seguintes passso:



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`VAULT_URL`=https://vault-brazil-cluster1-dev.nees.ufal.br/

`VAULT_TOKEN`=hvs.CAESI


## Run Locally

Clone the project

```bash
  git clone https://github.com/rdurelli/vault-client.git
```

Go to the project directory

```bash
  cd my-project
```

Install it using docker

```bash
  cd vaultclient
  docker build -t imagename .
```

Run the image

```bash
  docker container run --publish 80:80 --name vaultclient imagename
```


## Usage/Examples

```javascript
### Send POST request with json body
POST http://127.0.0.1:80/v1/api/vault/create_or_update/
Content-Type: application/json

{
    "policy_name": "teste",
    "group_name": "ead-backend",
    "secret_path": "durelli/cli2",
    "member_entity_ids" : [
        "b0729698-447f-f786-4f1c-684d438de3c2",
        "4ebf7934-55b9-03d9-2810-cccb5d158291"
    ]
}
```


## Authors

- [@rdurelli](https://www.github.com/rdurelli)

