--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--

DROP DATABASE ttndung;




--
-- Drop roles
--

DROP ROLE admin;


--
-- Roles
--

CREATE ROLE admin;
ALTER ROLE admin WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:6oEXMiFajQXvlXhituEAkA==$rJWxpc/4dfZn5nX4rWktsqbUbi+YIWtNFXmZf4jYroU=:DRt1FapM8dkxeex6uOV1jI8z2EzmQTPUGbGkErH+qf8=';






--
-- Databases
--

--
-- Database "template1" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Debian 14.4-1.pgdg110+1)
-- Dumped by pg_dump version 14.4 (Debian 14.4-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- Name: template1; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO admin;

\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: admin
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: admin
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- Database "ttndung" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Debian 14.4-1.pgdg110+1)
-- Dumped by pg_dump version 14.4 (Debian 14.4-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: ttndung; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE ttndung WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE ttndung OWNER TO admin;

\connect ttndung

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: app_ancu_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_ancu_scraper (
    id integer NOT NULL,
    post_title character varying(200),
    post_author character varying(100),
    description text,
    price_with_unit character varying(100),
    address text,
    area double precision,
    phone_number bigint,
    website character varying(191),
    url character varying(191) NOT NULL,
    type character varying(100),
    updated_at character varying(191),
    post_time bigint,
    coordinate character varying(191)
);


ALTER TABLE public.app_ancu_scraper OWNER TO admin;

--
-- Name: app_dangbannhadat_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_dangbannhadat_scraper (
    id integer NOT NULL,
    post_title character varying(200),
    post_author character varying(100),
    description text,
    price_with_unit character varying(100),
    area double precision,
    phone_number bigint,
    website character varying(191),
    url character varying(191) NOT NULL,
    type character varying(100),
    updated_at character varying(191),
    address text
);


ALTER TABLE public.app_dangbannhadat_scraper OWNER TO admin;

--
-- Name: app_facebook_comment_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_facebook_comment_scraper (
    id integer NOT NULL,
    post_id character varying(191) NOT NULL,
    post_comment_user_id character varying(191) NOT NULL,
    post_comment_parent_id character varying(191),
    post_message text NOT NULL,
    post_total_reactions bigint NOT NULL,
    post_image_link text,
    post_image_alt text,
    post_tags text,
    post_links text,
    post_attach_link text,
    "timestamp" double precision NOT NULL,
    created_at double precision NOT NULL,
    updated_at double precision NOT NULL
);


ALTER TABLE public.app_facebook_comment_scraper OWNER TO admin;

--
-- Name: app_facebook_comment_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_facebook_comment_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_facebook_comment_scraper_id_seq OWNER TO admin;

--
-- Name: app_facebook_comment_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_facebook_comment_scraper_id_seq OWNED BY public.app_facebook_comment_scraper.id;


--
-- Name: app_facebook_post_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_facebook_post_scraper (
    id integer NOT NULL,
    group_id character varying(191) NOT NULL,
    post_id character varying(191) NOT NULL,
    post_user_id character varying(191) NOT NULL,
    post_message text,
    post_image_link text,
    post_image_alt text,
    post_total_reactions bigint NOT NULL,
    post_total_comments bigint NOT NULL,
    post_total_shares bigint NOT NULL,
    "timestamp" double precision NOT NULL,
    created_at double precision NOT NULL,
    updated_at double precision NOT NULL
);


ALTER TABLE public.app_facebook_post_scraper OWNER TO admin;

--
-- Name: app_facebook_post_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_facebook_post_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_facebook_post_scraper_id_seq OWNER TO admin;

--
-- Name: app_facebook_post_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_facebook_post_scraper_id_seq OWNED BY public.app_facebook_post_scraper.id;


--
-- Name: app_facebook_reaction_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_facebook_reaction_scraper (
    id integer NOT NULL,
    post_id character varying(191) NOT NULL,
    post_user_id character varying(191) NOT NULL,
    like_reaction bigint,
    created_at double precision NOT NULL,
    updated_at double precision NOT NULL
);


ALTER TABLE public.app_facebook_reaction_scraper OWNER TO admin;

--
-- Name: app_facebook_reaction_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_facebook_reaction_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_facebook_reaction_scraper_id_seq OWNER TO admin;

--
-- Name: app_facebook_reaction_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_facebook_reaction_scraper_id_seq OWNED BY public.app_facebook_reaction_scraper.id;


--
-- Name: app_facebook_search_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_facebook_search_scraper (
    id integer NOT NULL,
    keyword character varying(191) NOT NULL,
    scrolls integer NOT NULL,
    name character varying(191) NOT NULL,
    bio character varying(191),
    work character varying(191),
    friends character varying(191),
    link character varying(191) NOT NULL,
    datetime character varying(191) NOT NULL,
    "timestamp" bigint NOT NULL
);


ALTER TABLE public.app_facebook_search_scraper OWNER TO admin;

--
-- Name: app_facebook_search_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_facebook_search_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_facebook_search_scraper_id_seq OWNER TO admin;

--
-- Name: app_facebook_search_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_facebook_search_scraper_id_seq OWNED BY public.app_facebook_search_scraper.id;


--
-- Name: app_facebook_user_profile_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_facebook_user_profile_scraper (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    user_name character varying(250) NOT NULL,
    name character varying(250) NOT NULL,
    work character varying(500) NOT NULL,
    education character varying(500) NOT NULL,
    friend_count integer NOT NULL,
    follower_count integer NOT NULL,
    following_count integer NOT NULL,
    cover_photo character varying(500) NOT NULL,
    profile_picture character varying(500) NOT NULL,
    created_at double precision NOT NULL,
    updated_at double precision NOT NULL
);


ALTER TABLE public.app_facebook_user_profile_scraper OWNER TO admin;

--
-- Name: app_facebook_user_profile_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_facebook_user_profile_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_facebook_user_profile_scraper_id_seq OWNER TO admin;

--
-- Name: app_facebook_user_profile_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_facebook_user_profile_scraper_id_seq OWNED BY public.app_facebook_user_profile_scraper.id;


--
-- Name: app_facebook_user_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_facebook_user_scraper (
    id integer NOT NULL,
    user_name character varying(191) NOT NULL,
    user_id character varying(191) NOT NULL,
    post_id text,
    post_comment_id text,
    post_reaction_id text,
    total_posts bigint NOT NULL,
    total_comments bigint NOT NULL,
    total_reactions bigint NOT NULL,
    created_at double precision NOT NULL,
    updated_at double precision NOT NULL
);


ALTER TABLE public.app_facebook_user_scraper OWNER TO admin;

--
-- Name: app_facebook_user_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_facebook_user_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_facebook_user_scraper_id_seq OWNER TO admin;

--
-- Name: app_facebook_user_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_facebook_user_scraper_id_seq OWNED BY public.app_facebook_user_scraper.id;


--
-- Name: app_google_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_google_scraper (
    id integer NOT NULL,
    keyword character varying(191) NOT NULL,
    crawled_page integer NOT NULL,
    title character varying(191) NOT NULL,
    link character varying(191) NOT NULL,
    datetime character varying(191) NOT NULL,
    "timestamp" bigint NOT NULL
);


ALTER TABLE public.app_google_scraper OWNER TO admin;

--
-- Name: app_google_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_google_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_google_scraper_id_seq OWNER TO admin;

--
-- Name: app_google_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_google_scraper_id_seq OWNED BY public.app_google_scraper.id;


--
-- Name: app_muabannet_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_muabannet_scraper (
    id integer NOT NULL,
    post_time bigint,
    post_author character varying(100),
    description text,
    price bigint,
    price_with_unit character varying(100),
    phone_number bigint,
    address text,
    location character varying(100),
    land_area double precision,
    bedroom integer,
    bathroom integer,
    floors integer,
    search_keywords character varying(100),
    type character varying(100),
    website character varying(191),
    url character varying(191) NOT NULL,
    updated_at character varying(191),
    post_title character varying(100),
    legal character varying(100)
);


ALTER TABLE public.app_muabannet_scraper OWNER TO admin;

--
-- Name: app_vieclamtot_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_vieclamtot_scraper (
    id integer NOT NULL,
    search_keyword character varying(191) NOT NULL,
    post_title text,
    post_author character varying(191),
    job_type character varying(191),
    full_description text,
    vacancies character varying(191),
    company_name text,
    phone character varying(20),
    salary_with_unit character varying(191),
    min_salary integer,
    max_salary integer,
    salary_type character varying(191),
    contract_type character varying(191),
    min_age integer,
    max_age integer,
    preferred_education text,
    preferred_gender text,
    preferred_working_experience text,
    skills text,
    benefits text,
    street_number character varying(191),
    ward text,
    district text,
    city text,
    address text,
    coordinate character varying(191),
    website character varying(191) NOT NULL,
    url character varying(191) NOT NULL,
    post_time bigint,
    updated_at character varying(191) NOT NULL,
    job_id integer,
    auto character varying(191) NOT NULL
);


ALTER TABLE public.app_vieclamtot_scraper OWNER TO admin;

--
-- Name: app_vieclamtot_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_vieclamtot_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_vieclamtot_scraper_id_seq OWNER TO admin;

--
-- Name: app_vieclamtot_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_vieclamtot_scraper_id_seq OWNED BY public.app_vieclamtot_scraper.id;


--
-- Name: app_vieclamtot_statistic; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.app_vieclamtot_statistic (
    id integer NOT NULL,
    crawled_at character varying(191) NOT NULL,
    builder integer NOT NULL,
    seller integer NOT NULL,
    driver integer NOT NULL,
    maid integer NOT NULL,
    restaurant_hotel integer NOT NULL,
    customer_care integer NOT NULL,
    guard integer NOT NULL,
    electrician integer NOT NULL,
    weaver integer NOT NULL,
    beauty_care integer NOT NULL,
    food_processor integer NOT NULL,
    assistant integer NOT NULL,
    mechanic integer NOT NULL,
    unskilled_labor integer NOT NULL,
    salesman integer NOT NULL,
    real_estate integer NOT NULL,
    worker integer NOT NULL,
    multi_industry integer NOT NULL,
    receptionist integer NOT NULL,
    chef_bartender integer NOT NULL,
    audit integer NOT NULL,
    metalist integer NOT NULL,
    carpenter integer NOT NULL,
    shipper integer NOT NULL
);


ALTER TABLE public.app_vieclamtot_statistic OWNER TO admin;

--
-- Name: app_vieclamtot_statistic_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.app_vieclamtot_statistic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_vieclamtot_statistic_id_seq OWNER TO admin;

--
-- Name: app_vieclamtot_statistic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.app_vieclamtot_statistic_id_seq OWNED BY public.app_vieclamtot_statistic.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO admin;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO admin;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: batdongsancom; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.batdongsancom (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    page integer NOT NULL,
    posted_at timestamp with time zone,
    expired_at timestamp with time zone,
    post_rank character varying(500),
    post_number character varying(15),
    price character varying(50),
    size character varying(50),
    house_type character varying(50),
    direction character varying(15),
    floors character varying(15),
    location character varying(150),
    balcony_direction character varying(15),
    bedrooms character varying(15),
    toilets character varying(15),
    furniture character varying(150),
    property_legal character varying(30),
    street_in character varying(15),
    street character varying(15),
    detail_header character varying(1000),
    title character varying(200),
    short_description character varying(200),
    description character varying(3500),
    tags character varying(1000),
    link character varying(500)
);


ALTER TABLE public.batdongsancom OWNER TO admin;

--
-- Name: batdongsancom_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.batdongsancom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.batdongsancom_id_seq OWNER TO admin;

--
-- Name: batdongsancom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.batdongsancom_id_seq OWNED BY public.batdongsancom.id;


--
-- Name: chotot; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.chotot (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    page integer NOT NULL,
    posted_at character varying(50) NOT NULL,
    format_posted_at timestamp with time zone,
    title character varying(200),
    price character varying(100),
    description character varying(3000) NOT NULL,
    user_type character varying(30),
    size character varying(50),
    direction character varying(50),
    property_legal character varying(50),
    pricem2 character varying(30),
    block character varying(200),
    land_type character varying(50),
    commercial_type character varying(50),
    house_type character varying(50),
    apartment_type character varying(50),
    length character varying(10),
    width character varying(10),
    bedrooms character varying(30),
    toilets character varying(30),
    living_size character varying(30),
    floors character varying(30),
    furniture character varying(100),
    tags character varying(1000),
    link character varying(500),
    json_data character varying(10000) NOT NULL
);


ALTER TABLE public.chotot OWNER TO admin;

--
-- Name: chotot_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.chotot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chotot_id_seq OWNER TO admin;

--
-- Name: chotot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.chotot_id_seq OWNED BY public.chotot.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- Name: estate_tags; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.estate_tags (
    id integer NOT NULL,
    _type character varying(30),
    content character varying(200),
    table_name character varying(100),
    post_id integer
);


ALTER TABLE public.estate_tags OWNER TO admin;

--
-- Name: estate_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.estate_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estate_tags_id_seq OWNER TO admin;

--
-- Name: estate_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.estate_tags_id_seq OWNED BY public.estate_tags.id;


--
-- Name: jobsfb_facebook_post_job_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.jobsfb_facebook_post_job_scraper (
    id integer NOT NULL,
    group_id character varying(191) NOT NULL,
    post_id character varying(191) NOT NULL,
    post_user_id character varying(191) NOT NULL,
    post_message text,
    post_image_link text,
    post_image_alt text,
    post_total_reactions bigint NOT NULL,
    post_total_comments bigint NOT NULL,
    post_total_shares bigint NOT NULL,
    "timestamp" double precision NOT NULL,
    created_at double precision NOT NULL,
    updated_at double precision NOT NULL
);


ALTER TABLE public.jobsfb_facebook_post_job_scraper OWNER TO admin;

--
-- Name: jobsfb_facebook_post_job_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.jobsfb_facebook_post_job_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobsfb_facebook_post_job_scraper_id_seq OWNER TO admin;

--
-- Name: jobsfb_facebook_post_job_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.jobsfb_facebook_post_job_scraper_id_seq OWNED BY public.jobsfb_facebook_post_job_scraper.id;


--
-- Name: jobsfb_facebook_user_profile_job_scraper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.jobsfb_facebook_user_profile_job_scraper (
    id integer NOT NULL,
    user_id_job bigint NOT NULL,
    user_name_job character varying(250) NOT NULL,
    name character varying(250) NOT NULL,
    work character varying(500) NOT NULL,
    education character varying(500) NOT NULL,
    friend_count integer,
    follower_count integer,
    following_count integer,
    cover_photo character varying(500),
    profile_picture character varying(500),
    created_at double precision NOT NULL,
    updated_at double precision NOT NULL,
    post_id character varying(191) NOT NULL,
    group_id character varying(191) NOT NULL
);


ALTER TABLE public.jobsfb_facebook_user_profile_job_scraper OWNER TO admin;

--
-- Name: jobsfb_facebook_user_profile_job_scraper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.jobsfb_facebook_user_profile_job_scraper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobsfb_facebook_user_profile_job_scraper_id_seq OWNER TO admin;

--
-- Name: jobsfb_facebook_user_profile_job_scraper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.jobsfb_facebook_user_profile_job_scraper_id_seq OWNED BY public.jobsfb_facebook_user_profile_job_scraper.id;


--
-- Name: muabannet; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.muabannet (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    page integer NOT NULL,
    posted_at timestamp with time zone,
    title character varying(200),
    location character varying(150),
    exact_location character varying(100),
    description character varying(3000) NOT NULL,
    price character varying(100),
    user_type character varying(100),
    property_name character varying(500),
    tags character varying(1000),
    direction character varying(100),
    bedrooms character varying(15),
    toilets character varying(15),
    floors character varying(15),
    living_size character varying(15),
    size character varying(15),
    property_legal character varying(50),
    link character varying(500)
);


ALTER TABLE public.muabannet OWNER TO admin;

--
-- Name: muabannet_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.muabannet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.muabannet_id_seq OWNER TO admin;

--
-- Name: muabannet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.muabannet_id_seq OWNED BY public.muabannet.id;


--
-- Name: app_facebook_comment_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_comment_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_facebook_comment_scraper_id_seq'::regclass);


--
-- Name: app_facebook_post_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_post_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_facebook_post_scraper_id_seq'::regclass);


--
-- Name: app_facebook_reaction_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_reaction_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_facebook_reaction_scraper_id_seq'::regclass);


--
-- Name: app_facebook_search_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_search_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_facebook_search_scraper_id_seq'::regclass);


--
-- Name: app_facebook_user_profile_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_user_profile_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_facebook_user_profile_scraper_id_seq'::regclass);


--
-- Name: app_facebook_user_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_user_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_facebook_user_scraper_id_seq'::regclass);


--
-- Name: app_google_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_google_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_google_scraper_id_seq'::regclass);


--
-- Name: app_vieclamtot_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_vieclamtot_scraper ALTER COLUMN id SET DEFAULT nextval('public.app_vieclamtot_scraper_id_seq'::regclass);


--
-- Name: app_vieclamtot_statistic id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_vieclamtot_statistic ALTER COLUMN id SET DEFAULT nextval('public.app_vieclamtot_statistic_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: batdongsancom id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.batdongsancom ALTER COLUMN id SET DEFAULT nextval('public.batdongsancom_id_seq'::regclass);


--
-- Name: chotot id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.chotot ALTER COLUMN id SET DEFAULT nextval('public.chotot_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: estate_tags id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.estate_tags ALTER COLUMN id SET DEFAULT nextval('public.estate_tags_id_seq'::regclass);


--
-- Name: jobsfb_facebook_post_job_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.jobsfb_facebook_post_job_scraper ALTER COLUMN id SET DEFAULT nextval('public.jobsfb_facebook_post_job_scraper_id_seq'::regclass);


--
-- Name: jobsfb_facebook_user_profile_job_scraper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.jobsfb_facebook_user_profile_job_scraper ALTER COLUMN id SET DEFAULT nextval('public.jobsfb_facebook_user_profile_job_scraper_id_seq'::regclass);


--
-- Name: muabannet id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.muabannet ALTER COLUMN id SET DEFAULT nextval('public.muabannet_id_seq'::regclass);


--
-- Name: app_ancu_scraper app_ancu_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_ancu_scraper
    ADD CONSTRAINT app_ancu_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_ancu_scraper app_ancu_scraper_url_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_ancu_scraper
    ADD CONSTRAINT app_ancu_scraper_url_key UNIQUE (url);


--
-- Name: app_dangbannhadat_scraper app_dangbannhadat_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_dangbannhadat_scraper
    ADD CONSTRAINT app_dangbannhadat_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_dangbannhadat_scraper app_dangbannhadat_scraper_url_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_dangbannhadat_scraper
    ADD CONSTRAINT app_dangbannhadat_scraper_url_key UNIQUE (url);


--
-- Name: app_facebook_comment_scraper app_facebook_comment_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_comment_scraper
    ADD CONSTRAINT app_facebook_comment_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_facebook_post_scraper app_facebook_post_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_post_scraper
    ADD CONSTRAINT app_facebook_post_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_facebook_reaction_scraper app_facebook_reaction_sc_post_user_id_post_id_a2a5e8af_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_reaction_scraper
    ADD CONSTRAINT app_facebook_reaction_sc_post_user_id_post_id_a2a5e8af_uniq UNIQUE (post_user_id, post_id);


--
-- Name: app_facebook_reaction_scraper app_facebook_reaction_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_reaction_scraper
    ADD CONSTRAINT app_facebook_reaction_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_facebook_search_scraper app_facebook_search_scraper_link_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_search_scraper
    ADD CONSTRAINT app_facebook_search_scraper_link_key UNIQUE (link);


--
-- Name: app_facebook_search_scraper app_facebook_search_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_search_scraper
    ADD CONSTRAINT app_facebook_search_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_facebook_user_profile_scraper app_facebook_user_profile_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_user_profile_scraper
    ADD CONSTRAINT app_facebook_user_profile_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_facebook_user_scraper app_facebook_user_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_user_scraper
    ADD CONSTRAINT app_facebook_user_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_facebook_user_scraper app_facebook_user_scraper_user_name_user_id_625222ed_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_user_scraper
    ADD CONSTRAINT app_facebook_user_scraper_user_name_user_id_625222ed_uniq UNIQUE (user_name, user_id);


--
-- Name: app_google_scraper app_google_scraper_link_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_google_scraper
    ADD CONSTRAINT app_google_scraper_link_key UNIQUE (link);


--
-- Name: app_google_scraper app_google_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_google_scraper
    ADD CONSTRAINT app_google_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_google_scraper app_google_scraper_title_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_google_scraper
    ADD CONSTRAINT app_google_scraper_title_key UNIQUE (title);


--
-- Name: app_muabannet_scraper app_muabannet_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_muabannet_scraper
    ADD CONSTRAINT app_muabannet_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_muabannet_scraper app_muabannet_scraper_url_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_muabannet_scraper
    ADD CONSTRAINT app_muabannet_scraper_url_key UNIQUE (url);


--
-- Name: app_vieclamtot_scraper app_vieclamtot_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_vieclamtot_scraper
    ADD CONSTRAINT app_vieclamtot_scraper_pkey PRIMARY KEY (id);


--
-- Name: app_vieclamtot_scraper app_vieclamtot_scraper_url_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_vieclamtot_scraper
    ADD CONSTRAINT app_vieclamtot_scraper_url_key UNIQUE (url);


--
-- Name: app_vieclamtot_statistic app_vieclamtot_statistic_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_vieclamtot_statistic
    ADD CONSTRAINT app_vieclamtot_statistic_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: batdongsancom batdongsancom_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.batdongsancom
    ADD CONSTRAINT batdongsancom_pkey PRIMARY KEY (id);


--
-- Name: chotot chotot_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.chotot
    ADD CONSTRAINT chotot_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: estate_tags estate_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.estate_tags
    ADD CONSTRAINT estate_tags_pkey PRIMARY KEY (id);


--
-- Name: app_facebook_user_profile_scraper facebook user id; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_user_profile_scraper
    ADD CONSTRAINT "facebook user id" UNIQUE (user_id);


--
-- Name: jobsfb_facebook_user_profile_job_scraper facebook user id job; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.jobsfb_facebook_user_profile_job_scraper
    ADD CONSTRAINT "facebook user id job" UNIQUE (user_id_job);


--
-- Name: app_facebook_user_profile_scraper facebook username; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.app_facebook_user_profile_scraper
    ADD CONSTRAINT "facebook username" UNIQUE (user_name);


--
-- Name: jobsfb_facebook_user_profile_job_scraper facebook username job; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.jobsfb_facebook_user_profile_job_scraper
    ADD CONSTRAINT "facebook username job" UNIQUE (user_name_job);


--
-- Name: jobsfb_facebook_post_job_scraper jobsfb_facebook_post_job_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.jobsfb_facebook_post_job_scraper
    ADD CONSTRAINT jobsfb_facebook_post_job_scraper_pkey PRIMARY KEY (id);


--
-- Name: jobsfb_facebook_user_profile_job_scraper jobsfb_facebook_user_profile_job_scraper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.jobsfb_facebook_user_profile_job_scraper
    ADD CONSTRAINT jobsfb_facebook_user_profile_job_scraper_pkey PRIMARY KEY (id);


--
-- Name: muabannet muabannet_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.muabannet
    ADD CONSTRAINT muabannet_pkey PRIMARY KEY (id);


--
-- Name: app_ancu_scraper_url_c49dde70_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_ancu_scraper_url_c49dde70_like ON public.app_ancu_scraper USING btree (url varchar_pattern_ops);


--
-- Name: app_dangbannhadat_scraper_url_d1077fae_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_dangbannhadat_scraper_url_d1077fae_like ON public.app_dangbannhadat_scraper USING btree (url varchar_pattern_ops);


--
-- Name: app_faceboo_keyword_044021_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_keyword_044021_idx ON public.app_facebook_search_scraper USING btree (keyword);


--
-- Name: app_faceboo_post_co_67cc48_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_post_co_67cc48_idx ON public.app_facebook_comment_scraper USING btree (post_comment_user_id);


--
-- Name: app_faceboo_post_co_d23bbd_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_post_co_d23bbd_idx ON public.app_facebook_user_scraper USING btree (post_comment_id);


--
-- Name: app_faceboo_post_id_33e8f5_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_post_id_33e8f5_idx ON public.app_facebook_comment_scraper USING btree (post_id);


--
-- Name: app_faceboo_post_id_cc2e84_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_post_id_cc2e84_idx ON public.app_facebook_user_scraper USING btree (post_id);


--
-- Name: app_faceboo_post_id_d13508_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_post_id_d13508_idx ON public.app_facebook_reaction_scraper USING btree (post_id);


--
-- Name: app_faceboo_post_us_fa0337_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_post_us_fa0337_idx ON public.app_facebook_reaction_scraper USING btree (post_user_id);


--
-- Name: app_faceboo_scrolls_f08cc3_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_scrolls_f08cc3_idx ON public.app_facebook_search_scraper USING btree (scrolls);


--
-- Name: app_faceboo_user_id_017736_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_user_id_017736_idx ON public.app_facebook_user_scraper USING btree (user_id);


--
-- Name: app_faceboo_user_na_57c180_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_faceboo_user_na_57c180_idx ON public.app_facebook_user_scraper USING btree (user_name);


--
-- Name: app_facebook_search_scraper_link_0a254b44_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_facebook_search_scraper_link_0a254b44_like ON public.app_facebook_search_scraper USING btree (link varchar_pattern_ops);


--
-- Name: app_google__crawled_25f614_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_google__crawled_25f614_idx ON public.app_google_scraper USING btree (crawled_page);


--
-- Name: app_google__keyword_610d90_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_google__keyword_610d90_idx ON public.app_google_scraper USING btree (keyword);


--
-- Name: app_google_scraper_link_f2b2d844_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_google_scraper_link_f2b2d844_like ON public.app_google_scraper USING btree (link varchar_pattern_ops);


--
-- Name: app_google_scraper_title_7a08bdc8_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_google_scraper_title_7a08bdc8_like ON public.app_google_scraper USING btree (title varchar_pattern_ops);


--
-- Name: app_muabannet_scraper_url_f23e1eff_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_muabannet_scraper_url_f23e1eff_like ON public.app_muabannet_scraper USING btree (url varchar_pattern_ops);


--
-- Name: app_vieclam_search__7d4a12_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_vieclam_search__7d4a12_idx ON public.app_vieclamtot_scraper USING btree (search_keyword);


--
-- Name: app_vieclamtot_scraper_url_e95d2620_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX app_vieclamtot_scraper_url_e95d2620_like ON public.app_vieclamtot_scraper USING btree (url varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Debian 14.4-1.pgdg110+1)
-- Dumped by pg_dump version 14.4 (Debian 14.4-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE postgres;
--
-- Name: postgres; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO admin;

\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

