-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP SEQUENCE public.ecig_colors_id_seq;

CREATE SEQUENCE public.ecig_colors_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ecig_flavors_id_seq;

CREATE SEQUENCE public.ecig_flavors_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ecig_images_id_seq;

CREATE SEQUENCE public.ecig_images_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ecig_nicotine_levels_id_seq;

CREATE SEQUENCE public.ecig_nicotine_levels_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ecig_product_attributes_id_seq;

CREATE SEQUENCE public.ecig_product_attributes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ecig_product_id_seq;

CREATE SEQUENCE public.ecig_product_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ecig_review_attributes_id_seq;

CREATE SEQUENCE public.ecig_review_attributes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ecig_reviews_id_seq;

CREATE SEQUENCE public.ecig_reviews_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.ecig_product definition

-- Drop table

-- DROP TABLE public.ecig_product;

CREATE TABLE public.ecig_product (
	id serial4 NOT NULL,
	product_name varchar NULL,
	site_name varchar NULL,
	url varchar NULL,
	site_category varchar NULL,
	site_tag varchar NULL,
	sku varchar NULL,
	brand varchar NULL,
	html text NULL,
	plain_text text NULL,
	price varchar NULL,
	price_sale varchar NULL,
	flavor_text text NULL,
	description text NULL,
	package_contents text NULL,
	ingredients text NULL,
	warnings text NULL,
	eliquid_contents varchar NULL,
	puffs varchar NULL,
	coil varchar NULL,
	battery_text varchar NULL,
	power_level varchar NULL,
	nicotine_level_text varchar NULL,
	stock_status varchar NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	features text NULL,
	CONSTRAINT ecig_product_pkey PRIMARY KEY (id),
	CONSTRAINT ecig_product_url_key UNIQUE (url)
);

-- Table Triggers

create trigger set_timestamps_ecig_product before
insert
    or
update
    on
    public.ecig_product for each row execute function set_timestamps();


-- public.ecig_colors definition

-- Drop table

-- DROP TABLE public.ecig_colors;

CREATE TABLE public.ecig_colors (
	id serial4 NOT NULL,
	product_id int4 NULL,
	color_name varchar NULL,
	color_description varchar NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	CONSTRAINT ecig_colors_pkey PRIMARY KEY (id),
	CONSTRAINT ecig_colors_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.ecig_product(id)
);

-- Table Triggers

create trigger set_timestamps_ecig_colors before
insert
    or
update
    on
    public.ecig_colors for each row execute function set_timestamps();


-- public.ecig_flavors definition

-- Drop table

-- DROP TABLE public.ecig_flavors;

CREATE TABLE public.ecig_flavors (
	id serial4 NOT NULL,
	product_id int4 NULL,
	flavor_name varchar NULL,
	flavor_description varchar NULL,
	flavor_category varchar NULL,
	iced_bool bool NULL,
	cbd_bool bool NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	CONSTRAINT ecig_flavors_pkey PRIMARY KEY (id),
	CONSTRAINT ecig_flavors_ecig_product_fk FOREIGN KEY (product_id) REFERENCES public.ecig_product(id)
);

-- Table Triggers

create trigger set_timestamps_ecig_flavors before
insert
    or
update
    on
    public.ecig_flavors for each row execute function set_timestamps();


-- public.ecig_images definition

-- Drop table

-- DROP TABLE public.ecig_images;

CREATE TABLE public.ecig_images (
	id serial4 NOT NULL,
	product_id int4 NULL,
	url varchar NULL,
	"path" varchar NULL,
	title varchar NULL,
	alt_text varchar NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	iced_bool bool NULL,
	has_screen_bool bool NULL,
	CONSTRAINT ecig_images_pkey PRIMARY KEY (id),
	CONSTRAINT ecig_images_ecig_product_fk FOREIGN KEY (product_id) REFERENCES public.ecig_product(id)
);

-- Table Triggers

create trigger set_timestamps_ecig_images before
insert
    or
