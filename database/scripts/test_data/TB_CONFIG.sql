
	
INSERT INTO public.TB_CONFIG(
            CFGPRM_KEY, CFGPRM_VAL, CFGPRM_DE)
    VALUES ('app.release_number', '0.1', 'Application Release Number');

INSERT INTO public.TB_CONFIG(
            CFGPRM_KEY, CFGPRM_VAL, CFGPRM_DE)
    VALUES ('app.base_url', 'http://localhost:9000', 'Server base url');

INSERT INTO public.TB_CONFIG(
            CFGPRM_KEY, CFGPRM_VAL, CFGPRM_DE)
    VALUES ('app.secret_key', 'E1pfGXPlSPNnLcyl29p7KVcLYovsJTANVrPyhkSw', 'Application Encryption key');

INSERT INTO public.TB_CONFIG(
            CFGPRM_KEY, CFGPRM_VAL, CFGPRM_DE)
    VALUES ('app.aes.secret_key', 'OucwXmUyIDJaHGeH', '16 Byte key');

INSERT INTO TB_CONFIG(
            CFGPRM_KEY, CFGPRM_VAL, CFGPRM_DE)
    VALUES ('app.smtp', 'localhost:9025', 'SMTP information,  <host>:<port>');



	