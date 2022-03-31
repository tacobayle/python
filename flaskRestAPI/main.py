from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

# pip3 install Flask
# pip3 install flask_restful

# curl 127.0.0.1:5000/helloworld
# curl -X POST 127.0.0.1:5000/helloworld

# nic@jumphp:~$
# nic@jumphp:~$ curl  127.0.0.1:5000/helloArgument/mystring/123
# {
#     "name-string": "mystring",
#     "test-int": 123
# }
# nic@jumphp:~$
# nic@jumphp:~$

# nic@jumphp:~$ curl -X PUT -H "Content-Type: application/json" -d '{"name":"nbayle"}' http://127.0.0.1:5000/deploy
# {
#     "name": "nbayle"
# }
# nic@jumphp:~$
# nic@jumphp:~$

# nic@jumphp:~$ curl -X GET -H "Content-Type: application/json" -d '{"name":"nbayle"}' http://127.0.0.1:5000/deploy
# {
#     "response": "nbayle",
#     "http_request": "get",
#     "status": " running"
# }
# nic@jumphp:~$




app = Flask(__name__)
api = Api(app)

deploy_args = reqparse.RequestParser()
deploy_args.add_argument("name", type=str, help="Name of the deployment required", required=True)

class HellowWorld(Resource):
  def get(self):
    return {'data': "Hello World"}

  def post(self):
    return {'data': "HTTP post"}

class helloArgument(Resource):
  def get(self, name, test):
    return {'name-string': name, "test-int": test}

class deployment(Resource):

  def get(self):
    args = deploy_args.parse_args()
    deployments = ['byoa_nbayle']
    status = 'running'
    full_deployment_name = 'byoa_' + args['name']
    if full_deployment_name not in deployments:
      abort(404, message='Could not find deployment called: ' + args['name'])
    return {'deployment_name': args['name'], 'status': status}, 201

  def put(self):
    args = deploy_args.parse_args()
    return {'response': args['name'], 'http_request': 'put'}, 201

  def delete(self):
    args = deploy_args.parse_args()
    deployments = ['byoa_nbayle']
    full_deployment_name = 'byoa_' + args['name']
    if full_deployment_name not in deployments:
      abort(404, message='Unable to delete deployment called: ' + args['name'] + ' deployment not found')
    return {'deployment_name': args['name'], 'status': 'deleted'}, 204

api.add_resource(HellowWorld, "/helloworld")

api.add_resource(helloArgument, "/helloArgument/<string:name>/<int:test>")

api.add_resource(deployment, "/deployment")

if __name__ == "__main__":
  app.run(debug=True)