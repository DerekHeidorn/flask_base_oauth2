-- REM INSERTING into TB_USER_TYP_CD
Insert into "TB_USER_TYP_CD" ("USRTYP_CD","USRTYP_DE") values ('0','System');
Insert into "TB_USER_TYP_CD" ("USRTYP_CD","USRTYP_DE") values ('1','Batch');
Insert into "TB_USER_TYP_CD" ("USRTYP_CD","USRTYP_DE") values ('2','Staff');
Insert into "TB_USER_TYP_CD" ("USRTYP_CD","USRTYP_DE") values ('3','Customer');

-- REM INSERTING into TB_USER_STA_CD
Insert into "TB_USER_STA_CD" ("USRSTA_CD","USRSTA_DE") values ('A','Active');
Insert into "TB_USER_STA_CD" ("USRSTA_CD","USRSTA_DE") values ('I','Inactive');
Insert into "TB_USER_STA_CD" ("USRSTA_CD","USRSTA_DE") values ('R','Archived');

Insert into "TB_BATCH_JOB_STATUS_CD" ("BATJOBSTA_CD","BATJOBSTA_DE") values ('COMPLETED','Completed Successfully');
Insert into "TB_BATCH_JOB_STATUS_CD" ("BATJOBSTA_CD","BATJOBSTA_DE") values ('FAILED','Failed');
Insert into "TB_BATCH_JOB_STATUS_CD" ("BATJOBSTA_CD","BATJOBSTA_DE") values ('INPROGRESS','In Progress');
Insert into "TB_BATCH_JOB_STATUS_CD" ("BATJOBSTA_CD","BATJOBSTA_DE") values ('ERRORS','Errors');
Insert into "TB_BATCH_JOB_STATUS_CD" ("BATJOBSTA_CD","BATJOBSTA_DE") values ('DUPPROC','Duplicate Processs / Process Already Running');
Insert into "TB_BATCH_JOB_STATUS_CD" ("BATJOBSTA_CD","BATJOBSTA_DE") values ('WARNINGS','Completed With Warnings');