update
    on
    public.ecig_images for each row execute function set_timestamps();


-- public.ecig_nicotine_levels definition

-- Drop table

-- DROP TABLE public.ecig_nicotine_levels;

CREATE TABLE public.ecig_nicotine_levels (
	id serial4 NOT NULL,
	product_id int4 NULL,
	value float8 NULL,
	unit varchar NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	CONSTRAINT ecig_nicotine_levels_pkey PRIMARY KEY (id),
	CONSTRAINT ecig_nicotine_levels_ecig_product_fk FOREIGN KEY (product_id) REFERENCES public.ecig_product(id)
);

-- Table Triggers

create trigger set_timestamps_ecig_nicotine_levels before
insert
    or
update
    on
    public.ecig_nicotine_levels for each row execute function set_timestamps();


-- public.ecig_product_attributes definition

-- Drop table

-- DROP TABLE public.ecig_product_attributes;

CREATE TABLE public.ecig_product_attributes (
	id serial4 NOT NULL,
	product_id int4 NULL,
	total_ounces_per_ml float8 NULL,
	product_category varchar NULL,
	screen_bool bool NULL,
	disposable_bool bool NULL,
	rechargeable_bool bool NULL,
	battery_bool bool NULL,
	usb_bool bool NULL,
	adjustable_bool bool NULL,
	tfn_bool bool NULL,
	nic_free varchar NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	eliquid_content varchar NULL,
	CONSTRAINT ecig_product_attributes_pkey PRIMARY KEY (id),
	CONSTRAINT unique_product_id UNIQUE (product_id),
	CONSTRAINT ecig_product_attributes_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.ecig_product(id)
);

-- Table Triggers

create trigger set_timestamps_ecig_product_attributes before
insert
    or
update
    on
    public.ecig_product_attributes for each row execute function set_timestamps();


-- public.ecig_review_attributes definition

-- Drop table

-- DROP TABLE public.ecig_review_attributes;

CREATE TABLE public.ecig_review_attributes (
	id serial4 NOT NULL,
	product_id int4 NULL,
	review_attribute_question varchar NULL,
	review_attribute_value varchar NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	CONSTRAINT ecig_review_attr_pkey PRIMARY KEY (id),
	CONSTRAINT ecig_review_attr_product_fk FOREIGN KEY (product_id) REFERENCES public.ecig_product(id)
);
CREATE UNIQUE INDEX ecig_review_attributes_product_id_idx ON public.ecig_review_attributes USING btree (product_id, review_attribute_question);

-- Table Triggers

create trigger set_timestamps_ecig_review_attrs before
insert
    or
update
    on
    public.ecig_review_attributes for each row execute function set_timestamps();


-- public.ecig_reviews definition

-- Drop table

-- DROP TABLE public.ecig_reviews;

CREATE TABLE public.ecig_reviews (
	id serial4 NOT NULL,
	product_id int4 NULL,
	review_date date NULL,
	rating float8 NULL,
	author varchar NULL,
	verified bool NULL,
	review_text varchar NULL,
	date_inserted timestamp DEFAULT now() NULL,
	date_updated timestamp DEFAULT now() NULL,
	variant varchar NULL,
	sweet_level int4 NULL,
	iced_level int4 NULL,
	CONSTRAINT ecig_review_pkey PRIMARY KEY (id),
	CONSTRAINT ecig_review_product_fk FOREIGN KEY (product_id) REFERENCES public.ecig_product(id)
);
CREATE UNIQUE INDEX ecig_reviews_review_date_idx ON public.ecig_reviews USING btree (review_date, author, variant, rating);

-- Table Triggers

create trigger set_timestamps_ecig_reviews before
insert
    or
update
    on
    public.ecig_reviews for each row execute function set_timestamps();


-- public.product_attributes_view source

