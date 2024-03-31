--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1 (Debian 16.1-1.pgdg120+1)
-- Dumped by pg_dump version 16.1 (Debian 16.1-1.pgdg120+1)

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
-- Name: Users_models; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Users_models" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    image character varying(100) NOT NULL,
    file character varying(100) NOT NULL,
    id_user_id integer NOT NULL
);


ALTER TABLE public."Users_models" OWNER TO admin;

--
-- Name: Users_models_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Users_models_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_models_id_seq" OWNER TO admin;

--
-- Name: Users_models_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Users_models_id_seq" OWNED BY public."Users_models".id;


--
-- Name: Users_submodels; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Users_submodels" (
    id integer NOT NULL,
    id_model_id integer NOT NULL,
    file character varying(100) NOT NULL
);


ALTER TABLE public."Users_submodels" OWNER TO admin;

--
-- Name: Users_submodels_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Users_submodels_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_submodels_id_seq" OWNER TO admin;

--
-- Name: Users_submodels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Users_submodels_id_seq" OWNED BY public."Users_submodels".id;


--
-- Name: Users_users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Users_users" (
    id integer NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    name character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public."Users_users" OWNER TO admin;

--
-- Name: Users_users_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Users_users_groups" (
    id integer NOT NULL,
    users_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public."Users_users_groups" OWNER TO admin;

--
-- Name: Users_users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Users_users_groups_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_users_groups_id_seq" OWNER TO admin;

--
-- Name: Users_users_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Users_users_groups_id_seq" OWNED BY public."Users_users_groups".id;


--
-- Name: Users_users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Users_users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_users_id_seq" OWNER TO admin;

--
-- Name: Users_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Users_users_id_seq" OWNED BY public."Users_users".id;


--
-- Name: Users_users_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Users_users_user_permissions" (
    id integer NOT NULL,
    users_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public."Users_users_user_permissions" OWNER TO admin;

--
-- Name: Users_users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Users_users_user_permissions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_users_user_permissions_id_seq" OWNER TO admin;

--
-- Name: Users_users_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Users_users_user_permissions_id_seq" OWNED BY public."Users_users_user_permissions".id;


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


ALTER SEQUENCE public.auth_group_id_seq OWNER TO admin;

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


ALTER SEQUENCE public.auth_group_permissions_id_seq OWNER TO admin;

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


ALTER SEQUENCE public.auth_permission_id_seq OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


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


ALTER SEQUENCE public.django_admin_log_id_seq OWNER TO admin;

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


ALTER SEQUENCE public.django_content_type_id_seq OWNER TO admin;

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


ALTER SEQUENCE public.django_migrations_id_seq OWNER TO admin;

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
-- Name: otp_totp_totpdevice; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.otp_totp_totpdevice (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    confirmed boolean NOT NULL,
    key character varying(80) NOT NULL,
    step smallint NOT NULL,
    t0 bigint NOT NULL,
    digits smallint NOT NULL,
    tolerance smallint NOT NULL,
    drift smallint NOT NULL,
    last_t bigint NOT NULL,
    user_id integer NOT NULL,
    throttling_failure_count integer NOT NULL,
    throttling_failure_timestamp timestamp with time zone,
    CONSTRAINT otp_totp_totpdevice_digits_check CHECK ((digits >= 0)),
    CONSTRAINT otp_totp_totpdevice_step_check CHECK ((step >= 0)),
    CONSTRAINT otp_totp_totpdevice_throttling_failure_count_check CHECK ((throttling_failure_count >= 0)),
    CONSTRAINT otp_totp_totpdevice_tolerance_check CHECK ((tolerance >= 0))
);


ALTER TABLE public.otp_totp_totpdevice OWNER TO admin;

--
-- Name: otp_totp_totpdevice_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.otp_totp_totpdevice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.otp_totp_totpdevice_id_seq OWNER TO admin;

--
-- Name: otp_totp_totpdevice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.otp_totp_totpdevice_id_seq OWNED BY public.otp_totp_totpdevice.id;


--
-- Name: Users_models id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_models" ALTER COLUMN id SET DEFAULT nextval('public."Users_models_id_seq"'::regclass);


--
-- Name: Users_submodels id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_submodels" ALTER COLUMN id SET DEFAULT nextval('public."Users_submodels_id_seq"'::regclass);


--
-- Name: Users_users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users" ALTER COLUMN id SET DEFAULT nextval('public."Users_users_id_seq"'::regclass);


--
-- Name: Users_users_groups id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_groups" ALTER COLUMN id SET DEFAULT nextval('public."Users_users_groups_id_seq"'::regclass);


--
-- Name: Users_users_user_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_user_permissions" ALTER COLUMN id SET DEFAULT nextval('public."Users_users_user_permissions_id_seq"'::regclass);


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
-- Name: otp_totp_totpdevice id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.otp_totp_totpdevice ALTER COLUMN id SET DEFAULT nextval('public.otp_totp_totpdevice_id_seq'::regclass);


--
-- Data for Name: Users_models; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."Users_models" (id, name, image, file, id_user_id) FROM stdin;
\.


