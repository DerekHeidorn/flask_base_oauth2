-- CUSTOMER ACCESS
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (100, 'Customer Access', 'General Customer Access', 'CUST_ACCESS');

-- GROUPS
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (200, 'Group Access', 'Group Access', 'GRP_ACCESS');

INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (201, 'Group Admin Access', 'Group Admin Access', 'GRP_ADMIN');



-- REPORTS
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (300, 'Customer Report Access', 'Customer Report Access', 'RPT_ACCESS');

INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (301, 'Active Group Report', 'Active Group Report', 'RPT_ACTIVE_USER_GRP');

INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (302, 'Public Group Report', 'Public Group Report', 'RPT_PUBLIC_GROUPS');

INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (303, 'Active Group Membership Report', 'Active Group Membership Report', 'RPT_ACTIVE_USER_GRP_MEMBERSHIPS');

INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (304, 'Group Members Report', 'Group Members Report', 'RPT_GROUP_MEMBERS');

INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (305, 'Group Members Detail Report', 'Group Members Detail Report', 'RPT_GROUP_MEMBER_DETAILS');

	
-- 2;Staff Access;General Staff Access;STAFF_ACCESS
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (1000, 'Staff Access', 'General Staff Access', 'ADM_ACCESS');


-- 3;Batch Operations;General Batch Operation Permissions;BATCH	
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (1100, 'Batch Operations', 'General Batch Operation Permissions', 'BATCH_ACCESS');
	
-- 4;System Operations;General System Permissions;SYSTEM
INSERT INTO public.TB_SCRTY_AUTH(
            SCRAUTH_ID, SCRAUTH_NAME, SCRAUTH_DE, SCRAUTH_KEY)
    VALUES (1200, 'System Operations', 'General System Permissions', 'SYSTEM_ACCESS');

-- 2;CUSTOMER;Customer;100
INSERT INTO public.TB_SCRTY_GRP(
            SCRGRP_ID, SCRGRP_NAME, SCRGRP_DE, SCRGRP_LEVEL)
    VALUES (100, 'CUSTOMER', 'Customer', 100);

INSERT INTO public.TB_SCRTY_GRP(
            SCRGRP_ID, SCRGRP_NAME, SCRGRP_DE, SCRGRP_LEVEL)
    VALUES (200, 'CUSTOMER_SUB', 'Subscribed Customer', 80);

INSERT INTO public.TB_SCRTY_GRP(
            SCRGRP_ID, SCRGRP_NAME, SCRGRP_DE, SCRGRP_LEVEL)
    VALUES (300, 'CUSTOMER_GRP_SUB', 'Subscribed Group Manager', 60);

-- 1;SYS_ADMIN;System Administrator;1001
INSERT INTO public.TB_SCRTY_GRP(
            SCRGRP_ID, SCRGRP_NAME, SCRGRP_DE, SCRGRP_LEVEL)
    VALUES (1000, 'SYS_ADMIN', 'System Administrator', 1);

-- CUSTOMER
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (100, 100);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (100, 200);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (100, 300);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (100, 301);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (100, 302);

-- Subscribed CUSTOMER
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (200, 100);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (200, 200);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (200, 300);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (200, 301);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (200, 302);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (200, 303);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (200, 304);

-- Subscribed Group CUSTOMER
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 100);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 200);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 201);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 300);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 301);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 302);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 303);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 304);
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (300, 305);

-- SYS_ADMIN
INSERT INTO public.TB_SCRTY_GRP_AUTH(SCRGRP_ID, SCRAUTH_ID) VALUES (1000, 1000);





-- Sys Admin Staff
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (1000, 'c957fece-e465-11e8-9f32-f2801f1b9fd1', 'sys.admin@foo.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'S', 0, null, 'QFDbVjDtCwu2d4J523y6suQwtEleE3aE',
            null, null, 'A', TRUE,
            'Sys', 'Admin', 'Sys_Admin');

INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (1000, 1000);

INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (1000, 1);

-- Customer		
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (1, 'c95802ac-e465-11e8-9f32-f2801f1b9fd1', 'Joe.Customer@foo.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Joe', 'Customer', 'Joe_Customer');

	
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (1, 100);

INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (1, 1);


-- Subscribed Customer
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY,
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (200, '14468f27-44e8-4fc3-8cc6-3a48c80fd5aa', 'Joe.Subscribed@foo.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Joe', 'Subscribed', 'Joe_Subscribed');


INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (200, 200);

INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (200, 1);


-- Subscribed Group Customer
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY,
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (300, 'd71b920a-04a9-44d3-beda-a736601a64c5', 'Joe.Group.Subscribed@foo.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Joe', 'GroupSubscribed', 'Joe_GroupSubscribed');


INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (300, 300);

INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (300, 1);

ALTER SEQUENCE public.TB_USER_USER_ID_seq RESTART WITH 2000;
ALTER SEQUENCE public.TB_OAUTH2_CLIENT_OAUTH2CL_ID_seq RESTART WITH 200;



-- 4e5d14ab-e91e-49b3-9c61-795748c41e09		Iron Man					Tony Stark
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (3, '4e5d14ab-e91e-49b3-9c61-795748c41e09', 'Iron.Man@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Tony', 'Stark', 'Ironman');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (3, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (3, 1);
			
			
-- f55b7b25-6ef5-4727-9645-7564fb777f21		Wasp						Janet van Dyne
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (4, 'f55b7b25-6ef5-4727-9645-7564fb777f21', 'Wasp@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Janet', 'Dyne', 'Wasp');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (4, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (4, 1);
-- e4176c50-9e84-49d3-a2b7-f8773d57fb9b		Hulk						Dr. Robert Bruce Banner
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (5, 'e4176c50-9e84-49d3-a2b7-f8773d57fb9b', 'Hulk@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Bruce', 'Banner', 'Hulk');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (5, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (5, 1);

-- 29ef21b2-825f-4d49-a654-df9dd2295630		Scarlet Witch				Wanda Maximoff
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (6, '29ef21b2-825f-4d49-a654-df9dd2295630', 'Scarlet.Witch@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Wanda', 'Maximoff', 'Scarlet_Witch');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (6, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (6, 1);

-- 5fa2a30d-403c-4ae8-b3fa-5dd207ef926b		Vision						Victor Shade 
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (7, '5fa2a30d-403c-4ae8-b3fa-5dd207ef926b', 'Vision@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Victor', 'Shade', 'Vision');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (7, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (7, 1);

-- b130cdd5-e09c-471f-b3df-da80413d58d5		Black Widow					Natasha Alianovna Romanoff
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (8, 'b130cdd5-e09c-471f-b3df-da80413d58d5', 'Black.Widow@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Natasha', 'Romanoff', 'Black_Widow');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (8, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (8, 1);

-- b8919fd0-0379-4fe3-b81e-4d06f079ce1f		Falcon						Samuel "Snap" Thomas Wilson
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (9, 'b8919fd0-0379-4fe3-b81e-4d06f079ce1f', 'Falcon@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Samuel', 'Wilson', 'Falcon');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (9, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (9, 1);
-- 48667be7-9b99-4353-af8d-814b4c308b15		Captain Marvel				Monica Rambeau
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (10, '48667be7-9b99-4353-af8d-814b4c308b15', 'Captain.Marvel@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Monica', 'Rambeau', 'Captain_Marvel');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (10, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (10, 1);
-- d627b053-7986-41ab-9065-f37fec698148		War Machine					James Rupert "Rhodey" Rhodes
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (11, 'd627b053-7986-41ab-9065-f37fec698148', 'War.Machine@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'James', 'Rhodes', 'War_Machine');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (11, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (11, 1);
-- 179c80b3-a6f4-4c39-9edd-f38db0c7d0af		Spider-Man					Peter Benjamin Parker
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (12, '179c80b3-a6f4-4c39-9edd-f38db0c7d0af', 'Spider.Man@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Peter', 'Parker', 'Spider_Man');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (12, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (12, 1);
-- a787b4e4-b09d-4d08-9073-2b47c8abbe5b		Ant-Man						Scott Lang
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (13, 'a787b4e4-b09d-4d08-9073-2b47c8abbe5b', 'Ant.Man@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Scott', 'Lang', 'Ant_Man');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (13, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (13, 1);
-- fc21caba-fcfc-48b5-a567-2bee36ef535d		Luke Cage					Carl Lucas
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (14, 'fc21caba-fcfc-48b5-a567-2bee36ef535d', 'Luke.Cage@avengers.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Carl', 'Lucas', 'Luke_Cage');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (14, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (14, 1);
-- 8ead1ce9-8867-4523-a84e-a1cf920038df		Zoe Washburne				Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (15, '8ead1ce9-8867-4523-a84e-a1cf920038df', 'Zoe.Washburne@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Zoe', 'Washburne', 'ZoeW1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (15, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (15, 1);
-- bb3985d3-9d2f-49c7-8304-a8271330f762		Hoban "Wash" Washburne		Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (16, 'bb3985d3-9d2f-49c7-8304-a8271330f762', 'Hoban.Washburne@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Hoban', 'Washburne', 'Wash');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (16, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (16, 1);
-- ac08889e-1c82-4e4e-8912-8e7c95b81a25		Inara Serra					Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (17, 'ac08889e-1c82-4e4e-8912-8e7c95b81a25', 'Inara.Serra@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Inara', 'Serra', 'Inara_firefly');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (17, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (17, 1);
-- e6abb20f-75f7-43b2-8be6-421876ff4db4		Jayne Cobb					Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (18, 'e6abb20f-75f7-43b2-8be6-421876ff4db4', 'Jayne.Cobb@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Jayne', 'Cobb', 'Jayne_firefly');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (18, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (18, 1);
-- d9c83075-6efa-4554-9ab1-891ab6472950		Kaylee Frye					Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (19, 'd9c83075-6efa-4554-9ab1-891ab6472950', 'Kaylee.Frye@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Kaylee', 'Frye', 'Kaylee_firefly');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (19, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (19, 1);
-- 53271313-d6a6-41a4-b733-a2c450834e07		Simon Tam					Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (20, '53271313-d6a6-41a4-b733-a2c450834e07', 'Simon.Tam@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Simon', 'Tam', 'Simon_firefly');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (20, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (20, 1);
-- 3e1bef3b-562c-4c0c-a1b2-123c1385a1d4		River Tam					Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (21, '3e1bef3b-562c-4c0c-a1b2-123c1385a1d4', 'River.Tam@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'River', 'Tam', 'River_firefly');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (21, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (21, 1);
-- 441fa406-54c1-45b5-b33d-981b7197f277		Derrial Book				Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (22, '441fa406-54c1-45b5-b33d-981b7197f277', 'Derrial.Book@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Derrial', 'Book', 'Bishop');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (22, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (22, 1);
-- c64ea92c-757b-4846-a385-15ee2febb2e2		Ada Wong					Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (23, 'c64ea92c-757b-4846-a385-15ee2febb2e2', 'Ada.Book@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Ada', 'Wong', 'Ada_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (23, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (23, 1);
-- 0ec0aeb8-8f3b-4d51-a3a0-a862cfcf0f96		Albert Wesker				Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (24, '0ec0aeb8-8f3b-4d51-a3a0-a862cfcf0f96', 'Albert.Wesker@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Albert', 'Wesker', 'Albert_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (24, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (24, 1);
-- 68d3d343-d5cd-4d46-8cf7-f8707c46a148		Chris Redfield				Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (25, '68d3d343-d5cd-4d46-8cf7-f8707c46a148', 'Chris.Redfield@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Chris', 'Redfield', 'Chris_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (25, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (25, 1);
-- bfaec952-7b06-4791-a321-02a925ff59b4		Claire Redfield				Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (26, 'bfaec952-7b06-4791-a321-02a925ff59b4', 'Claire.Redfield@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Claire', 'Redfield', 'Claire_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (26, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (26, 1);
-- d81dc597-ed99-46a7-846f-6495898b40c9		Jill Valentine				Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (27, 'd81dc597-ed99-46a7-846f-6495898b40c9', 'Jill.Valentine@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Jill', 'Valentine', 'Jill_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (27, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (27, 1);
-- ac6e6270-87eb-4be7-b3ce-385d9a7a2057		Leon Scott Kennedy			Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (28, 'ac6e6270-87eb-4be7-b3ce-385d9a7a2057', 'Leon.Kennedy@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Leon', 'Kennedy', 'Leon_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (28, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (28, 1);
-- 78f59ccd-7dcf-4b85-8251-5bc1ba8f9b51		Rebecca Chambers			Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (29, '78f59ccd-7dcf-4b85-8251-5bc1ba8f9b51', 'Rebecca.Chambers@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Rebecca', 'Chambers', 'Rebecca_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (29, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (29, 1);
-- 121461d4-a78b-4bbb-9471-9cf8233fdc78		Janus Prospero (Alice)				Resident Evil
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (30, '121461d4-a78b-4bbb-9471-9cf8233fdc78', 'Janus.Prospero@ResidentEvil.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Janus', 'Prospero', 'Janus_1');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (30, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (30, 1);
-- a10541a9-46f4-49ae-97f4-625bc92b5f7c		Malcolm Reynolds					Firefly
INSERT INTO public.TB_USER(
            USER_ID, USER_UUID, USERNAME, USER_PASSWD, USER_PASSWD_SALT,
            USRTYP_CD, USER_ATTEMPT_CNT, USER_ATTEMPT_TS, USER_PRIV_KEY, 
            USER_ACTV_CODE, USER_RESET_CODE, USRSTA_CD, USER_PRIVATE_FL,
            USER_FNAME, USER_LNAME, USER_ALIAS)
    VALUES (31, 'a10541a9-46f4-49ae-97f4-625bc92b5f7c', 'Malcolm.Reynolds@Firefly.com.invali', '5adc7c7ceb10eed3fe8bdef909a8417f57a1e7a4fdf9503b39a9bb84b3e5e5fd3908d7599fc0e6db960807f2afce507dc3b20e45f761a870960893922bb70b1f', 'YSh3SpOres2CgkzFKi5s1FuSqSWYc7dS',
            'C', 0, null, 'BHc9UCugXO7F9PczI86uArbeOFncaYPl',
            null, null, 'A', FALSE,
            'Malcolm', 'Reynolds', 'Captain_Reynolds');
INSERT INTO public.TB_USER_SCRTY(
            USER_ID, SCRGRP_ID)
    VALUES (31, 200);
INSERT INTO public.TB_USER_OAUTH2_CLIENT(
            USER_ID, OAUTH2CL_ID)
    VALUES (31, 1);
-- 53e491f9-96b3-495f-8fd6-a6d0aa54e0fc

-- 21ce38c2-5456-40ac-a880-2b8477684a15

-- 0785e9e4-c80e-4f70-9c73-51fd1c63a142

-- 71dfe7fc-7279-46d9-a1ff-b6227d69aa73

-- 157b3c6c-c56f-467b-8311-2202a066c531

-- 1ed78d12-82c0-4eb6-bde8-b8413f9406f3

-- 5d7d2422-17e2-4613-9a5a-645675a4999a

-- 51111c6e-0c60-4fa6-8fae-9d89e61b2509

-- 3fd59bd4-6f32-4590-bb7a-0be27b9d9dfd

-- 36c3f1e9-3b66-4f49-8ca1-1da059659b28

-- 5f9e9005-f67d-4767-af24-6c690b71a5c6

-- fe81b81a-4eb5-4fef-9d72-00b1b14a284f

-- d8f2fd6f-de8b-4528-b0f4-aa01bb2d07a6

-- 1d478f27-af12-4719-9f44-3a5de8ab2d50

-- 083c29e5-eb97-4a33-b3fa-2a279a8d4bff

-- f70e16e3-9fa9-4d93-bff8-433a6cb751d9

-- e73eae4a-70ed-4366-9785-9cabefdb2b4e

-- dd67ea1d-f811-4b7c-97ec-9eeb69e759bf


-- Friendships
INSERT INTO public.tb_friendship(
            user_id, friend_user_id, friendship_sta_cd, friendship_from_ts)
    VALUES (1, 200, 'A', CURRENT_TIMESTAMP);