CREATE OR REPLACE VIEW public.product_attributes_view
AS SELECT er.product_id,
    ep.product_name,
    ep.site_name,
    ep.url,
    ep.site_category,
    ep.site_tag,
    ep.price,
    ep.description,
    ep.package_contents,
    ep.eliquid_contents,
    ep.puffs,
    ep.battery_text,
    ep.nicotine_level_text,
    q2.flavors,
    er.total_ounces_per_ml,
    er.product_category,
    er.screen_bool,
    er.disposable_bool,
    er.battery_bool,
    er.usb_bool,
    er.adjustable_bool,
    er.tfn_bool,
    er.nic_free,
    er.eliquid_content
   FROM ecig_product_attributes er
     JOIN ecig_product ep ON ep.id = er.product_id
     LEFT JOIN ( SELECT ecig_flavors.product_id,
            string_agg(ecig_flavors.flavor_name::text, ', '::text) AS flavors
           FROM ecig_flavors
          GROUP BY ecig_flavors.product_id) q2 ON q2.product_id = ep.id
  ORDER BY ep.product_name;


-- public.review_attributes_view source

CREATE OR REPLACE VIEW public.review_attributes_view
AS SELECT ep.product_name,
    ep.site_name,
    ep.url,
    ep.site_category,
    ep.site_tag,
    ep.price,
    ep.description,
    ep.package_contents,
    ep.eliquid_contents,
    ep.puffs,
    ep.battery_text,
    ep.nicotine_level_text,
    q2.flavors,
    q1.sweet_level::double precision / 4.0::double precision * 100::double precision AS sweet_percentage,
    q1.iced_level::double precision / 4.0::double precision * 100::double precision AS iced_percentage
   FROM ecig_product ep
     LEFT JOIN ( SELECT era.product_id,
            max(
                CASE
                    WHEN era.review_attribute_question::text = 'Ice Level'::text THEN era.review_attribute_value
                    ELSE NULL::character varying
                END::text) AS iced_level,
            max(
                CASE
                    WHEN era.review_attribute_question::text = 'Sweet Level'::text THEN era.review_attribute_value
                    ELSE NULL::character varying
                END::text) AS sweet_level
           FROM ecig_review_attributes era
          GROUP BY era.product_id) q1 ON q1.product_id = ep.id
     LEFT JOIN ( SELECT ecig_flavors.product_id,
            string_agg(ecig_flavors.flavor_name::text, ', '::text) AS flavors
           FROM ecig_flavors
          GROUP BY ecig_flavors.product_id) q2 ON q2.product_id = ep.id
  ORDER BY ep.product_name;


-- public.reviews_view source

CREATE OR REPLACE VIEW public.reviews_view
AS SELECT er.review_date,
    er.sweet_level,
    er.iced_level,
    (er.sweet_level::numeric / 4.0)::double precision * 100::double precision AS sweet_percentage,
    (er.iced_level::numeric / 4.0)::double precision * 100::double precision AS iced_percentage,
    er.rating,
    er.author,
    er.verified,
    er.review_text,
    ep.product_name,
    ep.site_name,
    ep.url,
    ep.site_category,
    ep.site_tag,
    ep.price,
    ep.description,
    ep.package_contents,
    ep.eliquid_contents,
    ep.puffs,
    ep.battery_text,
    ep.nicotine_level_text,
    q2.flavors
   FROM ecig_reviews er
     JOIN ecig_product ep ON ep.id = er.product_id
     LEFT JOIN ( SELECT ecig_flavors.product_id,
            string_agg(ecig_flavors.flavor_name::text, ', '::text) AS flavors
           FROM ecig_flavors
          GROUP BY ecig_flavors.product_id) q2 ON q2.product_id = ep.id
  ORDER BY ep.product_name, er.review_date;



-- DROP FUNCTION public.set_timestamps();

CREATE OR REPLACE FUNCTION public.set_timestamps()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        NEW.date_inserted = NOW();
        NEW.date_updated = NOW();
    ELSIF (TG_OP = 'UPDATE') THEN
        NEW.date_updated = NOW();
    END IF;
    RETURN NEW;
END;
$function$
;