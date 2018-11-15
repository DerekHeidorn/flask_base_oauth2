INSERT INTO public.tb_batch_job(
            batjob_id, batjoc_cd, batjob_start_ts, batjob_end_ts, batjobsta_cd,
            batjob_details)
    VALUES (1, 'STATS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'COMPLETED',
            'Testing Stats!');


ALTER SEQUENCE public.tb_batch_job_batjob_id_seq RESTART WITH 100;