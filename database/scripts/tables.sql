
  
  CREATE TABLE public."TB_USER_STA_CD"
(
  "USRSTA_CD" character(1) NOT NULL, -- User Status Code
  "USRSTA_DE" character varying(30) NOT NULL, -- User Status Description
  CONSTRAINT "PK_TB_USER_STA_CD" PRIMARY KEY ("USRSTA_CD")
)
WITH (
  OIDS=FALSE
);

ALTER TABLE public."TB_USER_STA_CD"
  OWNER TO postgres;
COMMENT ON COLUMN public."TB_USER_STA_CD"."USRSTA_CD" IS 'User Status Code';
COMMENT ON COLUMN public."TB_USER_STA_CD"."USRSTA_DE" IS 'User Status Description';
  
  -- ===================================================================
  
    CREATE TABLE "TB_USER_TYP_CD" 
   (	"USRTYP_CD" character varying(2) NOT NULL, 
	"USRTYP_DE" character varying(20) NOT NULL, 
	 CONSTRAINT "PKTB_USER_TYP_CD" PRIMARY KEY ("USRTYP_CD"));
	 
  ALTER TABLE public."TB_USER_TYP_CD"
  OWNER TO postgres;
  
  -- =====================================================================

-- Table: public."TB_USER"

-- DROP TABLE public."TB_USER";