--
-- Data for Name: Users_submodels; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."Users_submodels" (id, id_model_id, file) FROM stdin;
\.


--
-- Data for Name: Users_users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."Users_users" (id, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, name, username, email, password) FROM stdin;
\.


--
-- Data for Name: Users_users_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."Users_users_groups" (id, users_id, group_id) FROM stdin;
\.


--
-- Data for Name: Users_users_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."Users_users_user_permissions" (id, users_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_users
22	Can change user	6	change_users
23	Can delete user	6	delete_users
24	Can view user	6	view_users
25	Can add models	7	add_models
26	Can change models	7	change_models
27	Can delete models	7	delete_models
28	Can view models	7	view_models
29	Can add sub models	8	add_submodels
30	Can change sub models	8	change_submodels
31	Can delete sub models	8	delete_submodels
32	Can view sub models	8	view_submodels
33	Can add TOTP device	9	add_totpdevice
34	Can change TOTP device	9	change_totpdevice
35	Can delete TOTP device	9	delete_totpdevice
36	Can view TOTP device	9	view_totpdevice
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	Users	users
7	Users	models
8	Users	submodels
9	otp_totp	totpdevice
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2023-11-08 13:36:10.270012+00
2	contenttypes	0002_remove_content_type_name	2023-11-08 13:36:10.291495+00
3	auth	0001_initial	2023-11-08 13:36:10.429777+00
4	auth	0002_alter_permission_name_max_length	2023-11-08 13:36:10.442794+00
5	auth	0003_alter_user_email_max_length	2023-11-08 13:36:10.457642+00
6	auth	0004_alter_user_username_opts	2023-11-08 13:36:10.476455+00
7	auth	0005_alter_user_last_login_null	2023-11-08 13:36:10.490985+00
8	auth	0006_require_contenttypes_0002	2023-11-08 13:36:10.499043+00
9	auth	0007_alter_validators_add_error_messages	2023-11-08 13:36:10.514114+00
10	auth	0008_alter_user_username_max_length	2023-11-08 13:36:10.52929+00
11	auth	0009_alter_user_last_name_max_length	2023-11-08 13:36:10.545454+00
12	auth	0010_alter_group_name_max_length	2023-11-08 13:36:10.563451+00
13	auth	0011_update_proxy_permissions	2023-11-08 13:36:10.578853+00
14	auth	0012_alter_user_first_name_max_length	2023-11-08 13:36:10.594419+00
15	Users	0001_initial	2023-11-08 13:36:10.796148+00
16	Users	0002_alter_users_password	2023-11-08 13:36:10.848534+00
17	admin	0001_initial	2023-11-08 13:36:10.921904+00
18	admin	0002_logentry_remove_auto_add	2023-11-08 13:36:10.94465+00
19	admin	0003_logentry_add_action_flag_choices	2023-11-08 13:36:10.963325+00
20	sessions	0001_initial	2023-11-08 13:36:11.023306+00
21	Users	0003_models	2023-12-26 19:44:34.377669+00
22	Users	0004_auto_20231126_1217	2023-12-26 19:44:34.454949+00
23	Users	0005_alter_models_file	2023-12-26 19:44:34.482476+00
24	Users	0006_submodels	2023-12-26 19:44:34.551201+00
25	Users	0007_submodels_file	2023-12-26 19:44:34.575403+00
26	Users	0008_alter_submodels_file	2023-12-26 19:44:34.594271+00
27	otp_totp	0001_initial	2023-12-26 19:44:34.648706+00
28	otp_totp	0002_auto_20190420_0723	2023-12-26 19:44:34.686097+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: otp_totp_totpdevice; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.otp_totp_totpdevice (id, name, confirmed, key, step, t0, digits, tolerance, drift, last_t, user_id, throttling_failure_count, throttling_failure_timestamp) FROM stdin;
\.


--
-- Name: Users_models_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public."Users_models_id_seq"', 93, true);


--
-- Name: Users_submodels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public."Users_submodels_id_seq"', 32, true);


--
-- Name: Users_users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public."Users_users_groups_id_seq"', 1, false);


--
-- Name: Users_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public."Users_users_id_seq"', 15, true);


--
-- Name: Users_users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public."Users_users_user_permissions_id_seq"', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 24, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 6, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);


--
-- Name: otp_totp_totpdevice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.otp_totp_totpdevice_id_seq', 1, false);


--
-- Name: Users_models Users_models_id_user_id_name_89f73558_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_models"
    ADD CONSTRAINT "Users_models_id_user_id_name_89f73558_uniq" UNIQUE (id_user_id, name);


--
-- Name: Users_models Users_models_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_models"
    ADD CONSTRAINT "Users_models_pkey" PRIMARY KEY (id);


--
-- Name: Users_submodels Users_submodels_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_submodels"
    ADD CONSTRAINT "Users_submodels_pkey" PRIMARY KEY (id);


--
-- Name: Users_users Users_users_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users"
    ADD CONSTRAINT "Users_users_email_key" UNIQUE (email);


--
-- Name: Users_users_groups Users_users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_groups"
    ADD CONSTRAINT "Users_users_groups_pkey" PRIMARY KEY (id);


--
-- Name: Users_users_groups Users_users_groups_users_id_group_id_7b8a1cd9_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_groups"
    ADD CONSTRAINT "Users_users_groups_users_id_group_id_7b8a1cd9_uniq" UNIQUE (users_id, group_id);


--
-- Name: Users_users Users_users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users"
    ADD CONSTRAINT "Users_users_pkey" PRIMARY KEY (id);


--
-- Name: Users_users_user_permissions Users_users_user_permiss_users_id_permission_id_828b73ce_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_user_permissions"
    ADD CONSTRAINT "Users_users_user_permiss_users_id_permission_id_828b73ce_uniq" UNIQUE (users_id, permission_id);


--
-- Name: Users_users_user_permissions Users_users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_user_permissions"
    ADD CONSTRAINT "Users_users_user_permissions_pkey" PRIMARY KEY (id);


--
-- Name: Users_users Users_users_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users"
    ADD CONSTRAINT "Users_users_username_key" UNIQUE (username);


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
-- Name: otp_totp_totpdevice otp_totp_totpdevice_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.otp_totp_totpdevice
    ADD CONSTRAINT otp_totp_totpdevice_pkey PRIMARY KEY (id);


--
-- Name: Users_models_id_user_id_1b35331f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_models_id_user_id_1b35331f" ON public."Users_models" USING btree (id_user_id);


--
-- Name: Users_submodels_id_model_id_f83e874d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_submodels_id_model_id_f83e874d" ON public."Users_submodels" USING btree (id_model_id);


--
-- Name: Users_users_email_983e4e0b_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_users_email_983e4e0b_like" ON public."Users_users" USING btree (email varchar_pattern_ops);


--
-- Name: Users_users_groups_group_id_5a0b88fb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_users_groups_group_id_5a0b88fb" ON public."Users_users_groups" USING btree (group_id);


--
-- Name: Users_users_groups_users_id_cd65c864; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_users_groups_users_id_cd65c864" ON public."Users_users_groups" USING btree (users_id);


--
-- Name: Users_users_user_permissions_permission_id_e9e8f9df; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_users_user_permissions_permission_id_e9e8f9df" ON public."Users_users_user_permissions" USING btree (permission_id);


--
-- Name: Users_users_user_permissions_users_id_a047c1bd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_users_user_permissions_users_id_a047c1bd" ON public."Users_users_user_permissions" USING btree (users_id);


--
-- Name: Users_users_username_754f0633_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "Users_users_username_754f0633_like" ON public."Users_users" USING btree (username varchar_pattern_ops);


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
-- Name: otp_totp_totpdevice_user_id_0fb18292; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX otp_totp_totpdevice_user_id_0fb18292 ON public.otp_totp_totpdevice USING btree (user_id);


--
-- Name: Users_models Users_models_id_user_id_1b35331f_fk_Users_users_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_models"
    ADD CONSTRAINT "Users_models_id_user_id_1b35331f_fk_Users_users_id" FOREIGN KEY (id_user_id) REFERENCES public."Users_users"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Users_submodels Users_submodels_id_model_id_f83e874d_fk_Users_models_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_submodels"
    ADD CONSTRAINT "Users_submodels_id_model_id_f83e874d_fk_Users_models_id" FOREIGN KEY (id_model_id) REFERENCES public."Users_models"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Users_users_groups Users_users_groups_group_id_5a0b88fb_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_groups"
    ADD CONSTRAINT "Users_users_groups_group_id_5a0b88fb_fk_auth_group_id" FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Users_users_groups Users_users_groups_users_id_cd65c864_fk_Users_users_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_groups"
    ADD CONSTRAINT "Users_users_groups_users_id_cd65c864_fk_Users_users_id" FOREIGN KEY (users_id) REFERENCES public."Users_users"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Users_users_user_permissions Users_users_user_per_permission_id_e9e8f9df_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_user_permissions"
    ADD CONSTRAINT "Users_users_user_per_permission_id_e9e8f9df_fk_auth_perm" FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: Users_users_user_permissions Users_users_user_per_users_id_a047c1bd_fk_Users_use; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users_users_user_permissions"
    ADD CONSTRAINT "Users_users_user_per_users_id_a047c1bd_fk_Users_use" FOREIGN KEY (users_id) REFERENCES public."Users_users"(id) DEFERRABLE INITIALLY DEFERRED;


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
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_Users_users_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT "django_admin_log_user_id_c564eba6_fk_Users_users_id" FOREIGN KEY (user_id) REFERENCES public."Users_users"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: otp_totp_totpdevice otp_totp_totpdevice_user_id_0fb18292_fk_Users_users_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.otp_totp_totpdevice
    ADD CONSTRAINT "otp_totp_totpdevice_user_id_0fb18292_fk_Users_users_id" FOREIGN KEY (user_id) REFERENCES public."Users_users"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

