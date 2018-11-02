from flask import Blueprint, request, session
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from authlib.flask.oauth2 import current_token
from authlib.specs.rfc6749 import OAuth2Error

from project.app.models.user import User
from project.app.models.oauth2 import OAuth2Client
from project.app.services import userService, oauth2Service
from project.app.services.utils import userUtils
from project.app.web.utils import debugUtils
from project.app.web.oauth2 import authorizationServer, require_oauth, scopes

bp = Blueprint(__name__, 'home')

# curl -v -u user:password localhost:9000

#  User Id is stored in the Flask Session
def currentUser():
    if 'id' in session:
        userId = session['id']
        print("id=" + str(userId))
        user = userService.getUserById(userId)
        print("user=" + str(user))
        return user
    return None


@bp.route('/', methods=['GET'])
def home():
    user = currentUser()
    if user:
        #clients = oauth2Service.getOAuth2Clients(user.id)
        clients = []
        print("clients=" + str(clients))
    else:
        clients = []
    return render_template('home.html', user=user, clients=clients)

@bp.route('/login', methods=['GET'])
def login():

    user = currentUser()
    if user:
        return redirect('/')
    else:
        #grant = authorizationServer.validate_consent_request()
        #print("grant=" + str(grant))
        return render_template('login.html')

# POST /token HTTP/1.1
# Host: server.example.com
# Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
# Content-Type: application/x-www-form-urlencoded

# grant_type=password&username=johndoe&password=A3ddj3w
@bp.route('/login', methods=['POST'])
def loginPost():

    print("loginPost called")

    username = request.form.get('username')
    password = request.form.get('password')

    if username is None or len(username.strip()) == 0:
         return redirect('/login?error=NoUserName')

    if password is None or len(password.strip()) == 0:
         return redirect('/login?error=NoPassword')   

    try:
        print("request:" + str(type(request)))

        return authorizationServer.create_authorization_response(request=request)
    except OAuth2Error as error:
        return error.error

    # userData = userService.getUserByLoginAndValidate(username, password)

    # print("userData=" + str(userData))

    # user = userData['user']
    # isPasswordValid = userData['isPasswordValid']

    # if user and isPasswordValid:
    #     session['id'] = user.id

    #     #return redirect('/oauth/authorize?response_type=code&client_id=MyApp')

    #     try:
    #         return authorizationServer.create_authorization_response(request=request, grant_user=user)
    #     except OAuth2Error as error:
    #         return error.error

    # else:
    #     return redirect('/login?error=NoUserPasswordFound')

# GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz
# &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb HTTP/1.1
# Host: server.example.com
#http://127.0.0.1:5000/oauth/authorize?response_type=code&client_id=wmahDfsran1jk6CaH1knpi3n
@bp.route('/oauth/authorize', methods=['GET'])
def authorize():

    user = currentUser()

    if user:
        try:
            print("validate_consent_request...")
            print("request.form=" + str(request.form))
            grant = authorizationServer.validate_consent_request(end_user=user)
            print("grant=" + str(grant))
        except OAuth2Error as error:
            return error.error

    else:
        return redirect('/login')        



@bp.route('/oauth/logout')
def logout():
    del session['id']
    return redirect('/')

# POST /token HTTP/1.1
# Host: server.example.com
# Content-Type: application/x-www-form-urlencoded

# grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
# &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb
# &client_id=s6BhdRkqt3

# POST /token HTTP/1.1
# Host: server.example.com
# Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
# Content-Type: application/x-www-form-urlencoded

# grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
# &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb

# POST /token HTTP/1.1
# Host: server.example.com
# Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
# Content-Type: application/x-www-form-urlencoded

# grant_type=password&username=johndoe&password=A3ddj3w
@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    print("issue_token called...")
    debugUtils.debugRequest(request)
    response = authorizationServer.create_token_response()
    debugUtils.debugResponse(response)
    return response


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorizationServer.create_endpoint_response('revocation')

@bp.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = userService.addUser(username, password)
        if user:
            session['id'] = user.id
            return redirect('/')
        else:
            render_template('signup.html')


@bp.route('/oauth/authorize3', methods=['GET', 'POST'])
def authorize3():
    user = currentUser()
    if request.method == 'GET':
        try:
            grant = authorizationServer.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)

    # r = requests.get('<MY_URI>', headers={'Authorization': 'TOK:<MY_TOKEN>'})
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorizationServer.create_authorization_response(grant_user=grant_user)

def current_user2():
    user = userService.getUserByLogin("foo")
    return user




@bp.route('/api/me', methods=['GET'])
@require_oauth('profile')
def api_me():
    print("current_token=" + str(current_token))
    #user = current_token.user
    user = userService.getUserById(current_token.user_id)
    return jsonify(id=user.id, username=user.login)

@bp.route('/api/nome', methods=['GET'])
@require_oauth('notta')
def api_nome():
    print("current_token=" + str(current_token))
    #user = current_token.user
    user = userService.getUserById(current_token.user_id)
    return jsonify(id=user.id, username=user.login)




#@bp.route('/authorize', methods=['GET', 'POST'])
#def authorize2():
    #if current_user:
    #    #form = ConfirmForm()
    #else:
    #    #form = LoginConfirmForm()

    #if form.validate_on_submit():
    #    if form.confirm.data:
    #        # granted by current user
    #        grant_user = current_user
    #    else:
    #        grant_user = None
    #    return authorization.create_authorization_response(grant_user)
    #try:
     #   grant = authorization.validate_authorization_request()
    #except OAuth2Error as error:
     #   # TODO: add an error page
     #   payload = dict(error.get_body())
     #   return jsonify(payload), error.status_code

        #resp = make_response(render_template('error.html'), 200)
        #resp.headers['X-Something'] = 'A value'

    #client = OAuth2Client.get_by_client_id(request.args['client_id'])
    #return render_template(
    #    'authorize.html',
    #    grant=grant,
    #    scopes=scopes,
    #    client=client
    #)


@bp.route('/token', methods=['POST'])
def issue_token3():
    return authorizationServer.create_token_response()


#@bp.route('/revoke', methods=['POST'])
#def revoke_token2():
 #   return authorization.create_revocation_response()
