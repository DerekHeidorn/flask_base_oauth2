-- 1;Customer Access;General Customer Access;CUST_ACCESS
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (1, 'Customer Access', 'General Customer Access', 'CUST_ACCESS');

-- 5;Customer Profile;Customer Profile;CUST_PROFILE
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (2, 'Customer Profile', 'Customer Profile', 'CUST_PROFILE');
	
-- 2;Staff Access;General Staff Access;STAFF_ACCESS
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (301, 'Staff Access', 'General Staff Access', 'STAFF_ACCESS');
	
-- 3;Batch Operations;General Batch Operation Permissions;BATCH	
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (302, 'Batch Operations', 'General Batch Operation Permissions', 'BATCH');
	
-- 4;System Operations;General System Permissions;SYSTEM
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (303, 'System Operations', 'General System Permissions', 'SYSTEM');	
	
-- 1;SYS_ADMIN;System Administrator;1
INSERT INTO public.TB_SCRTY_GRP(
            SCRGRP_ID, SCRGRP_NAME, SCRGRP_DE, SCRGRP_LEVEL)
    VALUES (1, 'SYS_ADMIN', 'System Administrator', 1);

-- 2;CUSTOMER;Customer;100
INSERT INTO public.TB_SCRTY_GRP(
            SCRGRP_ID, SCRGRP_NAME, SCRGRP_DE, SCRGRP_LEVEL)
    VALUES (2, 'CUSTOMER', 'Customer', 100);
	
-- SYS_ADMIN
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (1, 301);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (1, 302);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (1, 303);

-- CUSTOMER
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (2, 1);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (2, 2);

-- Sys Admin Staff
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_RESET_PRSN_ID, 
            USER_FNAME, USER_LNAME)
    VALUES (1, 'c957fece-e465-11e8-9f32-f2801f1b9fd1', 'sys.admin@foo.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            '2', 0, null, 'XQYpe3fGFp0mJ0CxNGBpZCbA1GCWRegM', 
            null, null, 'A', null, 
            'Sys', 'Admin');
		
-- Customer		
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_RESET_PRSN_ID, 
            USER_FNAME, USER_LNAME)
    VALUES (2, 'c95802ac-e465-11e8-9f32-f2801f1b9fd1', 'Joe.Customer@foo.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            '3', 0, null, 'XQYpe3fFFp0mJFCxNGBpZCbA1GCWRegM', 
            null, null, 'A', null, 
            'Joe', 'Customer');			


INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (1, 1);
	
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (2, 2);


INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (1, 1);

INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (2, 1);

ALTER SEQUENCE public.TB_USER_USER_ID_seq RESTART WITH 100;
ALTER SEQUENCE public.TB_OAUTH2_CLIENT_OAUTH2CL_ID_seq RESTART WITH 10;


