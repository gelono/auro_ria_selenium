CREATE SEQUENCE info_id_seq START 1;


CREATE TABLE IF NOT EXISTS public.info
(
    id integer NOT NULL DEFAULT nextval('info_id_seq'::regclass),
    url character varying(255) COLLATE pg_catalog."default",
    title character varying(255) COLLATE pg_catalog."default",
    price_usd numeric(10,2),
    odometer integer,
    username character varying(255) COLLATE pg_catalog."default",
    phone_number character varying(15) COLLATE pg_catalog."default",
    image_url character varying(255) COLLATE pg_catalog."default",
    images_count integer,
    car_number character varying(20) COLLATE pg_catalog."default",
    car_vin character varying(20) COLLATE pg_catalog."default",
    datetime_found timestamp with time zone DEFAULT LOCALTIMESTAMP,
    CONSTRAINT info_pkey PRIMARY KEY (id)
);