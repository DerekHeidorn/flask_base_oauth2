-- TB_SCRTY_AUTH
INSERT INTO "TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (1, "Customer Access", "General Customer Access", "CUST_ACCESS");
	
INSERT INTO "TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (2, "Staff Access", "General Staff Access", "STAFF_ACCESS");

INSERT INTO "TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (3, "Batch Operations", "General Batch Operation Permissions", "BATCH");

INSERT INTO "TB_SCRTY_AUTH"(
            "SCRAUTH_ID", "SCRAUTH_NAME", "SCRAUTH_DE", "SCRAUTH_KEY")
    VALUES (4, "System Operations", "General System Permissions", "SYSTEM");	