CREATE TABLE public."TB_USER"
(
  "USER_ID" serial NOT NULL, -- System-generated ID for a User.
  "USER_UUID" uuid NOT NULL,
  "USERNAME" character varying(100) NOT NULL, -- Username for a User
  "USER_PASSWD" character(256), -- Hashed password used in login authentication
  "USER_PASSWD_SALT" character(32), -- Used in hashing and authentication
  "USER_PASSWD_EXP_TS" timestamp without time zone, -- A timestamp for expiring a password, used for temporary passwords
  "USRTYP_CD" character(2) NOT NULL, -- Code value for user type
  "USER_ATTEMPT_CNT" integer NOT NULL DEFAULT 0, -- Number of attempts since the last sucessful login.
  "USER_ATTEMPT_TS" timestamp without time zone, -- When the last login attempt was made.
  "USER_PRIV_KEY" character(32), -- Used for encrypting the data specific to the user.
  "USER_ACTV_CODE" character(32), -- A code that is used to Reactivate an account that got deactivated.
  "USER_RESET_CODE" character(32), -- Encrypted code passed to the user at the point of a password reset.
  "USRSTA_CD" character(1) NOT NULL, -- User Status Code
  "USER_RESET_PRSN_ID" integer, -- ID of the individual (Staff User) who performed the reset
  "USER_FNAME" character varying(50), -- First Name of the User
  "USER_LNAME" character varying(80), -- Last Name of the User
  CONSTRAINT "PKTB_USER" PRIMARY KEY ("USER_ID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."TB_USER"
  OWNER TO postgres;
COMMENT ON TABLE public."TB_USER"
  IS 'User Table - A User is an individual who logs into the system ';
COMMENT ON COLUMN public."TB_USER"."USER_ID" IS 'System-generated ID for a User.';
COMMENT ON COLUMN public."TB_USER"."USER_UUID" IS 'Unique User Id';
COMMENT ON COLUMN public."TB_USER"."USERNAME" IS 'Username for a User';
COMMENT ON COLUMN public."TB_USER"."USER_PASSWD" IS 'Hashed password used in login authentication';
COMMENT ON COLUMN public."TB_USER"."USER_PASSWD_SALT" IS 'Used in hashing and authentication';
COMMENT ON COLUMN public."TB_USER"."USER_PASSWD_EXP_TS" IS 'A timestamp for expiring a password, used for temporary passwords';
COMMENT ON COLUMN public."TB_USER"."USRTYP_CD" IS 'Code value for user type';
COMMENT ON COLUMN public."TB_USER"."USER_ATTEMPT_CNT" IS 'Number of attempts since the last sucessful login.';
COMMENT ON COLUMN public."TB_USER"."USER_ATTEMPT_TS" IS 'When the last login attempt was made.';
COMMENT ON COLUMN public."TB_USER"."USER_PRIV_KEY" IS 'Used for encrypting the data specific to the user.';
COMMENT ON COLUMN public."TB_USER"."USER_ACTV_CODE" IS 'A code that is used to Reactivate an account that got deactivated.';
COMMENT ON COLUMN public."TB_USER"."USER_RESET_CODE" IS 'Encrypted code passed to the user at the point of a password reset.';
COMMENT ON COLUMN public."TB_USER"."USRSTA_CD" IS 'User Status Code';
COMMENT ON COLUMN public."TB_USER"."USER_RESET_PRSN_ID" IS 'ID of the individual (Staff User) who performed the reset';
COMMENT ON COLUMN public."TB_USER"."USER_FNAME" IS 'First Name of the User';
COMMENT ON COLUMN public."TB_USER"."USER_LNAME" IS 'Last Name of the User';


-- Index: public."XIE1TB_USER"

-- DROP INDEX public."XIE1TB_USER";

CREATE INDEX "XIE1TB_USER"
  ON public."TB_USER"
  USING btree
  ("USRTYP_CD" COLLATE pg_catalog."default");

-- Index: public."XIE2TB_USER"

-- DROP INDEX public."XIE2TB_USER";

CREATE INDEX "XIE2TB_USER"
  ON public."TB_USER"
  USING btree
  ("USERNAME" COLLATE pg_catalog."default");

-- Index: public."XIE3TB_USER"

-- DROP INDEX public."XIE3TB_USER";

CREATE INDEX "XIE3TB_USER"
  ON public."TB_USER"
  USING btree
  (lower("USERNAME"::text) COLLATE pg_catalog."default");

-- Index: public."XIE4TB_USER"

-- DROP INDEX public."XIE4TB_USER";

CREATE INDEX "XIE4TB_USER"
  ON public."TB_USER"
  USING btree
  ("USRTYP_CD" COLLATE pg_catalog."default", "USER_ID");

-- Index: public."XIF8TB_USER"

-- DROP INDEX public."XIF8TB_USER";

CREATE INDEX "XIF8TB_USER"
  ON public."TB_USER"
  USING btree
  ("USRSTA_CD" COLLATE pg_catalog."default");

-- Index: public."XIF9TB_USER"

-- DROP INDEX public."XIF9TB_USER";

CREATE INDEX "XIF9TB_USER"
  ON public."TB_USER"
  USING btree
  ("USER_RESET_PRSN_ID");




-- =======================================================================


  CREATE TABLE "TB_SCRTY_AUTH" 
   (	"SCRAUTH_ID" serial NOT NULL, 
	"SCRAUTH_NAME" character varying(60) NOT NULL, 
	"SCRAUTH_DE" character varying(200) NOT NULL,   
	"SCRAUTH_KEY" character varying(60) NOT NULL, 
	 CONSTRAINT "XPKTB_SCRTY_AUTH" PRIMARY KEY ("SCRAUTH_ID"), 
	 CONSTRAINT "XAK1TB_SCRTY_AUTH" UNIQUE ("SCRAUTH_KEY")
	 );

   COMMENT ON COLUMN "TB_SCRTY_AUTH"."SCRAUTH_ID" IS 'Security Authority Surrogate Key';
   COMMENT ON COLUMN "TB_SCRTY_AUTH"."SCRAUTH_NAME" IS 'Authority Name, used within the application to reference the authority';
   COMMENT ON COLUMN "TB_SCRTY_AUTH"."SCRAUTH_DE" IS 'Authority Description, to be displayed within the administration screens.';
   COMMENT ON COLUMN "TB_SCRTY_AUTH"."SCRAUTH_KEY" IS 'Unique key name of the security authority';
   COMMENT ON TABLE "TB_SCRTY_AUTH"  IS 'A permission for a specific function within the CRRS application. A permission ca be for a Function within the application, or it can be to view a specific set of data.';

  -- ===================================================================
   
 CREATE TABLE "TB_SCRTY_GRP" 
   (	"SCRGRP_ID" serial NOT NULL, 
	"SCRGRP_NAME" character varying(60) NOT NULL, 
	"SCRGRP_DE" character varying(200) NOT NULL, 
	"SCRGRP_LEVEL" INTEGER DEFAULT 100 NOT NULL, 
	 CONSTRAINT "XPKTB_SCRTY_GRP" PRIMARY KEY ("SCRGRP_ID")
   );

   COMMENT ON COLUMN "TB_SCRTY_GRP"."SCRGRP_ID" IS 'Security Group Surrogate Key';
   COMMENT ON COLUMN "TB_SCRTY_GRP"."SCRGRP_NAME" IS 'Security group name';
   COMMENT ON COLUMN "TB_SCRTY_GRP"."SCRGRP_DE" IS 'Security Group Description';
   COMMENT ON COLUMN "TB_SCRTY_GRP"."SCRGRP_LEVEL" IS 'Security Level of the Security Group. Example, SYS_ADMIN=1, BOOTH_STAFF=20, PUBLIC=100.  Used to determine what security groups are available to assign to staff';
   COMMENT ON TABLE "TB_SCRTY_GRP"  IS 'Contains information about security groups.';   
   
  -- ===================================================================   
   
  CREATE TABLE "TB_SCRTY_GRP_AUTH" 
   (	"SCRGRP_ID" INTEGER NOT NULL, 
	"SCRAUTH_ID" INTEGER NOT NULL, 
	 CONSTRAINT "XPKTB_SCRTY_GRP_AUTH" PRIMARY KEY ("SCRGRP_ID", "SCRAUTH_ID"), 
	 CONSTRAINT "SCTB_AUTH_TO_SCRTY_GRP_AUTH" FOREIGN KEY ("SCRAUTH_ID") REFERENCES "TB_SCRTY_AUTH" ("SCRAUTH_ID"), 
	 CONSTRAINT "SCTB_GRP_TO_SCRTY_GRP_AUTH" FOREIGN KEY ("SCRGRP_ID") REFERENCES "TB_SCRTY_GRP" ("SCRGRP_ID")
   ) ;

   COMMENT ON COLUMN "TB_SCRTY_GRP_AUTH"."SCRGRP_ID" IS 'Security Group Surrogate Key';
   COMMENT ON COLUMN "TB_SCRTY_GRP_AUTH"."SCRAUTH_ID" IS 'Security Authority Surrogate Key';;
   COMMENT ON TABLE "TB_SCRTY_GRP_AUTH"  IS 'Join table - stores assignments of Security Authorities to Groups';

  CREATE INDEX "XIF1TB_SCRTY_GRP_AUTH" ON "TB_SCRTY_GRP_AUTH" ("SCRGRP_ID");

  CREATE INDEX "XIF2TB_SCRTY_GRP_AUTH" ON "TB_SCRTY_GRP_AUTH" ("SCRAUTH_ID");


-- =================================================


-- Table: public."TB_USER_SCRTY"

CREATE TABLE public."TB_USER_SCRTY"
(
  "USER_ID" integer NOT NULL, -- System-generated ID for a User.
  "SCRGRP_ID" integer NOT NULL, -- Security Group Surrogate Key
  CONSTRAINT "XPKTB_USER_SCRTY" PRIMARY KEY ("USER_ID", "SCRGRP_ID"),
  CONSTRAINT "SCRTY_GRP_TO_SCRTY_USER" FOREIGN KEY ("SCRGRP_ID")
      REFERENCES public."TB_SCRTY_GRP" ("SCRGRP_ID") MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "SCRTY_USER_TO_SCRTY_USER" FOREIGN KEY ("USER_ID")
      REFERENCES public."TB_USER" ("USER_ID") MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION  
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."TB_USER_SCRTY"
  OWNER TO postgres;
COMMENT ON TABLE public."TB_USER_SCRTY"
  IS 'Table to associate Users with Security groups';
COMMENT ON COLUMN public."TB_USER_SCRTY"."USER_ID" IS 'System-generated ID for a User.';
COMMENT ON COLUMN public."TB_USER_SCRTY"."SCRGRP_ID" IS 'Security Group Surrogate Key';


CREATE INDEX "XIF1TB_USER_SCRTY"
  ON public."TB_USER_SCRTY"
  USING btree
  ("USER_ID");



  -- =================================================

  CREATE TABLE "TB_CONFIG" 
   (	
	"CFGPRM_ID" serial NOT NULL,
	"CFGPRM_KEY" character varying(100) NOT NULL, 
	"CFGPRM_VAL" character varying(100) NOT NULL,	
	"CFGPRM_DE" character varying(300) NOT NULL, 
	 CONSTRAINT "XPKTB_CONFIG" PRIMARY KEY ("CFGPRM_ID")
	) 
	 ;

   COMMENT ON COLUMN "TB_CONFIG"."CFGPRM_ID" IS 'Surrogate ID for a configurable system parameter';
   COMMENT ON COLUMN "TB_CONFIG"."CFGPRM_DE" IS 'Description or comments for a configurable system parameter';
   COMMENT ON COLUMN "TB_CONFIG"."CFGPRM_VAL" IS 'Parameter value for a configurable system parameter';
   COMMENT ON COLUMN "TB_CONFIG"."CFGPRM_KEY" IS 'ID name for a configurable parameter value';   
   COMMENT ON TABLE "TB_CONFIG"  IS 'Table for holding configurable system parameters.';
   
 -- =================================================
   
    CREATE TABLE "TB_BATCH_JOB_CD" 
   (	"BATJOC_CD" character varying(10) NOT NULL, 
	"BATJOC_DE" character varying(30) NOT NULL, 
	"BATJOC_COMMENT" character varying(500) NOT NULL, 
	 CONSTRAINT "XPKTB_BATCH_JOB_CD" PRIMARY KEY ("BATJOC_CD")
  
   )  ;

   COMMENT ON COLUMN "TB_BATCH_JOB_CD"."BATJOC_CD" IS 'Batch Job Code value';
   COMMENT ON COLUMN "TB_BATCH_JOB_CD"."BATJOC_DE" IS 'Batch Job Code description';
   COMMENT ON COLUMN "TB_BATCH_JOB_CD"."BATJOC_COMMENT" IS 'Batch Job Comments; include at least Job(s) involved and execution scheduling';
   COMMENT ON TABLE "TB_BATCH_JOB_CD"  IS 'Batch Job code table';

     CREATE TABLE "TB_BATCH_JOB_STATUS_CD" 
   (	"BATJOBSTA_CD" character varying(10) NOT NULL, 
	"BATJOBSTA_DE" character varying(50) NOT NULL, 
	 CONSTRAINT "XPKTB_BATCH_JOB_STATUS_CD" PRIMARY KEY ("BATJOBSTA_CD")
   )  ;

   COMMENT ON COLUMN "TB_BATCH_JOB_STATUS_CD"."BATJOBSTA_CD" IS 'Batch Job Status Code value';
   COMMENT ON COLUMN "TB_BATCH_JOB_STATUS_CD"."BATJOBSTA_DE" IS 'Batch Job Status Code description';
   COMMENT ON TABLE "TB_BATCH_JOB_STATUS_CD"  IS 'Batch Job Status Code table';   

  CREATE TABLE "TB_BATCH_JOB" 
   (	"BATJOB_ID" serial NOT NULL, 
	"BATJOC_CD" character varying(10) NOT NULL, 
	"BATJOB_START_TS" timestamp without time zone NOT NULL, 
	"BATJOB_END_TS" timestamp without time zone, 
	"BATJOBSTA_CD" character varying(10) NOT NULL, 
	"BATJOB_DETAILS" character varying(200), 
	 CONSTRAINT "XPKTB_BATCH_JOB" PRIMARY KEY ("BATJOB_ID"),
	 CONSTRAINT "BATCH_TO_BATCH_CODE" FOREIGN KEY ("BATJOC_CD")
		REFERENCES public."TB_BATCH_JOB_CD" ("BATJOC_CD") ,
	 CONSTRAINT "BATCH_TO_BATCH_STATUS" FOREIGN KEY ("BATJOBSTA_CD")
		REFERENCES public."TB_BATCH_JOB_STATUS_CD" ("BATJOBSTA_CD") 
   ) 
   ;

   COMMENT ON COLUMN "TB_BATCH_JOB"."BATJOB_ID" IS 'Batch Job ID';
   COMMENT ON COLUMN "TB_BATCH_JOB"."BATJOC_CD" IS 'Batch Job Code value';
   COMMENT ON COLUMN "TB_BATCH_JOB"."BATJOB_START_TS" IS 'Start Date of a Batch Job';
   COMMENT ON COLUMN "TB_BATCH_JOB"."BATJOB_END_TS" IS 'End Date of a Batch Job';
   COMMENT ON COLUMN "TB_BATCH_JOB"."BATJOBSTA_CD" IS 'Batch Status Code value';
   COMMENT ON COLUMN "TB_BATCH_JOB"."BATJOB_DETAILS" IS 'Details of the batch job';
   COMMENT ON TABLE "TB_BATCH_JOB"  IS 'Batch Job Table';
   
   
  -- ===================================================================
  -- client_id = Column(String(48), index=True)
  -- client_secret = Column(String(120))
  -- issued_at = Column(
  --     Integer, nullable=False,
  --     default=lambda: int(time.time())
  -- )
  -- expires_at = Column(Integer, nullable=False, default=0)

  -- redirect_uri = Column(Text, nullable=False, default='')
  -- token_endpoint_auth_method = Column(
  --     String(48), default='client_secret_basic')
  -- grant_type = Column(Text, nullable=False, default='')
  -- response_type = Column(Text, nullable=False, default='')
  -- scope = Column(Text, nullable=False, default='')

  -- client_name = Column(String(100))
  -- client_uri = Column(Text)
  -- logo_uri = Column(Text)
  -- contact = Column(Text)
  -- tos_uri = Column(Text)
  -- policy_uri = Column(Text)
  -- jwks_uri = Column(Text)
  -- jwks_text = Column(Text)
  -- i18n_metadata = Column(Text)

  -- software_id = Column(String(36))
  -- software_version = Column(String(48))
  CREATE TABLE "TB_OAUTH2_CLIENT"
    (	"OAUTH2CL_ID" serial NOT NULL,
       "client_id" character varying(48),
       "client_secret" character varying(120),
       "issued_at" integer NOT NULL,
       "expires_at" integer NOT NULL DEFAULT 0,
       "redirect_uri" text NOT NULL,
       "token_endpoint_auth_method" character varying(48),
       "grant_type" text,
       "response_type" text,
       "scope" text,
       "client_name" character varying(100),
       "client_uri" text,
       "logo_uri" text,
       "contact" text,
       "tos_uri" text,
       "policy_uri" text,
       "jwks_uri" text,
       "jwks_text" text,
       "i18n_metadata" text,
       "software_id" character varying(36),
       "software_version" character varying(48),
 	    CONSTRAINT "XPKTB_OAUTH2_CLIENT" PRIMARY KEY ("OAUTH2CL_ID")
    );
    CREATE INDEX "IDX1TB_OAUTH2_CLIENT" ON "TB_OAUTH2_CLIENT" ("client_id");

CREATE TABLE public."TB_USER_OAUTH2_CLIENT"
(
    "USER_ID" integer NOT NULL,
  "OAUTH2CL_ID" integer NOT NULL,
  CONSTRAINT "XPKTB_USER_OAUTH2_CLIENT" PRIMARY KEY ("USER_ID", "OAUTH2CL_ID"),
  CONSTRAINT "USER_TO_OAUTH2_CLIENT" FOREIGN KEY ("OAUTH2CL_ID")
      REFERENCES public."TB_OAUTH2_CLIENT" ("OAUTH2CL_ID") MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT "OAUTH2_CODE_TO_SCRTY_USER" FOREIGN KEY ("USER_ID")
        REFERENCES public."TB_USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."TB_USER_OAUTH2_CLIENT"
  OWNER TO postgres;
COMMENT ON TABLE public."TB_USER_OAUTH2_CLIENT"
  IS 'Table to associate Users with Oauth Clients';
COMMENT ON COLUMN public."TB_USER_OAUTH2_CLIENT"."OAUTH2CL_ID" IS 'Oauth Client Id';

  -- ===================================================================
   
  -- code = Column(String(120), unique=True, nullable=False)
  -- client_id = Column(String(48))
  -- redirect_uri = Column(Text, default='')
  -- response_type = Column(Text, default='')
  -- scope = Column(Text, default='')
  -- auth_time = Column(
  --     Integer, nullable=False,
  --     default=lambda: int(time.time())
  -- )

 CREATE TABLE "TB_OAUTH2_CODE"
   (	"OAUTH2CD_ID" serial NOT NULL,
        "USER_ID" integer NOT NULL,
      "code" character varying(120) NOT NULL,
      "client_id" character varying(48),
      "redirect_uri" text,
      "response_type" text,
      "scope" text,
      "auth_time" integer NOT NULL,
	    CONSTRAINT "XPKTB_OAUTH2_CODE" PRIMARY KEY ("OAUTH2CD_ID"),
	    CONSTRAINT "OAUTH2_CODE_TO_USER" FOREIGN KEY ("USER_ID")
            REFERENCES public."TB_USER" ("USER_ID")
   );
  CREATE INDEX "IDX1TB_OAUTH2_CODE" ON "TB_OAUTH2_CODE" ("code");

--CREATE TABLE public."TB_USER_OAUTH2_CODE"
--(
--  "USER_ID" integer NOT NULL,
--  "OAUTH2CD_ID" integer NOT NULL,
--  CONSTRAINT "XPKTB_USER_OAUTH2_CODE" PRIMARY KEY ("USER_ID", "OAUTH2CD_ID"),
--  CONSTRAINT "USER_TO_OAUTH2_CODE" FOREIGN KEY ("OAUTH2CD_ID")
--      REFERENCES public."TB_OAUTH2_CODE" ("OAUTH2CD_ID") MATCH SIMPLE
--      ON UPDATE NO ACTION ON DELETE NO ACTION,
--  CONSTRAINT "OAUTH2_CODE_TO_SCRTY_USER" FOREIGN KEY ("USER_ID")
--      REFERENCES public."TB_USER" ("USER_ID") MATCH SIMPLE
--      ON UPDATE NO ACTION ON DELETE NO ACTION
--)
--WITH (
--  OIDS=FALSE
--);
--ALTER TABLE public."TB_USER_OAUTH2_CODE"
--  OWNER TO postgres;
--COMMENT ON TABLE public."TB_USER_OAUTH2_CODE"
--  IS 'Table to associate Users with Oauth Tokens';
--COMMENT ON COLUMN public."TB_USER_OAUTH2_CODE"."USER_ID" IS 'System-generated ID for a User.';
--COMMENT ON COLUMN public."TB_USER_OAUTH2_CODE"."OAUTH2CD_ID" IS 'Oauth Code Id';

  -- ===================================================================
   
  -- client_id = Column(String(48))
  -- token_type = Column(String(40))
  -- access_token = Column(String(255), unique=True, nullable=False)
  -- refresh_token = Column(String(255), index=True)
  -- scope = Column(Text, default='')
  -- revoked = Column(Boolean, default=False)
  -- issued_at = Column(
  --     Integer, nullable=False, default=lambda: int(time.time())
  -- )
  -- expires_in = Column(Integer, nullable=False, default=0)

 CREATE TABLE "TB_OAUTH2_TOKEN" 
   (	"OAUTH2TKN_ID" serial NOT NULL,
        "USER_ID" integer NOT NULL,
      "client_id" character varying(48), 
      "token_type" character varying(40), 
      "access_token" character varying(255) NOT NULL, 
      "refresh_token" character varying(255), 
      "scope" text,
      "revoked" boolean,
      "issued_at" integer NOT NULL, 
      "expires_in" integer NOT NULL DEFAULT 0, 
	    CONSTRAINT "XPKTB_OAUTH2_TOKEN" PRIMARY KEY ("OAUTH2TKN_ID"),
	    CONSTRAINT "OAUTH2_TOKEN_TO_USER" FOREIGN KEY ("USER_ID")
            REFERENCES public."TB_USER" ("USER_ID")
   );  

    CREATE INDEX "IDX1TB_OAUTH2_TOKEN" ON "TB_OAUTH2_TOKEN" ("access_token");
    CREATE INDEX "IDX2TB_OAUTH2_TOKEN" ON "TB_OAUTH2_TOKEN" ("refresh_token");


--CREATE TABLE public."TB_USER_OAUTH2_TOKEN"
--(
--  "USER_ID" integer NOT NULL, -- System-generated ID for a User.
--  "OAUTH2TKN_ID" integer NOT NULL, -- Security Group Surrogate Key
--  CONSTRAINT "XPKTB_USER_OAUTH2_TOKEN" PRIMARY KEY ("USER_ID", "OAUTH2TKN_ID"),
--  CONSTRAINT "USER_TO_OAUTH2_TOKEN" FOREIGN KEY ("OAUTH2TKN_ID")
--      REFERENCES public."TB_OAUTH2_TOKEN" ("OAUTH2TKN_ID") MATCH SIMPLE
--      ON UPDATE NO ACTION ON DELETE NO ACTION,
--  CONSTRAINT "OAUTH2_TOKEN_TO_USER" FOREIGN KEY ("USER_ID")
--      REFERENCES public."TB_USER" ("USER_ID") MATCH SIMPLE
--      ON UPDATE NO ACTION ON DELETE NO ACTION
--)
--WITH (
--  OIDS=FALSE
--);
--ALTER TABLE public."TB_USER_OAUTH2_TOKEN"
--  OWNER TO postgres;
--COMMENT ON TABLE public."TB_USER_OAUTH2_TOKEN"
--  IS 'Table to associate Users with Oauth Tokens';
--COMMENT ON COLUMN public."TB_USER_OAUTH2_TOKEN"."USER_ID" IS 'System-generated ID for a User.';
--COMMENT ON COLUMN public."TB_USER_OAUTH2_TOKEN"."OAUTH2TKN_ID" IS 'Oauth Token Id';














