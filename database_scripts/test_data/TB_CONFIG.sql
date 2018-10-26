
	
INSERT INTO public."TB_CONFIG"(
            "CFGPRM_ID", "CFGPRM_KEY", "CFGPRM_VAL", "CFGPRM_DE")
    VALUES (1, 'app.release_number', '0.1', 'Application Release Number');
	
INSERT INTO public."TB_CONFIG"(
            "CFGPRM_ID", "CFGPRM_KEY", "CFGPRM_VAL", "CFGPRM_DE")
    VALUES (2, 'app.mode', 'dev', 'Application Mode: dev, test, or prod');	

-- oauth2_secret_key
INSERT INTO "TB_CONFIG"(
            "CFGPRM_KEY", "CFGPRM_VAL", "CFGPRM_DE")
    VALUES (3, "oauth2_secret_key", "LjPVqqG1rjpis1QvmcHCygSulSGPmYUZM4uCCLiA", "Oauth2 Secret Key");

	