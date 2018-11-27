INSERT INTO public.TB_OAUTH2_CLIENT(
            OAUTH2CL_ID, client_id, client_secret, issued_at, expires_at,
            redirect_uri, token_endpoint_auth_method, grant_type, response_type,
            scope, client_name, client_uri)
    VALUES (1, 'CLTID-Zeq1LRso5q-iLU9RKCKnu', null, 1531271519, 0
			, 'http://127.0.0.1:4200/oauth/callback', 'none', 'password', 'code'
			, 'app.public', 'UsernamePasswordClient', 'http://127.0.0.1:4200/');