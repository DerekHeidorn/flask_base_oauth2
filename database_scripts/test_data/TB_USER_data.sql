-- 1;"Customer Access";"General Customer Access";"CUST_ACCESS"
INSERT INTO public."TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (1, 'Customer Access', 'General Customer Access', 'CUST_ACCESS');
	
-- 2;"Staff Access";"General Staff Access";"STAFF_ACCESS"
INSERT INTO public."TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (2, 'Staff Access', 'General Staff Access', 'STAFF_ACCESS');
	
-- 3;"Batch Operations";"General Batch Operation Permissions";"BATCH"	
INSERT INTO public."TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (3, 'Batch Operations', 'General Batch Operation Permissions', 'BATCH');
	
-- 4;"System Operations";"General System Permissions";"SYSTEM"
INSERT INTO public."TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (4, 'System Operations', 'General System Permissions', 'SYSTEM');	
	
-- 1;"SYS_ADMIN";"System Administrator";1
INSERT INTO public."TB_SCRTY_GRP"(
            "SCRGRP_ID", "SCRGRP_NAME", "SCRGRP_DE", "SCRGRP_LEVEL")
    VALUES (1, 'SYS_ADMIN', 'System Administrator', 1);

-- 2;"CUSTOMER";"Customer";100
INSERT INTO public."TB_SCRTY_GRP"(
            "SCRGRP_ID", "SCRGRP_NAME", "SCRGRP_DE", "SCRGRP_LEVEL")
    VALUES (2, 'CUSTOMER', 'Customer', 100);
	
-- SYS_ADMIN
INSERT INTO public."TB_SCRTY_GRP_AUTH"("SCRGRP_ID", "SCRAUTH_ID") VALUES (1, 1);
INSERT INTO public."TB_SCRTY_GRP_AUTH"("SCRGRP_ID", "SCRAUTH_ID") VALUES (1, 2);
INSERT INTO public."TB_SCRTY_GRP_AUTH"("SCRGRP_ID", "SCRAUTH_ID") VALUES (1, 3);
INSERT INTO public."TB_SCRTY_GRP_AUTH"("SCRGRP_ID", "SCRAUTH_ID") VALUES (1, 4);

-- CUSTOMER
INSERT INTO public."TB_SCRTY_GRP_AUTH"("SCRGRP_ID", "SCRAUTH_ID") VALUES (2, 1);

	
	
INSERT INTO "TB_USER" ("USER_FNAME", "USER_LNAME", "USER_LOGIN", "USRTYP_CD", "USRSTA_CD") VALUES ('Tester', 'Auto', 'auto@tester.com', '1', 'A') ;

-- Sys Admin Staff
INSERT INTO public."TB_USER"(
            "USER_ID", "USER_LOGIN", "USER_PASSWD", "USER_PASSWD_SALT", "USER_PASSWD_EXP_TS", 
            "USRTYP_CD", "USER_ATTEMPT_CNT", "USER_ATTEMPT_TS", "USER_PRIV_KEY", 
            "USER_ACTV_CODE", "USER_RESET_CODE", "USRSTA_CD", "USER_RESET_PRSN_ID", 
            "USER_FNAME", "USER_LNAME")
    VALUES (1, 'sys.admin@foo.com.invali', '8dcaecb4b70a28b989925e3e005555954a85e87c5f8086f1cb3648549f06163240c8ab576a65d88fde2005f68795e044b387ae8531d71aa9e1e3e4b18b5d6ddb', 'Q8Z6wiigjd9HgeCZamMdyiHBtvAvZLtu', null, 
            '2', 0, null, 'XQYpe3fGFp0mJ0CxNGBpZCbA1GCWRegM', 
            null, null, 'A', null, 
            'Sys', 'Admin');
		
-- Customer		
INSERT INTO public."TB_USER"(
            "USER_ID", "USER_LOGIN", "USER_PASSWD", "USER_PASSWD_SALT", "USER_PASSWD_EXP_TS", 
            "USRTYP_CD", "USER_ATTEMPT_CNT", "USER_ATTEMPT_TS", "USER_PRIV_KEY", 
            "USER_ACTV_CODE", "USER_RESET_CODE", "USRSTA_CD", "USER_RESET_PRSN_ID", 
            "USER_FNAME", "USER_LNAME")
    VALUES (2, 'Joe.Customer@foo.com.invali', '8dcaecb4b70a28b989925e3e005555954a85e87c5f8086f1cb3648549f06163240c8ab576a65d88fde2005f68795e044b387ae8531d71aa9e1e3e4b18b5d6ddb', 'Q8Z6wiigjd9HgeCZamMdyiHBtvAvZLtu', null, 
            '3', 0, null, 'XQYpe3fFFp0mJFCxNGBpZCbA1GCWRegM', 
            null, null, 'A', null, 
            'Joe', 'Customer');			


INSERT INTO public."TB_SCRTY_USER"(
            "USER_ID", "SCRGRP_ID")
    VALUES (1, 1);
	
INSERT INTO public."TB_SCRTY_USER"(
            "USER_ID", "SCRGRP_ID")
    VALUES (2, 2);	

