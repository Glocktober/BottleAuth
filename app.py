from bottle import Bottle, request
from BotAuth import BotAuth
from BottleSaml import SamlSP
from config import saml_config, session_config
from BottleSessions import BottleSessions

app = Bottle()
BottleSessions(app, **session_config)
saml = SamlSP(app, saml_config=saml_config)
pathlist = {
    '/sysadmin/': {'groups': ['sysadmin', 'sql']}
}
auth = BotAuth(saml, authn_all_routes=True, authz_by_prefix=pathlist)
app.install(auth)

@app.route('/', skip=[auth])
def index():
    return 'Hello World!'


@app.route('/login', authn=True)
def login():
    return f'Hello {request.session["username"]}'


@app.route('/.sess', authn=False)
def sess():
    return request.session


@app.route('/x', authz={'username': 'r.r.kras-stu'})
@app.route('/sysadmin/x')
@app.route('/sysadmin/xyz')
@app.route('/sql/x')
@app.route('/sql/xyz')
def xx():
    return 'in'

if __name__ == '__main__':
    app.run(port=8001, debug=True, reloader=True)
