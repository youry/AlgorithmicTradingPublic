
-- DB script to clear all data from all tables under the market schema in the algtrading db. 
-- for testing 
DO
$$
DECLARE
    tbl text;
BEGIN
    -- loop through all tables in the market schema
    FOR tbl IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'market'
    LOOP
        -- truncate each table 
        EXECUTE format('TRUNCATE TABLE market.%I RESTART IDENTITY CASCADE;', tbl);
    END LOOP;
END;
$$;
