--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.15
-- Dumped by pg_dump version 9.1.15
-- Started on 2015-03-02 01:50:40 CET

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 191 (class 3079 OID 11687)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2097 (class 0 OID 0)
-- Dependencies: 191
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 515 (class 1247 OID 16390)
-- Dependencies: 6 161
-- Name: color; Type: TYPE; Schema: public; Owner: axou
--

CREATE TYPE color AS (
	r smallint,
	g smallint,
	b smallint
);


ALTER TYPE public.color OWNER TO axou;

--
-- TOC entry 518 (class 1247 OID 16392)
-- Dependencies: 6
-- Name: enum_genre_client; Type: TYPE; Schema: public; Owner: axou
--

CREATE TYPE enum_genre_client AS ENUM (
    'théâtre',
    'troupe',
    'audio-visuel',
    'bar',
    'concert',
    'institution publique',
    'entreprise',
    'autre'
);


ALTER TYPE public.enum_genre_client OWNER TO axou;

--
-- TOC entry 205 (class 1255 OID 33061)
-- Dependencies: 592 6
-- Name: array_pop(anyarray, character varying); Type: FUNCTION; Schema: public; Owner: axou
--

CREATE FUNCTION array_pop(a anyarray, element character varying) RETURNS anyarray
    LANGUAGE plpgsql
    AS $$
DECLARE 
    result a%TYPE;
BEGIN
SELECT ARRAY(
    SELECT b.e FROM (SELECT unnest(a)) AS b(e) WHERE b.e <> element) INTO result;
RETURN result;
END;
$$;


ALTER FUNCTION public.array_pop(a anyarray, element character varying) OWNER TO axou;

--
-- TOC entry 203 (class 1255 OID 16409)
-- Dependencies: 6
-- Name: terre_dist(double precision, double precision, double precision, double precision); Type: FUNCTION; Schema: public; Owner: axou
--

CREATE FUNCTION terre_dist(_lat1 double precision, _lon1 double precision, _lat2 double precision, _lon2 double precision) RETURNS double precision
    LANGUAGE sql IMMUTABLE
    AS $_$
  select ACOS(SIN($1)*SIN($3)+COS($1)*COS($3)*COS($4-$2))*6371;
$_$;


ALTER FUNCTION public.terre_dist(_lat1 double precision, _lon1 double precision, _lat2 double precision, _lon2 double precision) OWNER TO axou;

--
-- TOC entry 204 (class 1255 OID 16410)
-- Dependencies: 6
-- Name: terre_dist_plus(double precision, double precision, double precision, double precision); Type: FUNCTION; Schema: public; Owner: axou
--

CREATE FUNCTION terre_dist_plus(_lat1 double precision, _lon1 double precision, _lat2 double precision, _lon2 double precision) RETURNS double precision
    LANGUAGE sql IMMUTABLE
    AS $_$
  select 2*6378.137*ASIN(SQRT(ABS(POW(SIN(ABS($3-$1)/2),2)+COS($2)*COS($4)*POW(SIN(ABS($4-$2)/2),2))));
$_$;


ALTER FUNCTION public.terre_dist_plus(_lat1 double precision, _lon1 double precision, _lat2 double precision, _lon2 double precision) OWNER TO axou;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 162 (class 1259 OID 16411)
-- Dependencies: 6
-- Name: adresses_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE adresses_tb (
    dbid integer NOT NULL,
    adresse character varying,
    dbid_cp_ville integer,
    principale smallint,
    longitude double precision,
    latitude double precision,
    hauteur double precision,
    dbid_lieu integer
);


ALTER TABLE public.adresses_tb OWNER TO axou;

--
-- TOC entry 163 (class 1259 OID 16417)
-- Dependencies: 6 162
-- Name: adresses_tb_id_adresse_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE adresses_tb_id_adresse_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.adresses_tb_id_adresse_seq OWNER TO axou;

--
-- TOC entry 2098 (class 0 OID 0)
-- Dependencies: 163
-- Name: adresses_tb_id_adresse_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE adresses_tb_id_adresse_seq OWNED BY adresses_tb.dbid;


--
-- TOC entry 164 (class 1259 OID 16419)
-- Dependencies: 6
-- Name: id_client_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE id_client_seq
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.id_client_seq OWNER TO axou;

--
-- TOC entry 165 (class 1259 OID 16421)
-- Dependencies: 1898 1899 515 6
-- Name: clients_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE clients_tb (
    dbid integer DEFAULT nextval('id_client_seq'::regclass) NOT NULL,
    nom character varying(50) DEFAULT 'Nouveau client'::character varying,
    surnom character varying(10),
    dbid_lieu integer,
    dbid_genre integer,
    color color
);


ALTER TABLE public.clients_tb OWNER TO axou;

--
-- TOC entry 166 (class 1259 OID 16429)
-- Dependencies: 6
-- Name: id_contrat_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE id_contrat_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.id_contrat_seq OWNER TO axou;

--
-- TOC entry 167 (class 1259 OID 16431)
-- Dependencies: 1900 6
-- Name: contrats_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE contrats_tb (
    dbid integer DEFAULT nextval('id_contrat_seq'::regclass) NOT NULL,
    dbid_client integer,
    date_ouverture date,
    date_cloture date,
    dbid_tournee integer,
    date_debut_prestation date,
    date_fin_prestation date,
    num integer,
    remise integer,
    dbid_genre smallint
);


ALTER TABLE public.contrats_tb OWNER TO axou;

--
-- TOC entry 168 (class 1259 OID 16435)
-- Dependencies: 6
-- Name: cp_villes_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE cp_villes_tb (
    dbid integer NOT NULL,
    cp integer,
    ville character varying
);


ALTER TABLE public.cp_villes_tb OWNER TO axou;

--
-- TOC entry 169 (class 1259 OID 16441)
-- Dependencies: 6
-- Name: depots_lieux_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE depots_lieux_tb (
    dbid_depot integer NOT NULL,
    dbid_lieu integer NOT NULL,
    quantite integer,
    destinataire character varying
);


ALTER TABLE public.depots_lieux_tb OWNER TO axou;

--
-- TOC entry 170 (class 1259 OID 16447)
-- Dependencies: 6
-- Name: id_depot_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE id_depot_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.id_depot_seq OWNER TO axou;

--
-- TOC entry 171 (class 1259 OID 16449)
-- Dependencies: 1902 6
-- Name: depots_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE depots_tb (
    dbid integer DEFAULT nextval('id_depot_seq'::regclass) NOT NULL,
    nom character varying,
    surnom character varying,
    volume real,
    poid integer,
    prix_unite real,
    dbid_genre integer,
    dbid_contrat integer,
    nb_paquet integer,
    nb_carton integer,
    quantite integer,
    remarque character varying
);


ALTER TABLE public.depots_tb OWNER TO axou;

--
-- TOC entry 2099 (class 0 OID 0)
-- Dependencies: 171
-- Name: COLUMN depots_tb.prix_unite; Type: COMMENT; Schema: public; Owner: axou
--

COMMENT ON COLUMN depots_tb.prix_unite IS 'prix d''un tas';


--
-- TOC entry 172 (class 1259 OID 16456)
-- Dependencies: 6
-- Name: etatslieux_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE etatslieux_tb (
    dbid integer NOT NULL,
    etat character varying
);


ALTER TABLE public.etatslieux_tb OWNER TO axou;

--
-- TOC entry 173 (class 1259 OID 16462)
-- Dependencies: 6 172
-- Name: etatslieux_tb_id_etatlieu_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE etatslieux_tb_id_etatlieu_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.etatslieux_tb_id_etatlieu_seq OWNER TO axou;

--
-- TOC entry 2100 (class 0 OID 0)
-- Dependencies: 173
-- Name: etatslieux_tb_id_etatlieu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE etatslieux_tb_id_etatlieu_seq OWNED BY etatslieux_tb.dbid;


--
-- TOC entry 174 (class 1259 OID 16464)
-- Dependencies: 6
-- Name: id_genre_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE id_genre_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.id_genre_seq OWNER TO axou;

--
-- TOC entry 175 (class 1259 OID 16466)
-- Dependencies: 1904 6
-- Name: genresclients_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE genresclients_tb (
    dbid integer DEFAULT nextval('id_genre_seq'::regclass) NOT NULL,
    genre character(50)
);


ALTER TABLE public.genresclients_tb OWNER TO axou;

--
-- TOC entry 176 (class 1259 OID 16470)
-- Dependencies: 6
-- Name: genrescontrats_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE genrescontrats_tb (
    dbid integer NOT NULL,
    genre character varying
);


ALTER TABLE public.genrescontrats_tb OWNER TO axou;

--
-- TOC entry 177 (class 1259 OID 16476)
-- Dependencies: 176 6
-- Name: genrescontrats_tb_dbid_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE genrescontrats_tb_dbid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genrescontrats_tb_dbid_seq OWNER TO axou;

--
-- TOC entry 2101 (class 0 OID 0)
-- Dependencies: 177
-- Name: genrescontrats_tb_dbid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE genrescontrats_tb_dbid_seq OWNED BY genrescontrats_tb.dbid;


--
-- TOC entry 178 (class 1259 OID 16478)
-- Dependencies: 6
-- Name: genresdepots_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE genresdepots_tb (
    dbid integer NOT NULL,
    genre character varying
);


ALTER TABLE public.genresdepots_tb OWNER TO axou;

--
-- TOC entry 179 (class 1259 OID 16484)
-- Dependencies: 178 6
-- Name: genresdepots_tb_id_genre_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE genresdepots_tb_id_genre_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genresdepots_tb_id_genre_seq OWNER TO axou;

--
-- TOC entry 2102 (class 0 OID 0)
-- Dependencies: 179
-- Name: genresdepots_tb_id_genre_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE genresdepots_tb_id_genre_seq OWNED BY genresdepots_tb.dbid;


--
-- TOC entry 180 (class 1259 OID 16486)
-- Dependencies: 6
-- Name: genreslieux_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE genreslieux_tb (
    dbid integer NOT NULL,
    genre character varying
);


ALTER TABLE public.genreslieux_tb OWNER TO axou;

--
-- TOC entry 181 (class 1259 OID 16492)
-- Dependencies: 6 180
-- Name: genreslieux_tb_id_genre_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE genreslieux_tb_id_genre_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genreslieux_tb_id_genre_seq OWNER TO axou;

--
-- TOC entry 2103 (class 0 OID 0)
-- Dependencies: 181
-- Name: genreslieux_tb_id_genre_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE genreslieux_tb_id_genre_seq OWNED BY genreslieux_tb.dbid;


--
-- TOC entry 182 (class 1259 OID 16494)
-- Dependencies: 6
-- Name: lieux_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE lieux_tb (
    dbid integer NOT NULL,
    nom character varying,
    dbid_genre integer,
    dbid_etat integer,
    pertinence integer,
    commentaire character varying,
    saturation_max integer
);


ALTER TABLE public.lieux_tb OWNER TO axou;

--
-- TOC entry 183 (class 1259 OID 16500)
-- Dependencies: 182 6
-- Name: id_lieu_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE id_lieu_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.id_lieu_seq OWNER TO axou;

--
-- TOC entry 2104 (class 0 OID 0)
-- Dependencies: 183
-- Name: id_lieu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE id_lieu_seq OWNED BY lieux_tb.dbid;


--
-- TOC entry 184 (class 1259 OID 16502)
-- Dependencies: 168 6
-- Name: localites_tb_id_localite_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE localites_tb_id_localite_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.localites_tb_id_localite_seq OWNER TO axou;

--
-- TOC entry 2105 (class 0 OID 0)
-- Dependencies: 184
-- Name: localites_tb_id_localite_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE localites_tb_id_localite_seq OWNED BY cp_villes_tb.dbid;


--
-- TOC entry 188 (class 1259 OID 16677)
-- Dependencies: 1911 1912 1913 6
-- Name: parcours_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE parcours_tb (
    dbid integer NOT NULL,
    dbid_tournee integer,
    dbid_pedaleur integer,
    list_dbid_lieu integer[] DEFAULT '{}'::integer[],
    polygon polygon DEFAULT '((2.2923,48.8577999999999975),(2.29510000000000014,48.8596000000000004),(2.29689999999999994,48.8564999999999969))'::polygon,
    line integer[] DEFAULT '{}'::integer[]
);


ALTER TABLE public.parcours_tb OWNER TO axou;

--
-- TOC entry 187 (class 1259 OID 16675)
-- Dependencies: 6 188
-- Name: parcours_tb_dbid_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE parcours_tb_dbid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parcours_tb_dbid_seq OWNER TO axou;

--
-- TOC entry 2106 (class 0 OID 0)
-- Dependencies: 187
-- Name: parcours_tb_dbid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE parcours_tb_dbid_seq OWNED BY parcours_tb.dbid;


--
-- TOC entry 190 (class 1259 OID 16731)
-- Dependencies: 1914 6
-- Name: pedaleurs_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE pedaleurs_tb (
    dbid integer NOT NULL,
    nom character varying,
    prenom character varying,
    surnom character varying,
    dbid_lieu integer,
    couleur character varying DEFAULT '#ffffff'::character varying
);


ALTER TABLE public.pedaleurs_tb OWNER TO axou;

--
-- TOC entry 189 (class 1259 OID 16729)
-- Dependencies: 190 6
-- Name: pedaleurs_tb_dbid_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE pedaleurs_tb_dbid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pedaleurs_tb_dbid_seq OWNER TO axou;

--
-- TOC entry 2107 (class 0 OID 0)
-- Dependencies: 189
-- Name: pedaleurs_tb_dbid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE pedaleurs_tb_dbid_seq OWNED BY pedaleurs_tb.dbid;


--
-- TOC entry 185 (class 1259 OID 16504)
-- Dependencies: 6
-- Name: tournees_tb; Type: TABLE; Schema: public; Owner: axou; Tablespace: 
--

CREATE TABLE tournees_tb (
    dbid integer NOT NULL,
    date_ouverture date,
    date_cloture date
);


ALTER TABLE public.tournees_tb OWNER TO axou;

--
-- TOC entry 186 (class 1259 OID 16507)
-- Dependencies: 185 6
-- Name: tournees_tb_dbid_seq; Type: SEQUENCE; Schema: public; Owner: axou
--

CREATE SEQUENCE tournees_tb_dbid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tournees_tb_dbid_seq OWNER TO axou;

--
-- TOC entry 2108 (class 0 OID 0)
-- Dependencies: 186
-- Name: tournees_tb_dbid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: axou
--

ALTER SEQUENCE tournees_tb_dbid_seq OWNED BY tournees_tb.dbid;


--
-- TOC entry 1897 (class 2604 OID 16601)
-- Dependencies: 163 162
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY adresses_tb ALTER COLUMN dbid SET DEFAULT nextval('adresses_tb_id_adresse_seq'::regclass);


--
-- TOC entry 1901 (class 2604 OID 16602)
-- Dependencies: 184 168
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY cp_villes_tb ALTER COLUMN dbid SET DEFAULT nextval('localites_tb_id_localite_seq'::regclass);


--
-- TOC entry 1903 (class 2604 OID 16603)
-- Dependencies: 173 172
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY etatslieux_tb ALTER COLUMN dbid SET DEFAULT nextval('etatslieux_tb_id_etatlieu_seq'::regclass);


--
-- TOC entry 1905 (class 2604 OID 16604)
-- Dependencies: 177 176
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY genrescontrats_tb ALTER COLUMN dbid SET DEFAULT nextval('genrescontrats_tb_dbid_seq'::regclass);


--
-- TOC entry 1906 (class 2604 OID 16605)
-- Dependencies: 179 178
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY genresdepots_tb ALTER COLUMN dbid SET DEFAULT nextval('genresdepots_tb_id_genre_seq'::regclass);


--
-- TOC entry 1907 (class 2604 OID 16606)
-- Dependencies: 181 180
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY genreslieux_tb ALTER COLUMN dbid SET DEFAULT nextval('genreslieux_tb_id_genre_seq'::regclass);


--
-- TOC entry 1908 (class 2604 OID 16607)
-- Dependencies: 183 182
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY lieux_tb ALTER COLUMN dbid SET DEFAULT nextval('id_lieu_seq'::regclass);


--
-- TOC entry 1910 (class 2604 OID 16680)
-- Dependencies: 188 187 188
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY parcours_tb ALTER COLUMN dbid SET DEFAULT nextval('parcours_tb_dbid_seq'::regclass);


--
-- TOC entry 1915 (class 2604 OID 16734)
-- Dependencies: 189 190 190
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY pedaleurs_tb ALTER COLUMN dbid SET DEFAULT nextval('pedaleurs_tb_dbid_seq'::regclass);


--
-- TOC entry 1909 (class 2604 OID 16608)
-- Dependencies: 186 185
-- Name: dbid; Type: DEFAULT; Schema: public; Owner: axou
--

ALTER TABLE ONLY tournees_tb ALTER COLUMN dbid SET DEFAULT nextval('tournees_tb_dbid_seq'::regclass);


--
-- TOC entry 2061 (class 0 OID 16411)
-- Dependencies: 162 2090
-- Data for Name: adresses_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY adresses_tb (dbid, adresse, dbid_cp_ville, principale, longitude, latitude, hauteur, dbid_lieu) FROM stdin;
462	9 Rue de la Montagne d'Aulas	32581	1	2.27890099999999984	48.8404230000000013	0	631
463	66 Avenue de la Porte de Montmartre	32584	1	2.33552360000000014	48.9005349999999979	0	632
397	94 Avenue Gambetta	32586	1	2.40349799999999991	48.8704651999999982	0	566
401	 	32567	1	2.34585599999999994	48.8623469999999998	0	570
661	Adresse inconnue	11678	1	0	0	0	833
709	84 Rue Oberkampf	32577	1	2.37633770000000011	48.8653795000000031	0	894
388	7 Rue Ballu	32575	1	2.33088870000000004	48.8815809999999971	0	557
389	9 Rue Ballu	32575	1	2.33066189999999995	48.8815814000000017	0	558
392	6 Rue Eugène Oudiné	32579	1	2.37578500000000004	48.8259559999999979	0	561
394	72 Boulevard de Rochechouart	32584	1	2.34372239999999987	48.8829464000000016	0	563
395	221 Rue de Belleville	32586	1	2.39536140000000008	48.8752710999999991	0	564
396	44 Rue Alphonse Penaud	32586	1	2.4059689999999998	48.868898999999999	0	565
399	14 Rue Courat	32586	1	2.40540989999999999	48.8572415000000007	0	568
402	5 Rue Perrée	32569	1	2.36230129999999994	48.8640521000000021	0	571
464	213 Rue Saint-Honoré	32567	1	2.3309069	48.8653635000000008	0	633
465	4 Rue du Bouloi	32567	1	2.34001400000000004	48.8632014000000012	0	634
390	51 Rue du Faubourg-Saint-Denis	32576	1	2.35368850000000007	48.8718294000000029	0	559
398	22 Rue du Soleillet	32586	1	2.39261819999999981	48.865577799999997	0	567
400	72 Rue Stendhal	32586	1	2.4001427999999998	48.8631439999999984	0	569
403	12 Rue Censier	32571	1	2.35468339999999987	48.8409412000000032	0	572
404	48 Rue du Cardinal Lemoine	32571	1	2.35161569999999998	48.8466106999999994	0	573
405	9 Place Saint-Michel	32572	1	2.34375849999999986	48.8534712000000013	0	574
406	208 Rue du Faubourg Saint-Honoré	32574	1	2.30472250000000001	48.8752781999999968	0	575
409	11 Rue de Lancry	32576	1	2.36010799999999987	48.8693870000000032	0	578
410	31 Rue du Château Landon	32576	1	2.36381400000000008	48.8832165000000032	0	579
411	6 Rue Boy-Zelensky	32576	1	2.3679174999999999	48.8767017999999993	0	580
412	107 Rue du Faubourg-Saint-Denis	32576	1	2.3558694	48.8751303000000021	0	581
413	116 Quai de Jemmapes	32576	1	2.36369819999999997	48.8748946999999987	0	582
414	4 Rue Mercœur	32577	1	2.38322870000000009	48.8569014999999993	0	583
415	43 Rue de l'Orillon	32577	1	2.37756180000000006	48.8705897999999976	0	584
416	6 Avenue Maurice Ravel	32578	1	2.41156639999999989	48.8415527000000012	0	585
417	36 Quai de la Rapée	32578	1	2.37178939999999994	48.8427053999999998	0	586
418	91 Rue Claude Decaen	32578	1	2.39624389999999998	48.838577800000003	0	587
419	1 Rue Gouthière	32579	1	2.35104809999999986	48.8205335000000034	0	588
420	12 Rue du Docteur Charles Richet	32579	1	2.36401100000000008	48.8319242000000031	0	589
422	6 Rue Simone Weil	32579	1	2.36393010000000015	48.8235097999999965	0	591
423	61 Rue Dunois	32579	1	2.36633490000000002	48.8331025999999966	0	592
424	15 Rue de la Fontaine à Mulard	32579	1	2.34938599999999997	48.8232058999999978	0	593
425	23 Rue de Campo-Formio	32579	1	2.35922369999999981	48.8350113999999991	0	594
426	3 Avenue Joseph Bédier	32579	1	2.37359959999999992	48.8206941999999984	0	595
427	11 Rue Caillaux	32579	1	2.36126520000000006	48.8226782999999998	0	596
429	183 Rue Vercingétorix	32580	1	2.30928969999999989	48.831423700000002	0	598
430	18 Avenue de la Porte Brancion	32581	1	2.30038890000000018	48.8266769999999966	0	599
431	36 Rue du Colonel Pierre Avia	32581	1	2.27374579999999993	48.8289979999999986	0	600
432	20 Rue Georges Duhamel	32581	1	2.3118675999999998	48.8356427000000011	0	601
433	40 Rue Didot	32580	1	2.3198430000000001	48.8315186000000026	0	602
435	11 Rue Jean de la Fontaine	32582	1	2.27463609999999994	48.8521963000000028	0	604
436	1 Rue du Général Malleterre	32582	1	2.26342370000000015	48.8374268000000029	0	605
437	88 Rue de la Jonquière	32583	1	2.31915499999999986	48.8947330000000022	0	606
438	3 Rue Louis Loucheur	32583	1	2.32567389999999996	48.8980843000000007	0	607
440	27 Rue Marguerite Long	32583	1	2.30255039999999989	48.8923587000000026	0	609
443	5 Rue Henri Brisson	32584	1	2.33477850000000009	48.8983921000000024	0	612
446	26 Rue Clavel	32585	1	2.38377110000000014	48.8764447000000004	0	615
447	90 Rue Curial	32585	1	2.37538589999999994	48.8956662000000009	0	616
448	15 Rue Mathis	32585	1	2.37489879999999998	48.8908421000000004	0	617
449	36 Rue Rebeval	32585	1	2.37822040000000001	48.8744305000000026	0	618
450	135 Boulevard Sérurier	32585	1	2.39454250000000002	48.8845311999999979	0	619
451	4 Rue des Lilas	32585	1	2.39577600000000013	48.8781020999999996	0	620
452	17 Rue Jules Romains	32585	1	2.37764180000000014	48.8737966999999998	0	621
453	110 Rue des Amandiers	32586	1	2.38874830000000005	48.8679580000000016	0	622
454	48 Rue Louis Lumière	32586	1	2.41122360000000002	48.8606861000000023	0	623
455	1 Rue Pauline Kergomard	32586	1	2.40760949999999996	48.854951100000001	0	624
456	39 Rue Joseph Python	32586	1	2.41257520000000003	48.8641038000000023	0	625
457	46 Rue Louis Lumière	32586	1	2.41136600000000012	48.8606616000000002	0	626
458	93 Boulevard Davout	32586	1	2.41009759999999984	48.8550804999999997	0	627
459	12 Rue Faidherbe	32577	1	2.38425079999999978	48.8511804999999981	0	628
460	74 Rue Jean-Pierre Timbaud	32577	1	2.37589370000000022	48.8672699999999978	0	629
442	66 Rue René Binet	32584	1	2.33629579999999981	48.8991469999999993	0	611
439	47 Rue de Saussure	32583	1	2.31498479999999995	48.8851602000000014	0	608
444	 	32584	1	0.980793000000000026	44.4324119999999994	0	613
470	3 Rue Papin	32568	1	2.35400410000000004	48.866837799999999	0	639
466	51 Rue de Bercy	32578	1	2.38256099999999993	48.8373160000000013	0	635
468	60 Rue Réaumur	32569	1	2.35548100000000016	48.8658420000000007	0	637
469	79 Rue du Temple	32569	1	2.35613390000000011	48.8613484999999983	0	638
471	12 Rue Saint-Gilles	32569	1	2.36663649999999981	48.8578720000000004	0	640
472	10 Rue Charlot	32569	1	2.36081489999999983	48.8613518000000013	0	641
473	108 Rue Vieille du Temple	32569	1	2.36293560000000014	48.8611024	0	642
474	9 Rue de Thorigny	32569	1	2.36310129999999985	48.8599545000000006	0	643
475	48 Rue de Montmorency	32569	1	2.35312790000000005	48.8636370999999983	0	644
391	68 Rue de la Folie Méricourt	32577	1	2.37085180000000006	48.8652263000000033	0	560
393	12 rue d'Alésia	32580	1	2.32308450000000022	48.8893780000000007	0	562
387	49 Rue le Peletier	32575	1	2.33963719999999986	48.8755305999999976	0	556
407	24 Rue de Rochechouart	32575	0	2.34493539999999978	48.8781135999999989	0	576
476	11 Rue Payenne	32570	1	2.36239290000000013	48.8582516999999967	0	645
477	19 Rue de Saintonge	32569	1	2.36247879999999988	48.8617776000000035	0	646
478	108 Rue Vieille du Temple	32569	1	2.36293560000000014	48.8611024	0	647
479	108 Rue Vieille du Temple	32569	1	2.36293560000000014	48.8611024	0	648
480	7 Rue Debelleyme	32569	1	2.36358049999999986	48.8608109999999982	0	649
481	17 Rue des Filles du Calvaire	32569	1	2.36603379999999985	48.8628199999999993	0	650
482	5 Rue Sainte-Anastase	32569	1	2.36413999999999991	48.859595800000001	0	651
483	42 Rue de Turenne	32569	1	2.36460479999999995	48.8577524000000025	0	652
484	16 Rue du Perche	32569	1	2.36082269999999994	48.8611688000000015	0	653
535	23 Rue Boyer	32586	1	2.39213029999999982	48.8686811000000034	0	704
467	182 Rue Saint-Honoré	32567	1	2.33889769999999997	48.8625095000000016	0	636
434	  vvvvv	32580	1	0.980793000000000026	44.4324119999999994	0	603
445	119 Rue du Mont Cenis	32584	1	2.34603470000000014	48.8956080000000028	0	614
461	10 Avenue de la Porte de Montmartre	32584	1	2.33689789999999986	48.8987593000000018	0	630
441	12 Rue des Fillettes	32584	1	2.36328769999999988	48.8942716000000033	0	610
428	20 Avenue Marc Sangnier	32580	1	2.30651040000000007	48.8262507000000028	0	597
534	21 Rue Boyer	32586	1	2.39216939999999978	48.8685849000000019	0	703
408	60 Rue la Fayette	32575	1	2.34272159999999996	48.8755578000000028	0	577
533	104 Rue d'Aubervilliers	32585	1	2.36849100000000012	48.8904515999999987	0	702
673	16 Cité Bauer	32580	1	2.31890470000000004	48.8321927000000002	0	863
485	3 Rue des Arquebusiers	32569	1	2.36692370000000007	48.859115199999998	0	654
486	20 Rue Dupetit-Thouars	32569	1	2.36125529999999983	48.8657713999999999	0	655
488	44 Rue Quincampoix	32570	1	2.3505269000000002	48.8609435999999988	0	657
489	3 Rue du Cloître Saint-Merri	32570	1	2.35171840000000021	48.8588700999999972	0	658
490	82 Rue François Miron	32570	1	2.35937460000000021	48.8553469000000007	0	659
491	1 Rue des Fossés Saint-Bernard	32571	1	2.35548229999999981	48.8492670999999987	0	660
493	 Rue Corneille	32572	1	2.33905940000000001	48.8492850000000018	0	662
495	13 Rue de l'Abbaye	32572	1	2.33436870000000019	48.8543062000000035	0	664
496	6 Rue Jacques Callot	32572	1	2.33751979999999993	48.8552874000000017	0	665
497	60 Rue Mazarine	32572	1	2.33803219999999978	48.8543562999999992	0	666
498	5 Rue de Constantine	32573	1	2.31505219999999978	48.8605285000000009	0	667
499	39 Boulevard de la Tour-Maubourg	32573	1	2.31038159999999992	48.8590615999999969	0	668
500	30 Avenue Marceau	32574	1	2.29882860000000022	48.8692151999999993	0	669
501	1 Place de la Concorde	32574	1	2.32339859999999998	48.8662564999999987	0	670
502	12 Rue Boissy d'Anglas	32574	1	2.32156429999999991	48.8684070999999989	0	671
505	59 Rue Condorcet	32575	1	2.34197819999999979	48.8802828000000034	0	674
506	16 Rue Chaptal	32575	1	2.33344769999999979	48.8810987999999966	0	675
507	58 Rue Saint-Lazare	32575	1	2.3336538	48.8769159000000002	0	676
508	40 Boulevard Haussmann	32575	1	2.33213200000000009	48.8734409999999997	0	677
509	11 Boulevard de Magenta	32576	1	2.36147820000000008	48.8700363000000024	0	678
510	2 Rue de Marseille	32576	1	2.36318420000000007	48.871352899999998	0	679
513	64 Rue Jean-Pierre Timbaud	32577	1	2.37442090000000006	48.8669001000000023	0	682
514	78 Rue Amelot	32577	1	2.36799090000000012	48.8605731999999975	0	683
516	10 Boulevard de la Bastille	32578	1	2.36750879999999997	48.8473479999999967	0	685
518	 Esplanade Pierre Vidal-Naquet	32579	1	2.38248989999999994	48.8300721000000024	0	687
519	7 Rue Francis de Pressensé	32580	1	2.31655480000000003	48.8339719000000017	0	688
520	261 Boulevard Raspail	32580	1	2.33168620000000004	48.8371775999999969	0	689
521	2 Impasse Lebouis	32580	1	2.32166320000000015	48.8367441999999983	0	690
522	11 Avenue du Président Wilson	38966	1	2.29890000000000017	48.8651309999999981	0	691
523	3 Avenue du Président Wilson	38966	1	2.299763	48.8648032999999984	0	692
524	75 Rue des Martyrs	32584	1	2.33961409999999992	48.882421800000003	0	693
525	21 Rue des 3 Frères	32584	1	2.34107969999999987	48.8844933000000026	0	694
527	2 Rue Ronsard	32584	1	2.34422100000000011	48.8848659000000012	0	696
532	 Villa Marcel Lods	32585	1	2.37713369999999991	48.8753699000000026	0	701
494	14 Rue Bonaparte	32572	1	2.33461819999999998	48.8566076999999979	0	663
512	200 Quai de Valmy	32576	1	2.36814079999999993	48.8812280000000001	0	681
511	72 Rue du Faubourg Saint-Martin	32576	1	2.35723530000000014	48.8717490000000012	0	680
528	6 Rue Francoeur	32584	1	2.34265070000000009	48.8900386999999981	0	697
492	31, rue d'Ulm	32571	1	0	0	0	661
503	28, place de la Madeleine	32574	1	0	0	0	672
504	5 avenue Vélasquez	32574	1	0	0	0	673
515	94, rue Jean-Pierre Timbaud	32577	1	0	0	0	684
526	80 boulevard Rochechouart	32584	1	0	0	0	695
530	211 Avenue Jean Jaurès	32585	1	2.39443200000000012	48.8890923000000015	0	699
487	32 Rue des Francs-Bourgeois	32570	1	2.35975460000000004	48.8581800999999984	0	656
531	33 Rue des Alouettes	32585	1	2.3855461	48.8780535	0	700
529	23 Rue Léon	32584	1	2.3534953999999999	48.8880059000000031	0	698
517	51 Rue de Bercy	32578	1	2.38272240000000002	48.8372024999999965	0	686
553	 	38966	1	0.980793000000000026	44.4324119999999994	0	722
557	 	38966	1	0.980793000000000026	44.4324119999999994	0	726
569	 	38966	1	0.980793000000000026	44.4324119999999994	0	738
601	13 Rue Henry Monnier	32575	1	2.3371761000000002	48.8798510000000022	0	770
554	39, rue de Bretagne	32569	1	0	0	0	723
575	2, place Baudoyer	32570	1	0	0	0	744
586	63, Bd St Marcel	32571	1	0	0	0	755
587	76, rue Monge	32571	1	0	0	0	756
597	5, rue de Montfaucon	32572	1	0	0	0	766
572	14 Rue François Miron	32570	1	2.35545690000000008	48.8558984000000009	0	741
594	19 Rue de l'Odéon	32572	1	2.33872539999999995	48.850204699999999	0	763
556	22 Rue de Picardie	32569	1	2.36276859999999989	48.8638705999999985	0	725
536	111 Rue Saint-Honoré	32567	1	2.34249829999999992	48.8614172999999994	0	705
537	25 Rue des Pyramides	32567	1	2.33364700000000003	48.8660938000000016	0	706
538	3 Rue des Déchargeurs	32567	1	2.34596919999999987	48.8596748000000005	0	707
540	35 Rue Saint-Roch	32567	1	2.33260239999999985	48.8659833000000035	0	709
541	4 Place du Louvre	32567	1	2.34111879999999983	48.8601379999999992	0	710
542	42 Rue Saint-Denis	32567	1	2.34849150000000018	48.8604375999999974	0	711
543	46 Rue Quincampoix	32570	1	2.35056229999999999	48.8610149000000007	0	712
545	 Impasse Saint-Eustache	32567	1	2.3456465999999998	48.8638521999999966	0	714
546	3 Rue Pierre Lescot	32567	1	2.34793370000000001	48.8616941000000011	0	715
547	2 Passage des Petits Pères	32568	1	2.34058369999999982	48.8664577999999992	0	716
548	177 Rue Saint-Denis	32568	1	2.35045599999999988	48.8654943000000017	0	717
549	8 Rue de la Banque	32568	1	2.34034720000000007	48.8668059999999969	0	718
550	10 Rue Portefoin	32569	1	2.3601236000000001	48.8635944999999978	0	719
551	2 Rue Eugène Spuller	32569	1	2.36133639999999989	48.8637557999999999	0	720
552	292 Rue Saint-Martin	32569	1	2.35429019999999989	48.8667255000000011	0	721
555	1 Rue Pierre l'Ermite	32584	1	2.35513769999999978	48.8850817000000006	0	724
558	25 Rue Rambuteau	32570	1	2.35448380000000013	48.8608638999999982	0	727
559	38 Rue des Francs-Bourgeois	32569	1	2.35928210000000016	48.8583803000000003	0	728
560	322 Rue Saint-Martin	32569	1	2.35526470000000021	48.8681946000000025	0	729
561	35 Boulevard du Temple	32577	1	2.36507440000000013	48.8658246999999974	0	730
563	62 Rue Beaubourg	32569	1	2.35482959999999997	48.8633436000000003	0	732
564	63 Rue Beaubourg	32569	1	2.35436980000000018	48.8630291999999997	0	733
565	129 Rue Saint-Martin	32570	1	2.35134489999999996	48.8610242000000028	0	734
566	46 Rue Quincampoix	32570	1	2.35056229999999999	48.8610149000000007	0	735
567	 Place Igor-Stravinsky	32570	1	2.35138889999999989	48.859444400000001	0	736
568	4 Rue de Lobau	32570	1	2.35368570000000021	48.8563986999999997	0	737
570	24 Rue Malher	32570	1	2.36139879999999991	48.8567391999999998	0	739
571	1 Rue du Figuier	32570	1	2.35936950000000012	48.8533723999999978	0	740
573	16 Rue Geoffroy l'Asnier	32570	1	2.35620530000000006	48.8545814000000007	0	742
574	2 Place Baudoyer	32570	1	2.3553172	48.8559278999999975	0	743
576	26 Rue Saint-Antoine	32570	1	2.36564910000000017	48.8537093999999996	0	745
578	41 Rue du Temple	32570	1	2.35396349999999988	48.8595553999999979	0	747
579	7 Rue Pecquay	32570	1	2.35585239999999985	48.8598671999999965	0	748
580	9 Rue Simon le Franc	32570	1	2.35353419999999991	48.8600800000000035	0	749
581	16 Rue Santeuil	32571	1	2.35419270000000003	48.8403615000000002	0	750
582	16 Rue des Écoles	32571	1	2.34911700000000012	48.8485663000000017	0	751
583	21 Place du Panthéon	32571	1	2.34449320000000005	48.8465518000000003	0	752
584	45 Rue d'Ulm	32571	1	2.3440344999999998	48.8418367000000018	0	753
585	58 Rue des Écoles	32571	1	2.3435674999999998	48.8501125000000016	0	754
589	101 Boulevard Raspail	32572	1	2.32852799999999993	48.846271299999998	0	758
590	12 Rue Monsieur-le-Prince	32572	1	2.33952999999999989	48.8502579999999966	0	759
591	125 Boulevard du Montparnasse	32572	1	2.33116570000000012	48.8416937000000004	0	760
592	170 Boulevard Saint-Germain	32572	1	2.33343159999999994	48.8537833000000035	0	761
593	174 Boulevard Saint-Germain	32572	1	2.33221740000000022	48.8542155000000022	0	762
595	3 Rue Mabillon	32572	1	2.33527320000000005	48.8519482000000025	0	764
596	4 Rue Félibien	32572	1	2.33670949999999999	48.8519141000000019	0	765
598	56 Rue des Saints-Pères	32572	1	2.32996820000000016	48.8537346000000028	0	767
599	2 Rue du Conservatoire	32575	1	2.34673279999999984	48.8721808999999965	0	768
600	11 Rue Ballu	32575	1	2.33057530000000002	48.881727699999999	0	769
602	17 Rue de Rochechouart	32575	1	2.34456800000000021	48.8774788999999998	0	771
603	24 Rue de Caumartin	32575	1	2.3281714	48.8718549000000024	0	772
604	47 Rue le Peletier	32575	1	2.33954659999999981	48.8753419000000022	0	773
605	5 Rue de l'Hôpital Saint-Louis	32576	1	2.36548470000000011	48.8748886999999996	0	774
606	57 Rue du Faubourg-Saint-Denis	32576	1	2.3537132999999999	48.8719436000000016	0	775
607	6 Rue Pierre Bullet	32576	1	2.35833989999999982	48.8718249	0	776
647	44 Rue du Poteau	32584	1	2.34106270000000016	48.8946793	0	816
539	3 Rue de Marivaux	32568	1	2.33736059999999979	48.8706466000000006	0	708
577	31 Rue des Francs-Bourgeois	32570	1	2.36105289999999979	48.8575467000000003	0	746
588	39 Avenue Georges Bernanos	32571	1	2.33738430000000008	48.8402168000000003	0	757
562	50 Rue des Tournelles	32569	1	2.36731960000000008	48.8562304000000012	0	731
544	 	38966	1	0.980793000000000026	44.4324119999999994	0	713
608	72 Rue du Faubourg Saint-Martin	32576	1	2.35723530000000014	48.8717490000000012	0	777
609	10 Rue la Vacquerie	32577	1	2.38519889999999979	48.8578919999999997	0	778
611	14 Rue la Vacquerie	32577	1	2.38501899999999978	48.8582431999999969	0	780
612	18 Rue de l'Orillon	32577	1	2.3757792000000002	48.870024800000003	0	781
613	20 Rue Faidherbe	32577	1	2.38395590000000013	48.8515687000000014	0	782
614	20 Avenue Parmentier	32577	1	2.37892619999999999	48.8601510000000019	0	783
615	23 Rue Voltaire	32577	1	2.39258000000000015	48.8529032000000001	0	784
617	45 Rue Richard Lenoir	32577	1	2.38110400000000011	48.8566124999999971	0	786
618	5 Passage Louis Philippe	32577	1	2.37276800000000021	48.853862399999997	0	787
620	58 Rue de la Roquette	32577	1	2.3735472999999998	48.8551154999999966	0	789
622	62 Rue du Faubourg Saint-Antoine	32578	1	2.37345719999999982	48.8518761999999995	0	791
623	7 Rue Duranti	32577	1	2.38488329999999982	48.8610417000000012	0	792
628	26 Rue Mouton-Duvernet	32580	1	2.32587680000000008	48.8324434000000025	0	797
629	38 Rue du Faubourg Saint-Jacques	32580	1	2.33805489999999994	48.8364858999999996	0	798
631	43 Rue Bargue	32581	1	2.30899849999999995	48.8379053000000027	0	800
632	29 Avenue de Villiers	32583	1	2.31220960000000009	48.8820997999999989	0	801
636	40 Rue Mathis	32585	1	2.3729998000000001	48.8913061000000013	0	805
637	5 Rue du Plateau	32585	1	2.38517950000000001	48.8779441000000006	0	806
639	55 Rue des Alouettes	32585	1	2.38567829999999992	48.8791815000000014	0	808
640	81 Rue Armand Carrel	32585	1	2.37206040000000007	48.8828375000000008	0	809
641	190 Boulevard de Charonne	32586	1	2.39176050000000018	48.8580236000000028	0	810
642	26 Rue des Grands Champs	32586	1	2.4010826999999999	48.8507661000000013	0	811
643	15 Rue Malte Brun	32586	1	2.39755850000000015	48.8646158999999969	0	812
644	51 Rue de Bagnolet	32586	1	2.3978815	48.8570565999999999	0	813
645	54 Rue des Cendriers	32586	1	2.38937419999999978	48.8662386999999967	0	814
646	3 Rue Ravignan	32584	1	2.33768410000000015	48.8854303999999971	0	815
648	67 Rue des Martyrs	32575	1	2.33963400000000021	48.8817761000000033	0	817
649	60 Boulevard de la Villette	32585	1	2.37418679999999993	48.8748165000000014	0	818
650	7 Quai de la Loire	32585	1	2.3716569999999999	48.8837919999999997	0	819
651	5 Rue Curial	32585	1	2.37147370000000013	48.8899404000000004	0	820
655	30 Rue de Belleville	32586	1	2.37972630000000018	48.8726740000000035	0	824
656	61 Rue de Bagnolet	32586	1	2.39879249999999988	48.8574315999999982	0	825
657	9 Rue des Gâtines	32586	1	2.39769960000000015	48.8652731000000031	0	826
658	59 Avenue du Général de Gaulle	38381	1	2.41644009999999998	48.8629717000000028	0	827
660	55 Avenue Laplace	38422	1	2.33006149999999979	48.8089944000000031	0	829
616	36 rue Léon Frot	32577	1	0	0	0	785
626	route du Champ de manœuvre 	32578	1	0	0	0	795
634	181 avenue Jean-Jaurès	32585	1	0	0	0	803
652	23 rue Boyer 	32586	1	0	0	0	821
653	21 rue Boyer 	32586	1	0	0	0	822
630	17 Boulevard Jourdan	32580	1	2.3387068000000002	48.8200968000000017	0	799
654	239 Rue des Pyrénées	32586	1	2.39870979999999978	48.8643829999999966	0	823
633	29 Rue Baudelique	32584	1	2.34768089999999985	48.893382299999999	0	802
619	50 Rue de Malte	32576	1	2.3668992000000002	48.8669118999999981	0	788
621	76 Rue de la Roquette	32577	1	2.37544420000000001	48.8558641999999992	0	790
624	94 Rue Jean-Pierre Timbaud	32577	1	2.37767259999999991	48.8677366000000006	0	793
610	14 Rue Lechevin	32577	1	2.37670799999999982	48.8632767000000001	0	779
635	39 Avenue Jean Jaurès	32585	1	2.37371940000000015	48.8837152999999986	0	804
659	1 Rue Charles Garnier	38411	1	2.33897859999999991	48.9052051999999975	0	828
638	 	38966	1	0.980793000000000026	44.4324119999999994	0	807
710	22 Rue Gerbier	32577	1	2.38604260000000012	48.8589887999999988	0	895
711	1 Rue Ramey	32584	1	2.34769929999999993	48.8868930999999876	0	896
712	209 Avenue Jean Jaurès	32585	1	2.39090530000000001	48.8879834999999972	0	897
713	181 Avenue Jean Jaurès	32585	1	2.38879080000000021	48.8878160000000008	0	898
714	18 Rue Janssen	32585	1	2.3975846999999999	48.8793361000000033	0	899
678	16 Cité Bauer	32580	1	2.3189495	48.8321970000000007	0	871
680	 Rue de Tlemcen	32586	1	2.38798259999999996	48.8648509999999874	0	873
682	 Rue de Rennes	32572	1	2.32982529999999999	48.8501744999999872	0	875
715	43 Rue des Panoyaux	32586	1	2.38719539999999997	48.8668509000000029	0	900
716	7 Rue des Plâtrières	32586	1	2.38946399999999981	48.8678998999999976	0	901
717	49 Boulevard Davout	32586	1	2.41081669999999981	48.8511508000000134	0	902
718	49 Rue Piat	32586	1	2.38382769999999988	48.8728454999999968	0	903
719	12 Rue du Télégraphe	32586	1	2.39999560000000001	48.8719782999999879	0	904
694	15 Rue d'Alésia	32580	1	2.33460059999999991	48.8274789999999967	0	879
695	33 Rue de Tlemcen	32586	0	2.38956519999999983	48.8655412000000027	0	879
720	13 Avenue de la Résistance	38398	1	2.43353740000000007	48.8685272000000026	0	905
721	4 Rue Édouard Vaillant	38398	1	2.43315970000000004	48.8573627999999971	0	906
696	23 boulevard belleville	32566	1	0	0	0	881
697	Adresse inconnue	11678	1	0	0	0	882
698	Adresse inconnue	11678	1	0	0	0	883
699	Adresse inconnue	11678	1	0	0	0	884
700	Adresse inconnue	11678	1	0	0	0	885
679	16 Cité Bauer	32580	1	2.3189495	48.8321970000000007	0	872
692	1 Rue de Tlemcen	32586	1	2.38612529999999978	48.8641672999999983	0	877
685	78 Rue Pernety	32580	0	2.31580640000000004	48.8353037999999984	0	876
686	1 Rue d'Alésia	32580	0	2.3412377000000002	48.8264466999999982	0	876
693	47 Rue d'Alésia	32580	1	2.33132280000000014	48.8277538999999976	0	878
683	12 Rue d'Alésia	32580	0	2.33345830000000021	48.8277417999999983	0	876
684	19 Rue Pernety	32580	0	2.31971149999999993	48.8329037999999969	0	876
690	52 Rue d'Alésia	32580	1	2.32791009999999998	48.8279320999999982	0	876
701	Adresse inconnue	11678	1	0	0	0	886
702	1 Place Charles Dullin	32584	1	2.3427614000000001	48.883355899999998	0	887
703	1 Place Jules Joffrin	32584	1	2.34451739999999997	48.8920280000000034	0	888
704	1 Rue Fleury	32584	1	2.3541224999999999	48.8841877999999994	0	889
689	Adresse inconnue	11678	1	0	0	0	851
705	1 Rue Victor Cousin	32571	1	2.34281989999999984	48.8482447000000022	0	890
706	1 Place du Trocadéro et du 11 Novembre	32582	1	2.28825119999999993	48.8629064	0	891
707	101 Quai Branly	32581	1	2.28952450000000018	48.8547708999999983	0	892
708	108 Boulevard Malesherbes	32583	1	2.30953579999999992	48.8835406000000035	0	893
722	9 Avenue de la Résistance	38398	1	2.43648879999999979	48.8590062999999972	0	907
723	9 Rue François Debergue	38398	1	2.43872929999999988	48.8580998999999991	0	908
724	10 Place Jean Jaurès	38398	1	2.44220870000000012	48.8625874000000024	0	909
687	7 Rue de Tlemcen	32586	1	2.38683529999999999	48.864443399999999	0	859
725	9 Rue Dombasle	38398	1	2.45000030000000013	48.8641435999999985	0	910
726	2 Rue Emile Zola	38398	1	2.41923980000000016	48.8549620999999874	0	911
727	5 Rue Jean Jaurès	38402	1	2.45341960000000014	48.8906500000000008	0	912
728	59 Rue Jules Guesde	38358	1	2.28570440000000019	48.8136166000000031	0	913
729	11 Rue du Coq Français	38395	1	2.41486389999999984	48.8785343999999995	0	914
730	35 Place Charles de Gaulle	38395	1	2.41917980000000021	48.8826808000000028	0	915
688	14 Cité Bauer	32580	1	2.31914800000000021	48.8320944999999966	0	874
731	35 Place Charles de Gaulle	38395	1	2.41917980000000021	48.8826808000000028	0	916
681	7 Rue de Tlemcen	32586	0	2.38683529999999999	48.864443399999999	0	874
691	3 Rue d'Alésia	32580	1	2.34029849999999984	48.826660099999998	0	874
732	23 Bis Rue Chassagnolle	38395	1	2.41340999999999983	48.8761836999999986	0	917
733	2 Rue Édouard Poisson	38379	1	2.38377870000000014	48.9107528999999985	0	918
734	 Rue Édouard Poisson	38379	1	2.38232650000000001	48.9108719999999977	0	919
735	53 Avenue Gabriel Péri	38411	1	2.33259470000000002	48.9079497000000032	0	920
736	9 Rue Gabrielle Josserand	38403	1	2.39391230000000022	48.9034136999999873	0	921
737	13 Rue des Lions Saint-Paul	32570	1	2.3618275999999998	48.8525866000000022	0	922
625	 Route du Champ de Manoeuvres	32578	1	2.45079510000000012	48.8350751999999986	0	794
738	13 Rue Santeuil	32571	1	2.35426460000000004	48.840184800000003	0	923
739	14 Rue la Vacquerie	32577	1	2.38502670000000006	48.8583242999999996	0	924
740	 Boulevard de la Bastille	32578	1	2.36808649999999998	48.8490146999999979	0	925
741	14 Rue Sainte-Isaure	32586	1	2.3442037	48.893591200000003	0	926
742	221 Avenue Jean Jaurès	32585	1	2.39361479999999993	48.889173999999997	0	927
743	41 Avenue de Flandre	32585	1	2.37137179999999992	48.8866852000000023	0	928
744	159 Avenue Gambetta	32586	1	2.40317729999999985	48.8703681000000003	0	929
745	104 Avenue Jean Lolive	38403	1	2.40890789999999999	48.8919635999999969	0	930
746	2 Rue Sadi Carnot	38403	1	2.4022237999999998	48.8967436999999876	0	931
747	4 Rue Fleury	32584	1	2.35411429999999999	48.8846117000000007	0	932
421	24 Rue Daviel	32579	1	2.34472460000000016	48.828176599999999	0	590
627	 Route du Champ de Manoeuvres	32578	1	2.45079510000000012	48.8350751999999986	0	796
748	7 Rue de Tlemcen	32586	0	2.38674900000000001	48.8645684000000031	0	576
749	6 Avenue Parmentier	32577	1	2.37997050000000021	48.8591357999999971	0	576
\.


--
-- TOC entry 2109 (class 0 OID 0)
-- Dependencies: 163
-- Name: adresses_tb_id_adresse_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('adresses_tb_id_adresse_seq', 749, true);


--
-- TOC entry 2064 (class 0 OID 16421)
-- Dependencies: 165 2090
-- Data for Name: clients_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY clients_tb (dbid, nom, surnom, dbid_lieu, dbid_genre, color) FROM stdin;
19	salope	N.C	833	1	\N
17	chienne	N.C	833	1	\N
8	Théâtre de la marionette	T.D.L.M	\N	1	\N
10	Tempête	TEM	\N	1	\N
11	Forum des images	FDI	\N	3	\N
16	Nouveau client	N.C	833	1	\N
15	zizu	tt	833	1	\N
18	pute	N.C	833	1	\N
27	Aquarium	Aqua	833	1	\N
12	Le bal	BAL	833	9	\N
28	Singe debout	S.D	833	2	\N
14	Maison des metalos	M.D.M	2	6	\N
20	Pornopera	PORN	833	3	\N
21	Nouveau client	N.C	833	1	\N
22	Nouveau client	N.C	833	1	\N
1	Dunois	DUN	833	1	(30,40,50)
9	Etouale du chnord	E.D.N	\N	2	\N
2	Clavel	CLA	833	1	\N
23	Client de oufff!!!	Client	833	6	\N
24	Opera de Paris	O.P	833	5	\N
25	Nouveau client	N.C	833	1	\N
7	Maison de la poèsie !	MDP	833	1	\N
26	Super client	Sup	833	1	\N
\.


--
-- TOC entry 2066 (class 0 OID 16431)
-- Dependencies: 167 2090
-- Data for Name: contrats_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY contrats_tb (dbid, dbid_client, date_ouverture, date_cloture, dbid_tournee, date_debut_prestation, date_fin_prestation, num, remise, dbid_genre) FROM stdin;
88	23	2000-01-01	2000-01-01	3	\N	\N	37	0	1
89	24	2000-01-01	2000-01-01	5	\N	\N	38	0	1
63	8	\N	\N	4	\N	\N	13	0	1
60	1	\N	\N	5	\N	\N	10	0	2
82	12	\N	\N	4	\N	\N	31	0	1
83	1	2000-01-11	2000-01-27	4	\N	\N	32	0	1
65	1	\N	\N	4	\N	\N	9	0	1
61	9	\N	\N	4	\N	\N	11	0	1
79	10	\N	\N	5	\N	\N	27	0	1
64	7	\N	\N	5	\N	\N	14	0	1
58	9	\N	\N	4	\N	\N	7	0	1
86	1	2000-01-01	2000-01-01	4	\N	\N	35	0	1
57	12	\N	\N	\N	\N	\N	6	0	1
90	1	2000-01-01	2000-01-01	3	\N	\N	39	0	2
54	1	2000-01-13	2000-01-03	6	2001-02-08	2000-01-18	30	10	2
67	10	\N	\N	5	\N	\N	15	0	2
91	27	2000-01-01	2000-01-01	\N	\N	\N	39	0	1
92	28	2000-01-01	2000-01-01	\N	\N	\N	40	0	1
56	7	\N	\N	7	\N	\N	5	0	1
75	1	\N	\N	7	\N	\N	21	0	1
72	10	\N	\N	5	\N	\N	13	0	1
69	1	\N	\N	\N	\N	\N	1	0	2
84	8	2000-01-01	2000-01-01	8	\N	\N	33	0	1
55	2	\N	\N	7	2000-01-12	2000-01-19	4	0	1
59	1	\N	\N	\N	\N	\N	9	0	2
73	1	\N	\N	\N	\N	\N	16	0	2
76	1	\N	\N	\N	\N	\N	21	0	2
74	1	\N	\N	\N	\N	\N	22	0	2
77	1	\N	\N	\N	\N	\N	23	0	2
71	1	\N	\N	\N	\N	\N	24	0	2
78	7	\N	\N	\N	\N	\N	25	0	2
85	21	2000-01-01	2000-01-01	\N	\N	\N	34	0	1
62	9	\N	\N	\N	\N	\N	12	0	1
66	1	\N	\N	\N	\N	\N	10	555	2
68	1	2000-01-12	2000-01-27	7	\N	\N	16	0	1
70	1	\N	\N	3	\N	\N	2	0	2
87	20	2000-01-01	2000-01-01	5	\N	\N	36	0	1
93	8	2000-01-01	2000-01-01	\N	\N	\N	41	0	1
94	14	2000-01-01	2000-01-01	\N	\N	\N	42	0	1
80	2	\N	\N	3	\N	\N	28	0	1
81	2	2000-01-01	2000-01-01	\N	\N	\N	29	0	1
95	2	2000-01-01	2000-01-01	\N	\N	\N	43	0	1
96	2	2000-01-01	2000-01-01	\N	\N	\N	44	0	1
97	1	2000-01-01	2000-01-01	\N	\N	\N	45	0	1
\.


--
-- TOC entry 2067 (class 0 OID 16435)
-- Dependencies: 168 2090
-- Data for Name: cp_villes_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY cp_villes_tb (dbid, cp, ville) FROM stdin;
38966	-1	VILLE HORS DB
11678	0	Ville inconnue
32566	75000	PARIS
33349	77760	ACHERES LA FORET
33350	77120	AMILLIS
33351	77760	AMPONVILLE
33352	77390	ANDREZEL
33353	77410	ANNET SUR MARNE
33354	77630	ARBONNE LA FORET
33355	77390	ARGENTIERES
33356	77440	ARMENTIERES EN BRIE
33357	77890	ARVILLE
33358	77720	AUBEPIERRE OZOUER LE REPO
33359	77570	AUFFERVILLE
33360	77560	AUGERS EN BRIE
33361	77120	AULNOY
33362	77210	AVON
33363	77480	BABY
33364	77167	BAGNEAUX SUR LOING
33365	77720	BAILLY CARROIS
33366	77700	BAILLY ROMAINVILLIERS
33367	77118	BALLOY
33368	77970	BANNOST VILLEGAGNON
33369	77130	BARBEY
33370	77630	BARBIZON
33371	77910	BARCY
33372	77750	BASSEVELLE
33373	77118	BAZOCHES LES BRAY
33374	77560	BEAUCHERY ST MARTIN
33375	77890	BEAUMONT DU GATINAIS
33376	77120	BEAUTHEIL
33377	77390	BEAUVOIR
33378	77510	BELLOT
33379	77540	BERNAY VILBERT
33380	77320	BETON BAZOCHES
33381	77970	BEZALLES
33382	77115	BLANDY
33383	77940	BLENNES
33384	77970	BOISDON
33385	77590	BOIS LE ROI
33386	77350	BOISSETTES
33387	77350	BOISSISE LA BERTRAND
33388	77310	BOISSISE LE ROI
33389	77760	BOISSY AUX CAILLES
33390	77169	BOISSY LE CHATEL
33391	77750	BOITRON
33392	77720	BOMBON
33393	77570	BOUGLIGNY
33394	77760	BOULANCOURT
33395	77580	BOULEURS
33396	77780	BOURRON MARLOTTE
33397	77470	BOUTIGNY
33398	77620	BRANSLES
33399	77480	BRAY SUR SEINE
33400	77720	BREAU
33401	77170	BRIE COMTE ROBERT
33402	77940	LA BROSSE MONTCEAUX
33403	77177	BROU SUR CHANTEREINE
33404	77890	BURCY
33405	77750	BUSSIERES
33406	77600	BUSSY ST GEORGES
33407	77600	BUSSY ST MARTIN
33408	77760	BUTHIERS
33409	77130	CANNES ECLUSES
33410	77400	CARNETIN
33411	77515	LA CELLE SUR MORIN
33412	77670	LA CELLE SUR SEINE
33413	77930	CELY
33414	77320	CERNEUX
33415	77240	CESSON
33416	77520	CESSOY EN MONTOIS
33417	77930	CHAILLY EN BIERE
33418	77120	CHAILLY EN BRIE
33419	77460	CHAINTREAUX
33420	77171	CHALAUTRE LA GRANDE
33421	77160	CHALAUTRE LA PETITE
33422	77520	CHALAUTRE LA REPOSTE
33423	77144	CHALIFERT
33424	77650	CHALMAISON
33425	77910	CHAMBRY
33426	77260	CHAMIGNY
33427	77430	CHAMPAGNE SUR SEINE
33428	77560	CHAMPCENEST
33429	77390	CHAMPDEUIL
33430	77720	CHAMPEAUX
33431	77420	CHAMPS SUR MARNE
33432	77660	CHANGIS SUR MARNE
33433	77600	CHANTELOUP EN BRIE
33434	77720	LA CHAPELLE GAUTHIER
33435	77540	LA CHAPELLE IGER
33436	77760	LA CHAPELLE LA REINE
33437	77370	LA CHAPELLE RABLAIS
33438	77160	LA CHAPELLE ST SULPICE
33439	77610	LES CHAPELLES BOURBON
33440	77580	LA CHAPELLE SUR CRECY
33441	77320	LA CHAPELLE MOUTILS
33442	77410	CHARMENTRAY
33443	77410	CHARNY
33444	77590	CHARTRETTES
33445	77320	CHARTRONGES
33446	77370	CHATEAUBLEAU
33447	77570	CHATEAU LANDON
33448	77820	LE CHATELET EN BRIE
33449	77126	CHATENAY SUR SEINE
33450	77167	CHATENOY
33451	77820	CHATILLON LA BORDE
33452	77610	CHATRES
33453	77124	CHAUCONIN
33454	77169	CHAUFFRY
33455	77390	CHAUMES EN BRIE
33456	77500	CHELLES
33457	77160	CHENOISE
33458	77570	CHENOU
33459	77700	CHESSY
33460	77760	CHEVRAINVILLIERS
33461	77320	CHEVRU
33462	77173	CHEVRY COSSIGNY
33463	77710	CHEVRY EN SEREINE
33464	77320	CHOISY EN BRIE
33465	77730	CITRY
33466	77410	CLAYE SOUILLY
33467	77370	CLOS FONTAINE
33468	77440	COCHEREL
33469	77090	COLLEGIEN
33470	77380	COMBS LA VILLE
33471	77290	COMPANS
33472	77600	CONCHES SUR GONDOIRE
33473	77450	CONDE STE LIBIAIRE
33474	77440	CONGIS SUR THEROUANNE
33475	77170	COUBERT
33476	77860	COUILLY PONT AUX DAMES
33477	77840	COULOMBS EN VALOIS
33478	77580	COULOMMES
33479	77120	COULOMMIERS
33480	77700	COUPVRAY
33481	77126	COURCELLES EN BASSEE
33482	77560	COURCHAMP
33483	77540	COURPALAY
33484	77390	COURQUETAINE
33485	77560	COURTACON
33486	77390	COURTOMER
33487	77181	COURTRY
33488	77154	COUTENCON
33489	77580	COUTEVROULT
33490	77580	CRECY LA CHAPELLE
33491	77124	CREGY LES MEAUX
33492	77610	CREVECOEUR EN BRIE
33493	77390	CRISENOY
33494	77183	CROISSY BEAUBOURG
33495	77370	LA CROIX EN BRIE
33496	77840	CROUY SUR OURCQ
33497	77160	CUCHARMOY
33498	77165	CUISY
33499	77320	DAGNY
33500	77190	DAMMARIE LES LYS
33501	77230	DAMMARTIN EN GOELE
33502	77163	DAMMARTIN SUR TIGEAUX
33503	77400	DAMPMART
33504	77140	DARVAULT
33505	77440	DHUISY
33506	77940	DIANT
33507	77520	DONNEMARIE DONTILLY
33508	77130	DORMELLES
33509	77510	DOUE
33510	77139	DOUY LA RAMEE
33511	77830	ECHOUBOULAINS
33512	77820	LES ECRENNES
33513	77250	ECUELLES
33514	77126	EGLIGNY
33515	77620	EGREVILLE
33516	77184	EMERAINVILLE
33517	77250	EPISY
33518	77450	ESBLY
33519	77940	ESMANS
33520	77139	ETREPILLY
33521	77157	EVERLY
33522	77166	EVRY GREGY SUR YERRE
33523	77515	FAREMOUTIERS
33524	77220	FAVIERES
33525	77167	FAY LES NEMOURS
33526	77133	FERICY
33527	77150	FEROLLES ATTILLY
33528	77164	FERRIERES
33529	77320	LA FERTE GAUCHER
33530	77260	LA FERTE SOUS JOUARRE
33531	77940	FLAGY
33532	77930	FLEURY EN BIERE
33533	77300	FONTAINEBLEAU
33534	77480	FONTAINE FOURCHES
33535	77590	FONTAINE LE PORT
33536	77560	FONTAINE SOUS MONTAIGUILL
33537	77370	FONTAINS
33538	77370	FONTENAILLES
33539	77610	FONTENAY TRESIGNY
33540	77165	FORFRY
33541	77130	FORGES
33542	77390	FOUJU
33543	77410	FRESNES SUR MARNE
33544	77320	FRETOY
33545	77760	FROMONT
33546	77470	FUBLAINES
33547	77890	GARENTREVILLE
33548	77370	GASTINS
33549	77690	LA GENEVRAYE
33550	77910	GERMIGNY L EVEQUE
33551	77840	GERMIGNY SOUS COULOMBS
33552	77165	GESVRES LE CHAPITRE
33553	77120	GIREMOUTIERS
33554	77890	GIRONVILLE
33555	77114	GOUAIX
33556	77400	GOUVERNES
33557	77130	LA GRANDE PAROISSE
33558	77720	GRANDPUITS BAILLY CARROIS
33559	77118	GRAVON
33560	77166	GREGY SUR YERRE
33561	77410	GRESSY
33562	77220	GRETZ ARMAINVILLIERS
33563	77880	GREZ SUR LOING
33564	77166	GRISY SUISNES
33565	77480	GRISY SUR SEINE
33566	77580	GUERARD
33567	77760	GUERCHEVILLE
33568	77600	GUERMANTES
33569	77390	GUIGNES
33570	77520	GURCY LE CHATEL
33571	77515	HAUTEFEUILLE
33572	77580	LA HAUTE MAISON
33573	77850	HERICY
33574	77114	HERME
33575	77510	HONDEVILLIERS
33576	77610	LA HOUSSAYE EN BRIE
33577	77890	ICHY
33578	77440	ISLES LES MELDEUSES
33579	77450	ISLES LES VILLENOY
33580	77165	IVERNY
33581	77450	JABLINES
33582	77440	JAIGNES
33583	77480	JAULNES
33584	77600	JOSSIGNY
33585	77640	JOUARRE
33586	77970	JOUY LE CHATEL
33587	77320	JOUY SUR MORIN
33588	77230	JUILLY
33589	77650	JUTIGNY
33590	77400	LAGNY SUR MARNE
33591	77760	LARCHANT
33592	77148	LAVAL EN BRIE
33593	77171	LECHELLE
33594	77320	LESCHEROLLES
33595	77450	LESCHES
33596	77150	LESIGNY
33597	77320	LEUDON EN BRIE
33598	77127	LIEUSAINT
33599	77550	LIMOGES FOURCHES
33600	77550	LISSY
33601	77220	LIVERDY EN BRIE
33602	77000	LIVRY SUR SEINE
33603	77650	LIZINES
33604	77440	LIZY SUR OURCQ
33605	77185	LOGNES
33606	77230	LONGPERRIER
33607	77650	LONGUEVILLE
33608	77710	LORREZ LE BOCAGE PREAUX
33609	77560	LOUAN VILLEGRUIS FONTAINE
33610	77520	LUISETAINES
33611	77540	LUMIGNY NESLES ORMEAUX
33612	77138	LUZANCY
33613	77133	MACHAULT
33614	77570	LA MADELEINE SUR LOING
33615	77700	MAGNY LE HONGRE
33616	77950	MAINCY
33617	77580	MAISONCELLES EN BRIE
33618	77570	MAISONCELLES EN GATINAIS
33619	77370	MAISON ROUGE
33620	77230	MARCHEMORET
33621	77139	MARCILLY
33622	77560	LES MARETS
33623	77100	MAREUIL LES MEAUX
33624	77610	MARLES EN BRIE
33625	77120	MAROLLES EN BRIE
33626	77130	MAROLLES SUR SEINE
33627	77440	MARY SUR MARNE
33628	77120	MAUPERTHUIS
33629	77990	MAUREGARD
33630	77145	MAY EN MULTIEN
33631	77100	MEAUX
33632	77350	LE MEE SUR SEINE
33633	77520	MEIGNEUX
33634	77320	MEILLERAY
33635	77000	MELUN
33636	77171	MELZ SUR SEINE
33637	77730	MERY SUR MARNE
33638	77990	LE MESNIL AMELOT
33639	77410	MESSY
33640	77130	MISY SUR YONNE
33641	77290	MITRY MORY
33642	77950	MOISENAY
33643	77550	MOISSY CRAMAYEL
33644	77570	MONDREVILLE
33645	77520	MONS EN MONTOIS
33646	77250	MONTARLOT
33647	77470	MONTCEAUX LES MEAUX
33648	77151	MONTCEAUX LES PROVINS
33649	77140	MONTCOURT FROMONVILLE
33650	77320	MONTDAUPHIN
33651	77320	MONTENILS
33652	77130	MONTEREAU FAUT YONNE
33653	77950	MONTEREAU SUR LE JARD
33654	77144	MONTEVRAIN
33655	77230	MONTGE EN GOELE
33656	77122	MONTHYON
33657	77480	MONTIGNY LE GUESDIER
33658	77520	MONTIGNY LENCOUP
33659	77690	MONTIGNY SUR LOING
33660	77940	MONTMACHOUX
33661	77320	MONTOLIVET
33662	77450	MONTRY
33663	77250	MORET SUR LOING
33664	77720	MORMANT
33665	77163	MORTCERF
33666	77160	MORTERY
33667	77120	MOUROUX
33668	77480	MOUSSEAUX LES BRAY
33669	77230	MOUSSY LE NEUF
33670	77230	MOUSSY LE VIEUX
33671	77320	MOUTILS
33672	77480	MOUY SUR SEINE
33673	77176	NANDY
33674	77370	NANGIS
33675	77760	NANTEAU SUR ESSONNES
33676	77710	NANTEAU SUR LUNAIN
33677	77100	NANTEUIL LES MEAUX
33678	77730	NANTEUIL SUR MARNE
33679	77230	NANTOUILLET
33680	77140	NEMOURS
33681	77540	NESLES LA GILBERDE
33682	77124	CHAUCONIN NEUFMONTIERS
33683	77610	NEUFMOUTIERS EN BRIE
33684	77186	NOISIEL
33685	77940	NOISY RUDIGNON
33686	77123	NOISY SUR ECOLE
33687	77140	NONVILLE
33688	77114	NOYEN SUR SEINE
33689	77890	OBSONVILLE
33690	77440	OCQUERRE
33691	77178	OISSERY
33692	77750	ORLY SUR MORIN
33693	77540	ORMEAUX
33694	77134	LES ORMES SUR VOULZIE
33695	77167	ORMESSON
33696	77280	OTHIS
33697	77330	OZOIR LA FERRIERE
33698	77720	OZOUER LE REPOS
33699	77390	OZOUER LE VOULGIS
33700	77710	PALEY
33701	77830	PAMFOU
33702	77520	PAROY
33703	77480	PASSY SUR SEINE
33704	77970	PECY
33705	77124	PENCHARD
33706	77930	PERTHES
33707	77131	PEZARCHES
33708	77580	PIERRE LEVEE
33709	77181	LE PIN
33710	77165	LE PLESSIS AUX BOIS
33711	77540	LE PLESSIS FEU AUSSOUX
33712	77165	LE PLESSIS L EVEQUE
33713	77440	LE PLESSIS PLACY
33714	77160	POIGNY
33715	77470	POINCY
33716	77167	POLIGNY
33717	77515	POMMEUSE
33718	77400	POMPONNE
33719	77340	PONTAULT COMBAULT
33720	77135	PONTCARRE
33721	77710	PREAUX
33722	77410	PRECY SUR MARNE
33723	77220	PRESLES EN BRIE
33724	77310	PRINGY
33725	77160	PROVINS
33726	77139	PUISIEUX
33727	77720	QUIERS
33728	77860	QUINCY VOISINS
33729	77370	RAMPILLON
33730	77550	REAU
33731	77510	REBAIS
33732	77760	RECLOSES
33733	77710	REMAUVILLE
33734	77260	REUIL EN BRIE
33735	77000	LA ROCHETTE
33736	77680	ROISSY EN BRIE
33737	77160	ROUILLY
33738	77230	ROUVRES
33739	77540	ROZAY EN BRIE
33740	77950	RUBELLES
33741	77760	RUMONT
33742	77560	RUPEREUX
33743	77730	SAACY SUR MARNE
33744	77510	SABLONNIERES
33745	77710	ST ANGE LE VIEL
33746	77515	ST AUGUSTIN
33747	77260	ST AULDE
33748	77320	ST BARTHELEMY
33749	77160	ST BRICE
33750	77650	STE COLOMBE
33751	77750	ST CYR SUR MORIN
33752	77510	ST DENIS LES REBAIS
33753	77310	ST FARGEAU PONTHIERRY
33754	77470	ST FIACRE
33755	77130	ST GERMAIN LAVAL
33756	77950	ST GERMAIN LAXIS
33757	77169	ST GERMAIN SOUS DOUE
33758	77930	ST GERMAIN SUR ECOLE
33759	77860	ST GERMAIN SUR MORIN
33760	77160	ST HILLIERS
33761	77660	ST JEAN LES DEUX JUMEAUX
33762	77370	ST JUST EN BRIE
33763	77510	ST LEGER
33764	77650	ST LOUP DE NAUD
33765	77670	ST MAMMES
33766	77230	ST MARD
33767	77320	ST MARS VIEUX MAISONS
33768	77560	ST MARTIN CHENNETRON
33769	77320	ST MARTIN DES CHAMPS
33770	77320	ST MARTIN DU BOSCHET
33771	77630	ST MARTIN EN BIERE
33772	77720	ST MERY
33773	77410	ST MESMES
33774	77720	ST OUEN EN BRIE
33775	77750	ST OUEN SUR MORIN
33776	77178	ST PATHUS
33777	77140	ST PIERRE LES NEMOURS
33778	77320	ST REMY DE LA VANNE
33779	77120	SAINTS
33780	77480	ST SAUVEUR LES BRAY
33781	77930	ST SAUVEUR SUR ECOLE
33782	77169	ST SIMEON
33783	77165	ST SOUPPLETS
33784	77400	ST THIBAULT DES VIGNES
33785	77148	SALINS
33786	77260	SAMMERON
33787	77920	SAMOIS SUR SEINE
33788	77210	SAMOREAU
33789	77580	SANCY
33790	77320	SANCY LES PROVINS
33791	77176	SAVIGNY LE TEMPLE
33792	77650	SAVINS
33793	77240	SEINE PORT
33794	77260	SEPT SORTS
33795	77700	SERRIS
33796	77170	SERVON
33797	77640	SIGNY SIGNETS
33798	77520	SIGY
33799	77115	SIVRY COURTRY
33800	77520	SOGNOLLES EN MONTOIS
33801	77111	SOIGNOLLES EN BRIE
33802	77650	SOISY BOUY
33803	77111	SOLERS
33804	77460	SOUPPES SUR LOING
33805	77171	SOURDUN
33806	77440	TANCROU
33807	77520	THENISY
33808	77230	THIEUX
33809	77810	THOMERY
33810	77400	THORIGNY SUR MARNE
33811	77156	THOURY FEROTTES
33812	77163	TIGEAUX
33813	77130	LA TOMBE
33814	77200	TORCY
33815	77131	TOUQUIN
33816	77220	TOURNAN EN BRIE
33817	77123	TOUSSON
33818	77510	LA TRETOIRE
33819	77710	TREUZY LEVELAY
33820	77450	TRILBARDOU
33821	77470	TRILPORT
33822	77440	TROCY EN MULTIEN
33823	77760	URY
33824	77260	USSY SUR MARNE
33825	77360	VAIRES SUR MARNE
33826	77830	VALENCE EN BRIE
33827	77370	VANVILLE
33828	77130	VARENNES SUR SEINE
33829	77910	VARREDDES
33830	77580	VAUCOURTOIS
33831	77123	LE VAUDOUE
33832	77141	VAUDOY EN BRIE
33833	77000	VAUX LE PENIL
33834	77710	VAUX SUR LUNAIN
33835	77440	VENDREST
33836	77250	VENEUX LES SABLONS
33837	77510	VERDELOT
33838	77390	VERNEUIL L ETANG
33839	77670	VERNOU LA CELLE SUR SEINE
33840	77240	VERT ST DENIS
33841	77370	VIEUX CHAMPAGNE
33842	77320	VIEUX MAISONS
33843	77450	VIGNELY
33844	77540	VILBERT
33845	77710	VILLEBEON
33846	77250	VILLECERF
33847	77970	VILLEGAGNON
33848	77560	VILLEGRUIS
33849	77710	VILLEMARECHAL
33850	77470	VILLEMAREUIL
33851	77250	VILLEMER
33852	77480	VILLENAUXE LA PETITE
33853	77174	VILLENEUVE LE COMTE
33854	77154	VILLENEUVE LES BORDES
33855	77174	VILLENEUVE ST DENIS
33856	77230	VILLENEUVE SOUS DAMMARTIN
33857	77510	VILLENEUVE SUR BELLOT
33858	77124	VILLENOY
33859	77270	VILLEPARISIS
33860	77410	VILLEROY
33861	77130	VILLE ST JACQUES
33862	77410	VILLEVAUDE
33863	77190	VILLIERS EN BIERE
33864	77560	VILLIERS ST GEORGES
33865	77760	VILLIERS SOUS GREZ
33866	77580	VILLIERS SUR MORIN
33867	77114	VILLIERS SUR SEINE
33868	77480	VILLUIS
33869	77520	VIMPELLES
33870	77230	VINANTES
33871	77139	VINCY MANOEUVRE
33872	77540	VOINSLES
33873	77950	VOISENON
33874	77580	VOULANGIS
33875	77560	VOULTON
33876	77940	VOULX
33877	77160	VULAINES LES PROVINS
33878	77870	VULAINES SUR SEINE
33879	77390	YEBLES
33880	77310	PONTHIERRY
33881	77410	SOUILLY
33882	77500	CHANTEREINE
33883	77410	MONTJAY LA TOUR
33884	77410	BORDEAUX
33885	77400	LA POMPONNETTE
33886	77184	MALNOUE
33887	77340	LE PAVE DE PONTAULT
33888	77400	RENTILLY
33889	77183	BEUABOURG
33890	77173	COSSIGNY
33891	77166	SUISNES
33892	77124	NEUFMONTIERS LES MEAUX
33893	78660	ABLIS
33894	78260	ACHERES
33895	78113	ADAINVILLE
33896	78240	AIGREMONT
33897	78660	ALLAINVILLE
33898	78580	LES ALLUETS LE ROI
33899	78770	ANDELU
33900	78570	ANDRESY
33901	78790	ARNOUVILLE LES MANTES
33902	78410	AUBERGENVILLE
33903	78610	AUFFARGIS
33904	78930	AUFREVILLE BRASSEUIL
33905	78126	AULNAY SUR MAULDRE
33906	78770	AUTEUIL
33907	78770	AUTOUILLET
33908	78870	BAILLY
33909	78550	BAZAINVILLE
33910	78580	BAZEMONT
33911	78490	BAZOCHES SUR GUYONNE
33912	78910	BEHOUST
33913	78270	BENNECOURT
33914	78650	BEYNES
33915	78270	BLARU
33916	78930	BOINVILLE EN MANTOIS
33917	78660	BOINVILLE LE GAILLARD
33918	78200	BOINVILLIERS
33919	78390	BOIS D ARCY
33920	78910	BOISSETS
33921	78125	LA BOISSIERE ECOLE
33922	78200	BOISSY MAUVOISIN
33923	78490	BOISSY SANS AVOIR
33924	78830	BONNELLES
33925	78270	BONNIERES SUR SEINE
33926	78410	BOUAFLE
33927	78380	BOUGIVAL
33928	78113	BOURDONNE
33929	78930	BREUIL BOIS ROBERT
33930	78980	BREVAL
33931	78610	LES BREVIAIRES
33932	78440	BRUEIL EN VEXIN
33933	78530	BUC
33934	78200	BUCHELAY
33935	78830	BULLION
33936	78955	CARRIERES SOUS POISSY
33937	78420	CARRIERES SUR SEINE
33938	78720	LA CELLE LES BORDES
33939	78170	LA CELLE ST CLOUD
33940	78720	CERNAY LA VILLE
33941	78240	CHAMBOURCY
33942	78570	CHANTELOUP LES VIGNES
33943	78130	CHAPET
33944	78117	CHATEAUFORT
33945	78400	CHATOU
33946	78270	CHAUFOUR LES BONNIERES
33947	78450	CHAVENAY
33948	78150	LE CHESNAY
33949	78460	CHEVREUSE
33950	78460	CHOISEL
33951	78910	CIVRY LA FORET
33952	78120	CLAIREFONTAINE EN YVELINE
33953	78340	LES CLAYES SOUS BOIS
33954	78310	COIGNIERES
33955	78113	CONDE SUR VESGRE
33956	78700	CONFLANS STE HONORINE
33957	78790	COURGENT
33958	78660	CRACHES
33959	78270	CRAVENT
33960	78121	CRESPIERES
33961	78290	CROISSY SUR SEINE
33962	78111	DAMMARTIN EN SERVE
33963	78720	DAMPIERRE EN YVELINES
33964	78550	DANNEMARIE
33965	78810	DAVRON
33966	78440	DROCOURT
33967	78920	ECQUEVILLY
33968	78990	ELANCOURT
33969	78125	EMANCE
33970	78680	EPONE
33971	78690	LES ESSARTS LE ROI
33972	78620	L ETANG LA VILLE
33973	78740	EVECQUEMONT
33974	78410	LA FALAISE
33975	78200	FAVRIEUX
33976	78810	FEUCHEROLLES
33977	78200	FLACOURT
33978	78910	FLEXANVILLE
33979	78790	FLINS NEUVE EGLISE
33980	78410	FLINS SUR SEINE
33981	78520	FOLLAINVILLE DENNEMONT
33982	78330	FONTENAY LE FLEURY
33983	78200	FONTENAY MAUVOISIN
33984	78440	FONTENAY ST PERE
33985	78112	FOURQUEUX
33986	78840	FRENEUSE
33987	78250	GAILLON SUR MONTCIENT
33988	78490	GALLUIS
33989	78950	GAMBAIS
33990	78490	GAMBAISEUIL
33991	78890	GARANCIERES
33992	78440	GARGENVILLE
33993	78125	GAZERAN
33994	78270	GOMMECOURT
33995	78770	GOUPILLIERES
33996	78930	GOUSSONVILLE
33997	78113	GRANDCHAMP
33998	78550	GRESSEY
33999	78490	GROSROUVRE
34000	78520	GUERNES
34001	78930	GUERVILLE
34002	78440	GUITRANCOURT
34003	78280	GUYANCOURT
34004	78250	HARDRICOURT
34005	78790	HARGEVILLE
34006	78113	LA HAUTEVILLE
34007	78580	HERBEVILLE
34008	78125	HERMERAY
34009	78550	HOUDAN
34010	78800	HOUILLES
34011	78440	ISSOU
34012	78440	JAMBVILLE
34013	78270	JEUFOSSE
34014	78760	JOUARS PONTCHARTRAIN
34015	78350	JOUY EN JOSAS
34016	78200	JOUY MAUVOISIN
34017	78580	JUMEAUVILLE
34018	78820	JUZIERS
34019	78440	LAINVILLE
34020	78320	LEVIS ST NOM
34021	78520	LIMAY
34022	78270	LIMETZ VILLEZ
34023	78350	LES LOGES EN JOSAS
34024	78270	LOMMOYE
34025	78980	LONGNES
34026	78730	LONGVILLIERS
34027	78430	LOUVECIENNES
34028	78200	MAGNANVILLE
34029	78114	MAGNY LES HAMEAUX
34030	78720	MAINCOURT SUR YVETTE
34031	78600	MAISONS LAFFITTE
34032	78200	MANTES LA JOLIE
34033	78200	MANTES LA VILLE
34034	78770	MARCQ
34035	78490	MAREIL LE GUYON
34036	78750	MAREIL MARLY
34037	78124	MAREIL SUR MAULDRE
34038	78160	MARLY LE ROI
34039	78580	MAULE
34040	78550	MAULETTE
34041	78780	MAURECOURT
34042	78310	MAUREPAS
34043	78670	MEDAN
34044	78200	MENERVILLE
34045	78490	MERE
34046	78270	MERICOURT
34047	78600	MESNIL LE ROI
34048	78320	LE MESNIL ST DENIS
34049	78490	LES MESNULS
34050	78250	MEULAN
34051	78970	MEZIERES SUR SEINE
34052	78250	MEZY SUR SEINE
34053	78940	MILLEMONT
34054	78470	MILON LA CHAPELLE
34055	78125	MITTAINVILLE
34056	78840	MOISSON
34057	78980	MONDREVILLE
34058	78124	MONTAINVILLE
34059	78440	MONTALET LE BOIS
34060	78790	MONTCHAUVET
34061	78360	MONTESSON
34062	78490	MONTFORT L AMAURY
34063	78180	MONTIGNY LE BRETONNEUX
34064	78630	MORAINVILLIERS
34065	78270	MOUSSEAUX SUR SEINE
34066	78790	MULCENT
34067	78130	LES MUREAUX
34068	78640	NEAUPHLE LE CHATEAU
34069	78640	NEAUPHLE LE VIEUX
34070	78980	NEAUPHLETTE
34071	78410	NEZEL
34072	78590	NOISY LE ROI
34073	78250	OINVILLE SUR MONTCIENT
34074	78125	ORCEMONT
34075	78910	ORGERUS
34076	78630	ORGEVAL
34077	78125	ORPHIN
34078	78660	ORSONVILLE
34079	78910	ORVILLIERS
34080	78910	OSMOY
34081	78660	PARAY DOUAVILLE
34082	78230	LE PECQ
34083	78200	PERDREAUVILLE
34084	78610	LE PERRAY EN YVELINES
34085	78370	PLAISIR
34086	78125	POIGNY LA FORET
34087	78300	POISSY
34088	78730	PONTHEVRARD
34089	78440	PORCHEVILLE
34090	78560	LE PORT MARLY
34091	78270	PORT VILLEZ
34092	78910	PRUNAY LE TEMPLE
34093	78660	PRUNAY EN YVELINES
34094	78940	LA QUEUE LES YVELINES
34095	78125	RAIZEUX
34096	78120	RAMBOUILLET
34097	78590	RENNEMOULIN
34098	78550	RICHEBOURG
34099	78730	ROCHEFORT EN YVELINES
34100	78150	ROCQUENCOURT
34101	78270	ROLLEBOISE
34102	78790	ROSAY
34103	78710	ROSNY SUR SEINE
34104	78440	SAILLY
34105	78730	ST ARNOULT EN YVELINES
34106	78210	ST CYR L ECOLE
34107	78720	ST FORGET
34108	78640	ST GERMAIN DE LA GRANGE
34109	78100	ST GERMAIN EN LAYE
34110	78125	ST HILARION
34111	78980	ST ILLIERS LA VILLE
34112	78980	ST ILLIERS LE BOIS
34113	78470	ST LAMBERT
34114	78610	ST LEGER EN YVELINES
34115	78660	ST MARTIN BRETHENCOURT
34116	78790	ST MARTIN DES CHAMPS
34117	78520	ST MARTIN LA GARENNE
34118	78730	STE MESME
34119	78860	ST NOM LA BRETECHE
34120	78470	ST REMY LES CHEVREUSE
34121	78690	ST REMY L HONORE
34122	78500	SARTROUVILLE
34123	78650	SAULX MARCHAIS
34124	78720	SENLISSE
34125	78790	SEPTEUIL
34126	78200	SOINDRES
34127	78120	SONCHAMP
34128	78910	TACOIGNIERES
34129	78113	LE TARTRE GAUDRAN
34130	78980	LE TERTRE ST DENIS
34131	78250	TESSANCOURT SUR AUBETTE
34132	78850	THIVERVAL GRIGNON
34133	78770	THOIRY
34134	78790	TILLY
34135	78117	TOUSSUS LE NOBLE
34136	78190	TRAPPES
34137	78490	LE TREMBLAY SUR MAULDRE
34138	78510	TRIEL SUR SEINE
34139	78740	VAUX SUR SEINE
34140	78140	VELIZY VILLACOUBLAY
34141	78480	VERNEUIL SUR SEINE
34142	78540	VERNOUILLET
34143	78320	LA VERRIERE
34144	78000	VERSAILLES
34145	78930	VERT
34146	78110	LE VESINET
34147	78490	VICQ
34148	78125	VIEILLE EGLISE YVELINES
34149	78270	LA VILLENEUVE EN CHEVRIE
34150	78670	VILLENNES SUR SEINE
34151	78450	VILLEPREUX
34152	78930	VILLETTE
34153	78770	VILLIERS LE MAHIEU
34154	78640	VILLIERS ST FREDERIC
34155	78220	VIROFLAY
34156	78960	VOISINS LE BRETONNEUX
34157	78114	CRESSELY
34158	78540	MARSINVAL
34159	78650	VAL DES QUATRE PIGNONS
34160	78300	LA MALADRERIE
34161	78510	HAUTIL
34162	78510	CHEVERCHEMONT
34163	78570	DENOUVAL
34164	78955	LES GRESILLONS
34165	78860	LA BRETECHE
34166	78160	MONTVAL
34167	78600	CARRIERES SOUS BOIS
34168	78280	BOUVIERS
34169	78280	VILLAROY
34170	78150	PARLY
34171	78470	RHODON
34172	78650	LA MALADRERIE
34173	78410	ELISABETHVILLE
34174	78690	ST HUBERT LE ROI
34175	78550	THIONVILLE SUR OPTON
38132	91150	ABBEVILLE LA RIVIERE
38133	91670	ANGERVILLE
38134	91470	ANGERVILLIERS
38135	91290	ARPAJON
38136	91690	ARRANCOURT
38137	91200	ATHIS MONS
38138	91410	AUTHON LA PLAINE
38139	91830	AUVERNAUX
38140	91580	AUVERS ST GEORGES
38141	91630	AVRAINVILLE
38142	91160	BALLAINVILLIERS
38143	91610	BALLANCOURT SUR ESSONNE
38144	91590	BAULNE
38145	91570	BIEVRES
38146	91150	BLANDY
38147	91720	BOIGNEVILLE
38148	91150	BOIS HERPIN
38149	91690	BOISSY LA RIVIERE
38150	91590	BOISSY LE CUTTE
38151	91870	BOISSY LE SEC
38152	91790	BOISSY SOUS ST YON
38153	91070	BONDOUFLE
38154	91470	BOULLAY LES TROUX
38155	91850	BOURAY SUR JUINE
38156	91800	BOUSSY ST ANTOINE
38157	91150	BOUTERVILLIERS
38158	91820	BOUTIGNY SUR ESSONNE
38159	91880	BOUVILLE
38160	91220	BRETIGNY SUR ORGE
38161	91650	BREUILLET
38162	91650	BREUX JOUY
38163	91150	BRIERES LES SCELLES
38164	91640	BRIIS SOUS FORGES
38165	91150	BROUY
38166	91800	BRUNOY
38167	91680	BRUYERES LE CHATEL
38168	91720	BUNO BONNEVAUX
38169	91440	BURES SUR YVETTE
38170	91590	CERNY
38171	91780	CHALO ST MARS
38172	91740	CHALOU MOULINEUX
38173	91730	CHAMARANDE
38174	91750	CHAMPCUEIL
38175	91160	CHAMPLAN
38176	91150	CHAMPMOTTEUX
38177	91410	CHATIGNONVILLE
38178	91580	CHAUFFOUR LES ETRECHY
38179	91630	CHEPTAINVILLE
38180	91750	CHEVANNES
38181	91380	CHILLY MAZARIN
38182	91740	CONGERVILLE
38183	91100	CORBEIL ESSONNES
38184	91410	CORBREUSE
38185	91830	LE COUDRAY MONTCEAUX
38186	91490	COURANCES
38187	91080	COURCOURONNES
38188	91720	COURDIMANCHE SUR ESSONNE
38189	91680	COURSON MONTELOUP
38190	91560	CROSNE
38191	91490	DANNEMOIS
38192	91590	D HUISON LONGUEVILLE
38193	91410	DOURDAN
38194	91210	DRAVEIL
38195	91540	ECHARCON
38196	91520	EGLY
38197	91860	EPINAY SOUS SENART
38198	91360	EPINAY SUR ORGE
38199	91660	ESTOUCHES
38200	91150	ETAMPES
38201	91450	ETIOLLES
38202	91580	ETRECHY
38203	91000	EVRY
38204	91590	LA FERTE ALAIS
38205	91700	FLEURY MEROGIS
38206	91690	FONTAINE LA RIVIERE
38207	91640	FONTENAY LES BRIIS
38208	91540	FONTENAY LE VICOMTE
38209	91410	LA FORET LE ROI
38210	91150	LA FORET STE CROIX
38211	91470	FORGES LES BAINS
38212	91190	GIF SUR YVETTE
38213	91720	GIRONVILLE SUR ESSONNE
38214	91400	GOMETZ LA VILLE
38215	91940	GOMETZ LE CHATEL
38216	91410	LES GRANGES LE ROI
38217	91350	GRIGNY
38218	91630	GUIBEVILLE
38219	91590	GUIGNEVILLE SUR ESSONNE
38220	91690	GUILLERVAL
38221	91430	IGNY
38222	91760	ITTEVILLE
38223	91510	JANVILLE SUR JUINE
38224	91640	JANVRY
38225	91260	JUVISY SUR ORGE
38226	91510	LARDY
38227	91630	LEUDEVILLE
38228	91310	LEUVILLE SUR ORGE
38229	91470	LIMOURS
38230	91310	LINAS
38231	91090	LISSES
38232	91160	LONGJUMEAU
38233	91310	LONGPONT SUR ORGE
38234	91720	MAISSE
38235	91460	MARCOUSSIS
38236	91150	MAROLLES EN BEAUCE
38237	91630	MAROLLES EN HUREPOIX
38238	91300	MASSY
38239	91730	MAUCHAMPS
38240	91540	MENNECY
38241	91660	MEREVILLE
38242	91780	MEROBERT
38243	91150	MESPUITS
38244	91490	MILLY LA FORET
38245	91490	MOIGNY SUR ECOLE
38246	91470	LES MOLIERES
38247	91590	MONDEVILLE
38248	91930	MONNERVILLE
38249	91230	MONTGERON
38250	91310	MONTLHERY
38251	91420	MORANGIS
38252	91150	MORIGNY CHAMPIGNY
38253	91390	MORSANG SUR ORGE
38254	91250	MORSANG SUR SEINE
38255	91750	NAINVILLE LES ROCHES
38256	91290	LA NORVILLE
38257	91620	NOZAY
38258	91290	OLLAINVILLE
38259	91490	ONCY SUR ECOLE
38260	91540	ORMOY
38261	91150	ORMOY LA RIVIERE
38262	91400	ORSAY
38263	91590	ORVEAU
38264	91120	PALAISEAU
38265	91550	PARAY VIEILLE POSTE
38266	91470	PECQUEUSE
38267	91220	LE PLESSIS PATE
38268	91410	PLESSIS ST BENOIST
38269	91720	PRUNAY SUR ESSONNE
38270	91150	PUISELET LE MARAIS
38271	91740	PUSSAY
38272	91480	QUINCY SOUS SENART
38273	91410	RICHARVILLE
38274	91130	RIS ORANGIS
38275	91410	ROINVILLE
38276	91150	ROINVILLIERS
38277	91690	SACLAS
38278	91400	SACLAY
38279	91190	ST AUBIN
38280	91530	ST CHERON
38281	91690	ST CYR LA RIVIERE
38282	91410	ST CYR SOUS DOURDAN
38283	91410	STE ESCOBILLE
38284	91700	STE GENEVIEVE DES BOIS
38285	91180	ST GERMAIN LES ARPAJON
38286	91250	ST GERMAIN LES CORBEIL
38287	91780	ST HILAIRE
38288	91940	ST JEAN DE BEAUREGARD
38289	91530	ST MAURICE MONTCOURONNE
38290	91240	ST MICHEL SUR ORGE
38291	91280	ST PIERRE DU PERRAY
38292	91250	SAINTRY SUR SEINE
38293	91910	ST SULPICE DE FAVIERES
38294	91770	ST VRAIN
38295	91650	ST YON
38296	91160	SAULX LES CHARTREUX
38297	91600	SAVIGNY SUR ORGE
38298	91530	SERMAISE
38299	91840	SOISY SUR ECOLE
38300	91450	SOISY SUR SEINE
38301	91580	SOUZY LA BRICHE
38302	91740	CONGERVILLE THIONVILLE
38303	91250	TIGERY
38304	91730	TORFOU
38305	91720	VALPUISEAUX
38306	91530	LE VAL ST GERMAIN
38307	91480	VARENNES JARCY
38308	91640	VAUGRIGNEUSE
38309	91430	VAUHALLAN
38310	91820	VAYRES SUR ESSONNE
38311	91370	VERRIERES LE BUISSON
38312	91810	VERT LE GRAND
38313	91710	VERT LE PETIT
38314	91890	VIDELLES
38315	91270	VIGNEUX SUR SEINE
38316	91100	VILLABE
38317	91140	VILLEBON SUR YVETTE
38318	91580	VILLECONIN
38319	91620	LA VILLE DU BOIS
38320	91140	VILLEJUST
38321	91360	VILLEMOISSON SUR ORGE
38322	91580	VILLENEUVE SUR AUVERS
38323	91190	VILLIERS LE BACLE
38324	91700	VILLIERS SUR ORGE
38325	91170	VIRY CHATILLON
38326	91320	WISSOUS
38327	91330	YERRES
38328	91940	LES ULIS
38329	91830	LE PLESSIS CHENET
38330	91190	VILLERAS
38331	91400	ORSIGNY
38332	91940	VILLEZIERS
38333	91400	LE VAL D ALBIAN
38334	91440	MONTJAY
38335	91430	GOMMONVILLER
38336	91140	FRETAY
38337	91160	BALIZY
38338	91210	MAINVILLE
38339	92160	ANTONY
38340	92600	ASNIERES SUR SEINE
38341	92220	BAGNEUX
38342	92270	BOIS COLOMBES
38343	92100	BOULOGNE BILLANCOURT
38344	92340	BOURG LA REINE
38345	92290	CHATENAY MALABRY
38346	92320	CHATILLON
38347	92370	CHAVILLE
38348	92140	CLAMART
38349	92110	CLICHY
38350	92700	COLOMBES
38351	92400	COURBEVOIE
38352	92260	FONTENAY AUX ROSES
38353	92380	GARCHES
38354	92250	LA GARENNE COLOMBES
38355	92230	GENNEVILLIERS
38356	92130	ISSY LES MOULINEAUX
38357	92300	LEVALLOIS PERRET
38358	92240	MALAKOFF
38359	92430	MARNES LA COQUETTE
38360	92190	MEUDON
38361	92120	MONTROUGE
38362	92000	NANTERRE
38363	92200	NEUILLY SUR SEINE
38364	92350	LE PLESSIS ROBINSON
38365	92800	PUTEAUX
38366	92500	RUEIL MALMAISON
38367	92210	ST CLOUD
38368	92330	SCEAUX
38369	92310	SEVRES
38370	92150	SURESNES
38371	92170	VANVES
38372	92420	VAUCRESSON
38373	92410	VILLE D AVRAY
38374	92390	VILLENEUVE LA GARENNE
38375	92360	MEUDON LA FORET
38376	92500	BUZENVAL
38377	92140	LE PETIT CLAMART
38378	92350	ROBINSON
38379	93300	AUBERVILLIERS
38380	93600	AULNAY SOUS BOIS
38381	93170	BAGNOLET
38382	93150	LE BLANC MESNIL
38383	93000	BOBIGNY
38384	93140	BONDY
38385	93350	LE BOURGET
38386	93390	CLICHY SOUS BOIS
38387	93470	COUBRON
38388	93120	LA COURNEUVE
38389	93700	DRANCY
38390	93440	DUGNY
38391	93800	EPINAY SUR SEINE
38392	93220	GAGNY
38393	93460	GOURNAY SUR MARNE
38394	93450	L ILE ST DENIS
38395	93260	LES LILAS
38396	93190	LIVRY GARGAN
38397	93370	MONTFERMEIL
38398	93100	MONTREUIL
38399	93360	NEUILLY PLAISANCE
38400	93330	NEUILLY SUR MARNE
38401	93160	NOISY LE GRAND
38402	93130	NOISY LE SEC
38403	93500	PANTIN
38404	93320	LES PAVILLONS SOUS BOIS
38405	93380	PIERREFITTE SUR SEINE
38406	93310	LE PRE ST GERVAIS
38407	93340	LE RAINCY
38408	93230	ROMAINVILLE
38409	93110	ROSNY SOUS BOIS
38410	93200	ST DENIS
38411	93400	ST OUEN
38412	93270	SEVRAN
38413	93240	STAINS
38414	93290	TREMBLAY EN FRANCE
38415	93410	VAUJOURS
38416	93250	VILLEMOMBLE
38417	93420	VILLEPINTE
38418	93430	VILLETANEUSE
38419	93210	LA PLAINE ST DENIS
38420	94480	ABLON SUR SEINE
38421	94140	ALFORTVILLE
38422	94110	ARCUEIL
38423	94470	BOISSY ST LEGER
38424	94380	BONNEUIL SUR MARNE
38425	94360	BRY SUR MARNE
38426	94230	CACHAN
38427	94500	CHAMPIGNY SUR MARNE
38428	94220	CHARENTON LE PONT
38429	94430	CHENNEVIERES SUR MARNE
38430	94550	CHEVILLY LARUE
38431	94600	CHOISY LE ROI
38432	94000	CRETEIL
38433	94120	FONTENAY SOUS BOIS
38434	94260	FRESNES
38435	94250	GENTILLY
38436	94240	L HAY LES ROSES
38437	94200	IVRY SUR SEINE
38438	94340	JOINVILLE LE PONT
38439	94270	LE KREMLIN BICETRE
38440	94450	LIMEIL BREVANNES
38441	94700	MAISONS ALFORT
38442	94520	MANDRES LES ROSES
38443	94440	MAROLLES EN BRIE
38444	94130	NOGENT SUR MARNE
38445	94880	NOISEAU
38446	94310	ORLY
38447	94490	ORMESSON SUR MARNE
38448	94520	PERIGNY
38449	94170	LE PERREUX SUR MARNE
38450	94420	LE PLESSIS TREVISE
38451	94510	LA QUEUE EN BRIE
38452	94150	RUNGIS
38453	94160	ST MANDE
38454	94100	ST MAUR DES FOSSES
38455	94410	ST MAURICE
38456	94440	SANTENY
38457	94370	SUCY EN BRIE
38458	94320	THIAIS
38459	94460	VALENTON
38460	94440	VILLECRESNES
38461	94800	VILLEJUIF
38462	94290	VILLENEUVE LE ROI
38463	94190	VILLENEUVE ST GEORGES
38464	94350	VILLIERS SUR MARNE
38465	94300	VINCENNES
38466	94400	VITRY SUR SEINE
38467	94390	AEROPORT D ORLY
38468	94210	LA VARENNE ST HILAIRE
38469	94460	VAL POMPADOUR
38470	94500	COEUILLY
38471	94370	LES BRUYERES
38472	95450	ABLEIGES
38473	95510	AINCOURT
38474	95710	AMBLEVILLE
38475	95510	AMENUCOURT
38476	95580	ANDILLY
38477	95100	ARGENTEUIL
38478	95400	ARNOUVILLE LES GONESSE
38479	95810	ARRONVILLE
38480	95420	ARTHIES
38481	95270	ASNIERES SUR OISE
38482	95570	ATTAINVILLE
38483	95430	AUVERS SUR OISE
38484	95450	AVERNES
38485	95560	BAILLET EN FRANCE
38486	95420	BANTHELU
38487	95250	BEAUCHAMP
38488	95260	BEAUMONT SUR OISE
38489	95750	LE BELLAY EN VEXIN
38490	95270	BELLEFONTAINE
38491	95270	BELLOY EN FRANCE
38492	95340	BERNES SUR OISE
38493	95810	BERVILLE
38494	95550	BESSANCOURT
38495	95840	BETHEMONT LA FORET
38496	95870	BEZONS
38497	95000	BOISEMONT
38498	95650	BOISSY L AILLERIE
38499	95500	BONNEUIL EN FRANCE
38500	95570	BOUFFEMONT
38501	95720	BOUQUEVAL
38502	95710	BRAY ET LU
38503	95640	BREANCON
38504	95640	BRIGNANCOURT
38505	95820	BRUYERES SUR OISE
38506	95770	BUHY
38507	95430	BUTRY SUR OISE
38508	95000	CERGY
38509	95660	CHAMPAGNE SUR OISE
38510	95420	LA CHAPELLE EN VEXIN
38511	95420	CHARMONT
38512	95750	CHARS
38513	95190	CHATENAY EN FRANCE
38514	95270	CHAUMONTEL
38515	95710	CHAUSSY
38516	95560	CHAUVRY
38517	95380	CHENNEVIERES LES LOUVRES
38518	95510	CHERENCE
38519	95420	CLERY EN VEXIN
38520	95450	COMMENY
38521	95450	CONDECOURT
38522	95240	CORMEILLES EN PARISIS
38523	95830	CORMEILLES EN VEXIN
38524	95650	COURCELLES SUR VIOSNE
38525	95800	COURDIMANCHE
38526	95170	DEUIL LA BARRE
38527	95330	DOMONT
38528	95600	EAUBONNE
38529	95440	ECOUEN
38530	95880	ENGHIEN LES BAINS
38531	95300	ENNERY
38532	95380	EPIAIS LEZ LOUVRES
38533	95810	EPIAIS RHUS
38534	95270	EPINAY CHAMPLATREUX
38535	95610	ERAGNY
38536	95120	ERMONT
38537	95460	EZANVILLE
38538	95190	FONTENAY EN PARISIS
38539	95470	FOSSES
38540	95130	FRANCONVILLE
38541	95450	FREMAINVILLE
38542	95830	FREMECOURT
38543	95740	FREPILLON
38544	95530	FRETTE SUR SEINE
38545	95690	FROUVILLE
38546	95450	GADANCOURT
38547	95140	GARGES LES GONESSE
38548	95420	GENAINVILLE
38549	95650	GENICOURT
38550	95500	GONESSE
38551	95190	GOUSSAINVILLE
38552	95450	GOUZANGREZ
38553	95810	GRISY LES PLATRES
38554	95410	GROSLAY
38555	95450	GUIRY EN VEXIN
38556	95640	HARAVILLIERS
38557	95780	HAUTE ISLE
38558	95640	LE HEAULME
38559	95690	HEDOUVILLE
38560	95220	HERBLAY
38561	95300	HEROUVILLE
38562	95420	HODENT
38563	95290	L ISLE ADAM
38564	95850	JAGNY SOUS BOIS
38565	95280	JOUY LE MOUTIER
38566	95690	LABBEVILLE
38567	95270	LASSY
38568	95300	LIVILLIERS
38569	95450	LONGUESSE
38570	95380	LOUVRES
38571	95270	LUZARCHES
38572	95560	MAFFLIERS
38573	95420	MAGNY EN VEXIN
38574	95850	MAREIL EN FRANCE
38575	95580	MARGENCY
38576	95640	MARINES
38577	95670	MARLY LA VILLE
38578	95420	MAUDETOUR EN VEXIN
38579	95810	MENOUVILLE
38580	95180	MENUCOURT
38581	95630	MERIEL
38582	95540	MERY SUR OISE
38583	95720	LE MESNIL AUBRY
38584	95570	MOISSELLES
38585	95650	MONTGEROULT
38586	95370	MONTIGNY LES CORMEILLES
38587	95680	MONTLIGNON
38588	95360	MONTMAGNY
38589	95160	MONTMORENCY
38590	95770	MONTREUIL SUR EPTE
38591	95560	MONTSOULT
38592	95260	MOURS
38593	95640	MOUSSY
38594	95590	NERVILLE LA FORET
38595	95690	NESLES LA VALLEE
38596	95640	NEUILLY EN VEXIN
38597	95000	NEUVILLE SUR OISE
38598	95590	NOINTEL
38599	95270	NOISY SUR OISE
38600	95420	NUCOURT
38601	95420	OMERVILLE
38602	95520	OSNY
38603	95620	PARMAIN
38604	95450	LE PERCHAY
38605	95340	PERSAN
38606	95480	PIERRELAYE
38607	95350	PISCOP
38608	95130	LE PLESSIS BOUCHARD
38609	95720	LE PLESSIS GASSOT
38610	95270	LE PLESSIS LUZARCHES
38611	95000	PONTOISE
38612	95590	PRESLES
38613	95380	PUISEUX EN FRANCE
38614	95650	PUISEUX PONTOISE
38615	95780	LA ROCHE GUYON
38616	95700	ROISSY EN FRANCE
38617	95340	RONQUEROLLES
38618	95450	SAGY
38619	95350	ST BRICE SOUS FORET
38620	95770	ST CLAIR SUR EPTE
38621	95510	ST CYR EN ARTHIES
38622	95420	ST GERVAIS
38623	95210	ST GRATIEN
38624	95320	ST LEU LA FORET
38625	95270	ST MARTIN DU TERTRE
38626	95310	ST OUEN L AUMONE
38627	95390	ST PRIX
38628	95470	ST WITZ
38629	95110	SANNOIS
38630	95640	SANTEUIL
38631	95200	SARCELLES
38632	95450	SERAINCOURT
38633	95270	SEUGY
38634	95230	SOISY SOUS MONTMORENCY
38635	95470	SURVILLIERS
38636	95150	TAVERNY
38637	95450	THEMERICOURT
38638	95810	THEUVILLE
38639	95500	LE THILLAY
38640	95450	US
38641	95810	VALLANGOUJARD
38642	95760	VALMONDOIS
38643	95500	VAUDHERLAND
38644	95490	VAUREAL
38645	95470	VEMARS
38646	95510	VETHEUIL
38647	95270	VIARMES
38648	95510	VIENNE EN ARTHIES
38649	95450	VIGNY
38650	95570	VILLAINES SOUS BOIS
38651	95380	VILLERON
38652	95510	VILLERS EN ARTHIES
38653	95840	VILLIERS ADAM
38654	95400	VILLIERS LE BEL
38655	95720	VILLIERS LE SEC
38656	95420	WY DIT JOLI VILLAGE
38657	95700	ROISSY AEROPORT CH DE GAU
38658	95000	MENANDON
38659	95280	JOUY LA FONTAINE
38660	95280	VINCOURT
38661	95220	LA PATTE D OIE
38662	95420	LE VAUMION
32567	75001	PARIS
32568	75002	PARIS
32569	75003	PARIS
32570	75004	PARIS
32571	75005	PARIS
32572	75006	PARIS
32573	75007	PARIS
32574	75008	PARIS
32575	75009	PARIS
32576	75010	PARIS
32577	75011	PARIS
32578	75012	PARIS
32579	75013	PARIS
32580	75014	PARIS
32581	75015	PARIS
32582	75016	PARIS
32583	75017	PARIS
32584	75018	PARIS
32585	75019	PARIS
32586	75020	PARIS
\.


--
-- TOC entry 2068 (class 0 OID 16441)
-- Dependencies: 169 2090
-- Data for Name: depots_lieux_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY depots_lieux_tb (dbid_depot, dbid_lieu, quantite, destinataire) FROM stdin;
159	556	1	\N
160	556	2	\N
161	556	3	\N
159	557	3	\N
160	557	6	\N
161	557	9	\N
159	558	5	\N
160	558	10	\N
161	558	15	\N
159	559	7	\N
160	559	14	\N
161	559	21	\N
159	560	9	\N
160	560	18	\N
161	560	27	\N
159	561	11	\N
160	561	22	\N
161	561	33	\N
159	562	13	\N
160	562	26	\N
161	562	39	\N
159	563	15	\N
160	563	30	\N
161	563	45	\N
159	564	17	\N
160	564	34	\N
161	564	51	\N
159	565	19	\N
160	565	38	\N
161	565	57	\N
159	566	21	\N
160	566	42	\N
161	566	63	\N
159	567	23	\N
160	567	46	\N
161	567	69	\N
159	568	25	\N
160	568	50	\N
161	568	75	\N
159	569	27	\N
160	569	54	\N
161	569	81	\N
159	570	29	\N
160	570	58	\N
161	570	87	\N
159	571	31	\N
160	571	62	\N
161	571	93	\N
159	572	33	\N
160	572	66	\N
161	572	99	\N
159	573	35	\N
160	573	70	\N
161	573	105	\N
159	574	37	\N
160	574	74	\N
161	574	111	\N
159	575	39	\N
160	575	78	\N
161	575	117	\N
159	576	41	\N
160	576	82	\N
161	576	123	\N
159	577	43	\N
160	577	86	\N
161	577	129	\N
159	578	45	\N
160	578	90	\N
161	578	135	\N
159	579	47	\N
160	579	94	\N
161	579	141	\N
159	580	49	\N
160	580	98	\N
161	580	147	\N
159	581	51	\N
160	581	102	\N
161	581	153	\N
159	582	53	\N
160	582	106	\N
161	582	159	\N
159	583	55	\N
160	583	110	\N
161	583	165	\N
159	584	57	\N
160	584	114	\N
161	584	171	\N
159	585	59	\N
160	585	118	\N
161	585	177	\N
159	586	61	\N
160	586	122	\N
161	586	183	\N
159	587	63	\N
160	587	126	\N
161	587	189	\N
159	588	65	\N
160	588	130	\N
161	588	195	\N
159	589	67	\N
160	589	134	\N
161	589	201	\N
159	590	69	\N
160	590	138	\N
161	590	207	\N
159	591	71	\N
160	591	142	\N
161	591	213	\N
159	592	73	\N
160	592	146	\N
161	592	219	\N
159	593	75	\N
160	593	150	\N
161	593	225	\N
159	594	77	\N
160	594	154	\N
161	594	231	\N
159	595	79	\N
160	595	158	\N
161	595	237	\N
159	596	81	\N
160	596	162	\N
161	596	243	\N
159	597	83	\N
160	597	166	\N
161	597	249	\N
159	598	85	\N
160	598	170	\N
161	598	255	\N
159	599	87	\N
160	599	174	\N
161	599	261	\N
159	600	89	\N
160	600	178	\N
161	600	267	\N
159	601	91	\N
160	601	182	\N
161	601	273	\N
159	602	93	\N
160	602	186	\N
161	602	279	\N
159	603	95	\N
160	603	190	\N
161	603	285	\N
159	604	97	\N
160	604	194	\N
161	604	291	\N
159	605	99	\N
160	605	198	\N
161	605	297	\N
159	606	101	\N
160	606	202	\N
161	606	303	\N
159	607	103	\N
160	607	206	\N
161	607	309	\N
159	608	105	\N
160	608	210	\N
161	608	315	\N
159	609	107	\N
160	609	214	\N
161	609	321	\N
159	610	109	\N
160	610	218	\N
161	610	327	\N
159	611	111	\N
160	611	222	\N
161	611	333	\N
159	612	113	\N
160	612	226	\N
161	612	339	\N
159	613	115	\N
160	613	230	\N
161	613	345	\N
159	614	117	\N
160	614	234	\N
161	614	351	\N
159	615	119	\N
160	615	238	\N
161	615	357	\N
159	616	121	\N
160	616	242	\N
161	616	363	\N
159	617	123	\N
160	617	246	\N
161	617	369	\N
159	618	125	\N
160	618	250	\N
161	618	375	\N
159	619	127	\N
160	619	254	\N
161	619	381	\N
159	620	129	\N
160	620	258	\N
161	620	387	\N
159	621	131	\N
160	621	262	\N
161	621	393	\N
159	622	133	\N
160	622	266	\N
161	622	399	\N
159	623	135	\N
160	623	270	\N
161	623	405	\N
159	624	137	\N
160	624	274	\N
161	624	411	\N
159	625	139	\N
160	625	278	\N
161	625	417	\N
159	626	141	\N
160	626	282	\N
161	626	423	\N
159	627	143	\N
160	627	286	\N
161	627	429	\N
159	628	145	\N
160	628	290	\N
161	628	435	\N
159	629	147	\N
160	629	294	\N
161	629	441	\N
159	630	149	\N
160	630	298	\N
161	630	447	\N
162	568	4	\N
163	568	5	\N
164	568	6	\N
162	569	5	\N
163	569	6	\N
164	569	7	\N
162	570	6	\N
163	570	7	\N
164	570	8	\N
162	571	7	\N
163	571	8	\N
164	571	9	\N
162	572	8	\N
163	572	9	\N
164	572	10	\N
162	573	9	\N
163	573	10	\N
164	573	11	\N
162	574	10	\N
163	574	11	\N
164	574	12	\N
162	575	11	\N
163	575	12	\N
164	575	13	\N
162	576	12	\N
163	576	13	\N
164	576	14	\N
162	577	13	\N
163	577	14	\N
164	577	15	\N
162	578	14	\N
163	578	15	\N
164	578	16	\N
162	579	15	\N
163	579	16	\N
164	579	17	\N
162	580	16	\N
163	580	17	\N
164	580	18	\N
162	581	17	\N
163	581	18	\N
164	581	19	\N
162	582	18	\N
163	582	19	\N
164	582	20	\N
162	583	19	\N
163	583	20	\N
164	583	21	\N
162	584	20	\N
163	584	21	\N
164	584	22	\N
162	585	21	\N
163	585	22	\N
164	585	23	\N
162	586	22	\N
163	586	23	\N
164	586	24	\N
162	587	23	\N
163	587	24	\N
164	587	25	\N
162	588	24	\N
163	588	25	\N
164	588	26	\N
162	589	25	\N
163	589	26	\N
164	589	27	\N
162	590	26	\N
163	590	27	\N
164	590	28	\N
162	591	27	\N
163	591	28	\N
164	591	29	\N
162	592	28	\N
163	592	29	\N
164	592	30	\N
162	593	29	\N
163	593	30	\N
164	593	31	\N
162	594	30	\N
163	594	31	\N
164	594	32	\N
162	595	31	\N
163	595	32	\N
164	595	33	\N
162	596	32	\N
163	596	33	\N
164	596	34	\N
162	597	33	\N
163	597	34	\N
164	597	35	\N
162	598	34	\N
163	598	35	\N
164	598	36	\N
162	599	35	\N
163	599	36	\N
164	599	37	\N
162	600	36	\N
163	600	37	\N
164	600	38	\N
162	601	37	\N
163	601	38	\N
164	601	39	\N
162	602	38	\N
163	602	39	\N
164	602	40	\N
162	631	39	\N
163	631	40	\N
164	631	41	\N
162	604	40	\N
163	604	41	\N
164	604	42	\N
162	605	41	\N
163	605	42	\N
164	605	43	\N
162	606	42	\N
163	606	43	\N
164	606	44	\N
162	607	43	\N
163	607	44	\N
164	607	45	\N
162	608	44	\N
163	608	45	\N
164	608	46	\N
162	609	45	\N
163	609	46	\N
164	609	47	\N
162	610	46	\N
163	610	47	\N
164	610	48	\N
162	611	47	\N
163	611	48	\N
164	611	49	\N
162	612	48	\N
163	612	49	\N
164	612	50	\N
162	632	49	\N
163	632	50	\N
164	632	51	\N
162	614	50	\N
163	614	51	\N
164	614	52	\N
162	615	51	\N
163	615	52	\N
164	615	53	\N
162	616	52	\N
163	616	53	\N
164	616	54	\N
162	617	53	\N
163	617	54	\N
164	617	55	\N
162	618	54	\N
163	618	55	\N
164	618	56	\N
165	595	1000	\N
169	633	4	\N
170	633	5	\N
171	633	6	\N
169	634	5	\N
170	634	6	\N
171	634	7	\N
169	635	6	\N
170	635	7	\N
171	635	8	\N
169	636	7	\N
170	636	8	\N
171	636	9	\N
169	637	8	\N
170	637	9	\N
171	637	10	\N
169	638	9	\N
170	638	10	\N
171	638	11	\N
169	639	10	\N
170	639	11	\N
171	639	12	\N
169	640	11	\N
170	640	12	\N
171	640	13	\N
169	641	12	\N
170	641	13	\N
171	641	14	\N
169	642	13	\N
170	642	14	\N
171	642	15	\N
169	643	14	\N
170	643	15	\N
171	643	16	\N
169	644	15	\N
170	644	16	\N
171	644	17	\N
169	645	16	\N
170	645	17	\N
171	645	18	\N
169	646	17	\N
170	646	18	\N
171	646	19	\N
169	647	18	\N
170	647	19	\N
171	647	20	\N
169	648	19	\N
170	648	20	\N
171	648	21	\N
169	649	20	\N
170	649	21	\N
171	649	22	\N
169	650	21	\N
170	650	22	\N
171	650	23	\N
169	651	22	\N
170	651	23	\N
171	651	24	\N
169	652	23	\N
170	652	24	\N
171	652	25	\N
169	653	24	\N
170	653	25	\N
171	653	26	\N
169	654	25	\N
170	654	26	\N
171	654	27	\N
169	655	26	\N
170	655	27	\N
171	655	28	\N
169	656	27	\N
170	656	28	\N
171	656	29	\N
169	657	28	\N
170	657	29	\N
171	657	30	\N
169	658	29	\N
170	658	30	\N
171	658	31	\N
169	659	30	\N
170	659	31	\N
171	659	32	\N
169	660	31	\N
170	660	32	\N
171	660	33	\N
169	661	32	\N
170	661	33	\N
171	661	34	\N
169	662	33	\N
170	662	34	\N
171	662	35	\N
169	663	34	\N
170	663	35	\N
171	663	36	\N
169	664	35	\N
170	664	36	\N
171	664	37	\N
169	665	36	\N
170	665	37	\N
171	665	38	\N
169	666	37	\N
170	666	38	\N
171	666	39	\N
169	667	38	\N
170	667	39	\N
171	667	40	\N
169	668	39	\N
170	668	40	\N
171	668	41	\N
169	669	40	\N
170	669	41	\N
171	669	42	\N
169	670	41	\N
170	670	42	\N
171	670	43	\N
169	671	42	\N
170	671	43	\N
171	671	44	\N
169	672	43	\N
170	672	44	\N
171	672	45	\N
169	673	44	\N
170	673	45	\N
171	673	46	\N
169	674	45	\N
170	674	46	\N
171	674	47	\N
169	675	46	\N
170	675	47	\N
171	675	48	\N
169	676	47	\N
170	676	48	\N
171	676	49	\N
169	677	48	\N
170	677	49	\N
171	677	50	\N
169	678	49	\N
170	678	50	\N
171	678	51	\N
169	679	50	\N
170	679	51	\N
171	679	52	\N
169	680	51	\N
170	680	52	\N
171	680	53	\N
169	681	52	\N
170	681	53	\N
171	681	54	\N
169	682	53	\N
170	682	54	\N
171	682	55	\N
169	683	54	\N
170	683	55	\N
171	683	56	\N
169	684	55	\N
170	684	56	\N
171	684	57	\N
169	685	56	\N
170	685	57	\N
171	685	58	\N
169	686	57	\N
170	686	58	\N
171	686	59	\N
169	687	58	\N
170	687	59	\N
171	687	60	\N
169	688	59	\N
170	688	60	\N
171	688	61	\N
169	689	60	\N
170	689	61	\N
171	689	62	\N
169	690	61	\N
170	690	62	\N
171	690	63	\N
169	691	62	\N
170	691	63	\N
171	691	64	\N
169	692	63	\N
170	692	64	\N
171	692	65	\N
169	693	64	\N
170	693	65	\N
171	693	66	\N
169	694	65	\N
170	694	66	\N
171	694	67	\N
169	695	66	\N
170	695	67	\N
171	695	68	\N
169	696	67	\N
170	696	68	\N
171	696	69	\N
169	697	68	\N
170	697	69	\N
171	697	70	\N
169	698	69	\N
170	698	70	\N
171	698	71	\N
169	699	70	\N
170	699	71	\N
171	699	72	\N
169	700	71	\N
170	700	72	\N
171	700	73	\N
169	701	72	\N
170	701	73	\N
171	701	74	\N
169	702	73	\N
170	702	74	\N
171	702	75	\N
169	703	74	\N
170	703	75	\N
171	703	76	\N
169	704	75	\N
170	704	76	\N
171	704	77	\N
172	705	20	\N
173	705	20	\N
174	705	20	\N
172	636	22	\N
173	636	22	\N
174	636	22	\N
172	706	23	\N
173	706	23	\N
174	706	23	\N
172	707	24	\N
173	707	24	\N
174	707	24	\N
172	708	25	\N
173	708	25	\N
174	708	25	\N
172	709	26	\N
173	709	26	\N
174	709	26	\N
172	710	27	\N
173	710	27	\N
174	710	27	\N
172	711	28	\N
173	711	28	\N
174	711	28	\N
172	712	29	\N
173	712	29	\N
174	712	29	\N
172	713	32	\N
173	713	32	\N
174	713	32	\N
172	714	33	\N
173	714	33	\N
174	714	33	\N
172	715	34	\N
173	715	34	\N
174	715	34	\N
172	716	35	\N
173	716	35	\N
174	716	35	\N
172	717	36	\N
173	717	36	\N
174	717	36	\N
172	718	37	\N
173	718	37	\N
174	718	37	\N
172	570	38	\N
173	570	38	\N
174	570	38	\N
172	719	39	\N
173	719	39	\N
174	719	39	\N
172	639	40	\N
173	639	40	\N
174	639	40	\N
172	720	41	\N
173	720	41	\N
174	720	41	\N
172	721	42	\N
173	721	42	\N
174	721	42	\N
172	722	43	\N
173	722	43	\N
174	722	43	\N
172	723	44	\N
173	723	44	\N
174	723	44	\N
172	724	45	\N
173	724	45	\N
174	724	45	\N
172	725	46	\N
173	725	46	\N
174	725	46	\N
172	726	47	\N
173	726	47	\N
174	726	47	\N
172	727	48	\N
173	727	48	\N
174	727	48	\N
172	728	49	\N
173	728	49	\N
174	728	49	\N
172	729	50	\N
173	729	50	\N
174	729	50	\N
172	730	51	\N
173	730	51	\N
174	730	51	\N
172	731	52	\N
173	731	52	\N
174	731	52	\N
172	732	53	\N
173	732	53	\N
174	732	53	\N
172	733	54	\N
173	733	54	\N
174	733	54	\N
172	734	55	\N
173	734	55	\N
174	734	55	\N
172	735	56	\N
173	735	56	\N
174	735	56	\N
172	736	57	\N
173	736	57	\N
174	736	57	\N
172	737	58	\N
173	737	58	\N
174	737	58	\N
172	738	59	\N
173	738	59	\N
174	738	59	\N
172	739	60	\N
173	739	60	\N
174	739	60	\N
172	740	61	\N
173	740	61	\N
174	740	61	\N
172	741	62	\N
173	741	62	\N
174	741	62	\N
172	742	63	\N
173	742	63	\N
174	742	63	\N
172	743	64	\N
173	743	64	\N
174	743	64	\N
172	744	65	\N
173	744	65	\N
174	744	65	\N
172	745	66	\N
173	745	66	\N
174	745	66	\N
172	746	67	\N
173	746	67	\N
174	746	67	\N
172	747	68	\N
173	747	68	\N
174	747	68	\N
172	748	69	\N
173	748	69	\N
174	748	69	\N
172	749	70	\N
173	749	70	\N
174	749	70	\N
172	750	71	\N
173	750	71	\N
174	750	71	\N
172	751	72	\N
173	751	72	\N
174	751	72	\N
172	752	73	\N
173	752	73	\N
174	752	73	\N
172	753	74	\N
173	753	74	\N
174	753	74	\N
172	754	75	\N
173	754	75	\N
174	754	75	\N
172	755	76	\N
173	755	76	\N
174	755	76	\N
172	756	77	\N
173	756	77	\N
174	756	77	\N
172	757	78	\N
173	757	78	\N
174	757	78	\N
172	758	79	\N
173	758	79	\N
174	758	79	\N
172	759	80	\N
173	759	80	\N
174	759	80	\N
172	760	81	\N
173	760	81	\N
174	760	81	\N
172	761	82	\N
173	761	82	\N
174	761	82	\N
172	762	83	\N
173	762	83	\N
174	762	83	\N
172	663	84	\N
173	663	84	\N
174	663	84	\N
172	763	85	\N
173	763	85	\N
174	763	85	\N
172	764	86	\N
173	764	86	\N
174	764	86	\N
172	765	87	\N
173	765	87	\N
174	765	87	\N
172	766	88	\N
173	766	88	\N
174	766	88	\N
172	767	89	\N
173	767	89	\N
174	767	89	\N
172	768	90	\N
173	768	90	\N
174	768	90	\N
172	769	91	\N
173	769	91	\N
174	769	91	\N
172	770	92	\N
173	770	92	\N
174	770	92	\N
172	771	93	\N
173	771	93	\N
174	771	93	\N
172	772	94	\N
173	772	94	\N
174	772	94	\N
172	773	95	\N
173	773	95	\N
174	773	95	\N
172	681	96	\N
173	681	96	\N
174	681	96	\N
172	774	97	\N
173	774	97	\N
174	774	97	\N
172	559	98	\N
173	559	98	\N
174	559	98	\N
172	775	99	\N
173	775	99	\N
174	775	99	\N
172	776	100	\N
173	776	100	\N
174	776	100	\N
172	777	101	\N
173	777	101	\N
174	777	101	\N
172	778	102	\N
173	778	102	\N
174	778	102	\N
172	779	103	\N
173	779	103	\N
174	779	103	\N
172	780	104	\N
173	780	104	\N
174	780	104	\N
172	781	105	\N
173	781	105	\N
174	781	105	\N
172	782	106	\N
173	782	106	\N
174	782	106	\N
172	783	107	\N
173	783	107	\N
174	783	107	\N
172	784	108	\N
173	784	108	\N
174	784	108	\N
172	785	109	\N
173	785	109	\N
174	785	109	\N
172	786	110	\N
173	786	110	\N
174	786	110	\N
172	787	111	\N
173	787	111	\N
174	787	111	\N
172	788	112	\N
173	788	112	\N
174	788	112	\N
172	789	113	\N
173	789	113	\N
174	789	113	\N
172	790	114	\N
173	790	114	\N
174	790	114	\N
172	791	115	\N
173	791	115	\N
174	791	115	\N
172	560	116	\N
173	560	116	\N
174	560	116	\N
172	792	117	\N
173	792	117	\N
174	792	117	\N
172	793	118	\N
173	793	118	\N
174	793	118	\N
172	794	119	\N
173	794	119	\N
174	794	119	\N
172	795	120	\N
173	795	120	\N
174	795	120	\N
172	796	121	\N
173	796	121	\N
174	796	121	\N
172	797	122	\N
173	797	122	\N
174	797	122	\N
172	798	123	\N
173	798	123	\N
174	798	123	\N
172	799	124	\N
173	799	124	\N
174	799	124	\N
172	800	125	\N
173	800	125	\N
174	800	125	\N
172	801	126	\N
173	801	126	\N
174	801	126	\N
172	562	127	\N
173	562	127	\N
174	562	127	\N
172	630	128	\N
173	630	128	\N
174	630	128	\N
172	802	129	\N
173	802	129	\N
174	802	129	\N
172	803	131	\N
173	803	131	\N
174	803	131	\N
172	804	132	\N
173	804	132	\N
174	804	132	\N
172	805	133	\N
173	805	133	\N
174	805	133	\N
172	806	134	\N
173	806	134	\N
174	806	134	\N
172	807	135	\N
173	807	135	\N
174	807	135	\N
172	808	136	\N
173	808	136	\N
174	808	136	\N
172	809	137	\N
173	809	137	\N
174	809	137	\N
172	810	138	\N
173	810	138	\N
174	810	138	\N
172	567	139	\N
173	567	139	\N
174	567	139	\N
172	811	140	\N
173	811	140	\N
174	811	140	\N
172	812	141	\N
173	812	141	\N
174	812	141	\N
172	813	142	\N
173	813	142	\N
174	813	142	\N
172	814	143	\N
173	814	143	\N
174	814	143	\N
172	569	144	\N
173	569	144	\N
174	569	144	\N
172	697	145	\N
173	697	145	\N
174	697	145	\N
172	815	146	\N
173	815	146	\N
174	815	146	\N
172	816	147	\N
173	816	147	\N
174	816	147	\N
172	817	148	\N
173	817	148	\N
174	817	148	\N
172	818	149	\N
173	818	149	\N
174	818	149	\N
172	819	150	\N
173	819	150	\N
174	819	150	\N
172	820	151	\N
173	820	151	\N
174	820	151	\N
172	821	152	\N
173	821	152	\N
174	821	152	\N
172	822	153	\N
173	822	153	\N
174	822	153	\N
172	823	154	\N
173	823	154	\N
174	823	154	\N
172	824	155	\N
173	824	155	\N
174	824	155	\N
172	825	156	\N
173	825	156	\N
174	825	156	\N
172	826	157	\N
173	826	157	\N
174	826	157	\N
172	827	158	\N
173	827	158	\N
174	827	158	\N
172	828	159	\N
173	828	159	\N
174	828	159	\N
172	829	160	\N
173	829	160	\N
174	829	160	\N
197	894	6	\N
198	894	8	\N
184	568	4	\N
185	568	5	\N
199	894	10	\N
184	569	5	\N
185	569	6	\N
186	569	7	\N
184	570	6	\N
185	570	7	\N
186	570	8	\N
184	571	7	\N
185	571	8	\N
186	571	9	\N
184	572	8	\N
185	572	9	\N
186	572	10	\N
184	573	9	\N
185	573	10	\N
186	573	11	\N
184	574	10	\N
185	574	11	\N
186	574	12	\N
184	575	11	\N
185	575	12	\N
186	575	13	\N
184	576	12	\N
185	576	13	\N
186	576	14	\N
184	577	13	\N
185	577	14	\N
186	577	15	\N
184	578	14	\N
185	578	15	\N
186	578	16	\N
184	579	15	\N
185	579	16	\N
186	579	17	\N
184	580	16	\N
185	580	17	\N
186	580	18	\N
184	581	17	\N
185	581	18	\N
186	581	19	\N
184	582	18	\N
185	582	19	\N
186	582	20	\N
184	583	19	\N
185	583	20	\N
186	583	21	\N
184	584	20	\N
185	584	21	\N
186	584	22	\N
184	585	21	\N
185	585	22	\N
186	585	23	\N
184	586	22	\N
185	586	23	\N
186	586	24	\N
184	587	23	\N
185	587	24	\N
186	587	25	\N
184	588	24	\N
185	588	25	\N
186	588	26	\N
184	589	25	\N
185	589	26	\N
186	589	27	\N
184	590	26	\N
185	590	27	\N
186	590	28	\N
184	591	27	\N
185	591	28	\N
186	591	29	\N
184	592	28	\N
185	592	29	\N
186	592	30	\N
184	593	29	\N
185	593	30	\N
186	593	31	\N
184	594	30	\N
185	594	31	\N
186	594	32	\N
184	595	31	\N
185	595	32	\N
186	595	33	\N
184	596	32	\N
185	596	33	\N
197	779	8	\N
184	597	33	\N
185	597	34	\N
186	597	35	\N
184	598	34	\N
185	598	35	\N
186	598	36	\N
184	599	35	\N
185	599	36	\N
186	599	37	\N
184	600	36	\N
185	600	37	\N
186	600	38	\N
184	601	37	\N
185	601	38	\N
186	601	39	\N
184	602	38	\N
185	602	39	\N
186	602	40	\N
184	631	39	\N
185	631	40	\N
184	604	40	\N
185	604	41	\N
186	604	42	\N
184	605	41	\N
185	605	42	\N
186	605	43	\N
184	606	42	\N
185	606	43	\N
186	606	44	\N
184	607	43	\N
185	607	44	\N
186	607	45	\N
184	608	44	\N
185	608	45	\N
184	609	45	\N
185	609	46	\N
186	609	47	\N
184	610	46	\N
185	610	47	\N
186	610	48	\N
184	611	47	\N
185	611	48	\N
186	611	49	\N
184	612	48	\N
185	612	49	\N
186	612	50	\N
184	632	49	\N
185	632	50	\N
186	632	51	\N
184	614	50	\N
185	614	51	\N
186	614	52	\N
184	615	51	\N
185	615	52	\N
186	615	53	\N
184	616	52	\N
185	616	53	\N
186	616	54	\N
184	617	53	\N
185	617	54	\N
186	617	55	\N
184	618	54	\N
185	618	55	\N
186	618	56	\N
198	779	10	\N
186	608	444	\N
186	596	8888	\N
186	631	999999	\N
194	705	20	\N
195	705	20	\N
196	705	20	\N
194	570	21	\N
195	570	21	\N
196	570	21	\N
194	636	22	\N
195	636	22	\N
196	636	22	\N
194	706	23	\N
195	706	23	\N
196	706	23	\N
194	707	24	\N
195	707	24	\N
196	707	24	\N
194	708	25	\N
195	708	25	\N
196	708	25	\N
194	709	26	\N
195	709	26	\N
196	709	26	\N
194	710	27	\N
195	710	27	\N
196	710	27	\N
194	711	28	\N
195	711	28	\N
196	711	28	\N
194	712	29	\N
195	712	29	\N
196	712	29	\N
194	713	32	\N
195	713	32	\N
196	713	32	\N
194	714	33	\N
195	714	33	\N
196	714	33	\N
194	715	34	\N
195	715	34	\N
196	715	34	\N
194	716	35	\N
195	716	35	\N
196	716	35	\N
194	717	36	\N
195	717	36	\N
196	717	36	\N
194	718	37	\N
195	718	37	\N
196	718	37	\N
194	719	39	\N
195	719	39	\N
196	719	39	\N
194	639	40	\N
195	639	40	\N
196	639	40	\N
194	720	41	\N
195	720	41	\N
196	720	41	\N
194	721	42	\N
195	721	42	\N
196	721	42	\N
194	722	43	\N
195	722	43	\N
196	722	43	\N
194	723	44	\N
195	723	44	\N
196	723	44	\N
194	724	45	\N
195	724	45	\N
196	724	45	\N
194	725	46	\N
195	725	46	\N
196	725	46	\N
194	726	47	\N
195	726	47	\N
196	726	47	\N
194	727	48	\N
195	727	48	\N
196	727	48	\N
194	728	49	\N
195	728	49	\N
196	728	49	\N
194	729	50	\N
195	729	50	\N
196	729	50	\N
194	730	51	\N
195	730	51	\N
196	730	51	\N
194	731	52	\N
195	731	52	\N
196	731	52	\N
194	732	53	\N
195	732	53	\N
196	732	53	\N
194	733	54	\N
195	733	54	\N
196	733	54	\N
194	734	55	\N
195	734	55	\N
196	734	55	\N
194	735	56	\N
195	735	56	\N
196	735	56	\N
194	736	57	\N
195	736	57	\N
194	737	58	\N
195	737	58	\N
196	737	58	\N
194	738	59	\N
195	738	59	\N
196	738	59	\N
194	739	60	\N
195	739	60	\N
196	739	60	\N
194	740	61	\N
195	740	61	\N
196	740	61	\N
194	741	62	\N
195	741	62	\N
196	741	62	\N
194	742	63	\N
195	742	63	\N
196	742	63	\N
194	743	64	\N
195	743	64	\N
196	743	64	\N
194	744	65	\N
195	744	65	\N
196	744	65	\N
194	745	66	\N
199	779	12	\N
197	895	10	\N
195	745	66	\N
196	745	66	\N
194	746	67	\N
195	746	67	\N
196	746	67	\N
194	747	68	\N
195	747	68	\N
196	747	68	\N
194	748	69	\N
195	748	69	\N
196	748	69	\N
194	749	70	\N
195	749	70	\N
196	749	70	\N
194	750	71	\N
195	750	71	\N
196	750	71	\N
194	751	72	\N
195	751	72	\N
196	751	72	\N
194	752	73	\N
195	752	73	\N
196	752	73	\N
194	753	74	\N
195	753	74	\N
196	753	74	\N
194	754	75	\N
195	754	75	\N
196	754	75	\N
194	755	76	\N
195	755	76	\N
196	755	76	\N
194	756	77	\N
195	756	77	\N
196	756	77	\N
194	757	78	\N
195	757	78	\N
196	757	78	\N
194	758	79	\N
195	758	79	\N
196	758	79	\N
194	759	80	\N
195	759	80	\N
196	759	80	\N
194	760	81	\N
195	760	81	\N
196	760	81	\N
194	761	82	\N
195	761	82	\N
196	761	82	\N
194	762	83	\N
195	762	83	\N
196	762	83	\N
194	663	84	\N
195	663	84	\N
196	663	84	\N
194	763	85	\N
195	763	85	\N
196	763	85	\N
194	764	86	\N
195	764	86	\N
196	764	86	\N
194	765	87	\N
195	765	87	\N
196	765	87	\N
194	767	89	\N
195	767	89	\N
196	767	89	\N
194	768	90	\N
195	768	90	\N
196	768	90	\N
194	769	91	\N
195	769	91	\N
196	769	91	\N
194	770	92	\N
195	770	92	\N
196	770	92	\N
194	771	93	\N
195	771	93	\N
196	771	93	\N
194	772	94	\N
195	772	94	\N
196	772	94	\N
194	773	95	\N
195	773	95	\N
196	773	95	\N
194	681	96	\N
195	681	96	\N
196	681	96	\N
194	774	97	\N
196	774	97	\N
194	559	98	\N
195	559	98	\N
196	559	98	\N
194	775	99	\N
195	775	99	\N
196	775	99	\N
194	776	100	\N
195	776	100	\N
196	776	100	\N
194	777	101	\N
195	777	101	\N
196	777	101	\N
194	778	102	\N
195	778	102	\N
196	778	102	\N
194	779	103	\N
195	779	103	\N
196	779	103	\N
194	780	104	\N
195	780	104	\N
196	780	104	\N
194	781	105	\N
195	781	105	\N
196	781	105	\N
194	782	106	\N
195	782	106	\N
196	782	106	\N
194	783	107	\N
195	783	107	\N
196	783	107	\N
194	784	108	\N
195	784	108	\N
196	784	108	\N
194	786	110	\N
195	786	110	\N
196	786	110	\N
194	787	111	\N
195	787	111	\N
196	787	111	\N
194	788	112	\N
195	788	112	\N
196	788	112	\N
194	789	113	\N
195	789	113	\N
196	789	113	\N
194	790	114	\N
195	790	114	\N
196	790	114	\N
194	791	115	\N
195	791	115	\N
196	791	115	\N
194	560	116	\N
195	560	116	\N
196	560	116	\N
194	792	117	\N
195	792	117	\N
196	792	117	\N
194	793	118	\N
195	793	118	\N
196	793	118	\N
194	794	119	\N
195	794	119	\N
196	794	119	\N
194	796	121	\N
195	796	121	\N
196	796	121	\N
194	797	122	\N
195	797	122	\N
196	797	122	\N
194	798	123	\N
195	798	123	\N
196	798	123	\N
194	799	124	\N
195	799	124	\N
196	799	124	\N
194	800	125	\N
195	800	125	\N
196	800	125	\N
194	801	126	\N
195	801	126	\N
196	801	126	\N
194	562	127	\N
195	562	127	\N
196	562	127	\N
194	630	128	\N
195	630	128	\N
196	630	128	\N
194	802	129	\N
195	802	129	\N
196	802	129	\N
194	697	130	\N
195	697	130	\N
196	697	130	\N
194	804	132	\N
195	804	132	\N
196	804	132	\N
194	805	133	\N
195	805	133	\N
196	805	133	\N
194	806	134	\N
195	806	134	\N
196	806	134	\N
194	807	135	\N
195	807	135	\N
196	807	135	\N
194	808	136	\N
195	808	136	\N
196	808	136	\N
194	809	137	\N
195	809	137	\N
196	809	137	\N
194	810	138	\N
195	810	138	\N
196	810	138	\N
194	567	139	\N
195	567	139	\N
196	567	139	\N
194	811	140	\N
195	811	140	\N
196	811	140	\N
194	812	141	\N
195	812	141	\N
196	812	141	\N
194	813	142	\N
195	813	142	\N
196	813	142	\N
194	814	143	\N
195	814	143	\N
196	814	143	\N
194	569	144	\N
195	569	144	\N
196	569	144	\N
194	815	146	\N
195	815	146	\N
196	815	146	\N
194	816	147	\N
195	816	147	\N
196	816	147	\N
194	817	148	\N
195	817	148	\N
196	817	148	\N
194	818	149	\N
195	818	149	\N
196	818	149	\N
194	819	150	\N
195	819	150	\N
196	819	150	\N
194	820	151	\N
195	820	151	\N
196	820	151	\N
194	823	154	\N
195	823	154	\N
196	823	154	\N
194	824	155	\N
195	824	155	\N
196	824	155	\N
194	825	156	\N
195	825	156	\N
196	825	156	\N
194	826	157	\N
195	826	157	\N
196	826	157	\N
194	827	158	\N
195	827	158	\N
196	827	158	\N
194	828	159	\N
195	828	159	\N
196	828	159	\N
194	829	160	\N
195	829	160	\N
181	769	10	\N
193	584	1	\N
192	618	45	\N
196	829	1	\N
198	895	12	\N
199	895	14	\N
197	786	12	\N
198	786	14	\N
199	786	16	\N
197	796	14	\N
198	796	16	\N
199	796	18	\N
197	889	16	\N
198	889	18	\N
199	889	20	\N
197	896	18	\N
198	896	20	\N
199	896	22	\N
197	817	20	\N
198	817	22	\N
199	817	24	\N
197	806	22	\N
198	806	24	\N
199	806	26	\N
197	615	24	\N
198	615	26	\N
199	615	28	\N
197	809	26	\N
198	809	28	\N
199	809	30	\N
197	897	28	\N
198	897	30	\N
199	897	32	\N
197	898	30	\N
198	898	32	\N
199	898	34	\N
197	899	32	\N
198	899	34	\N
199	899	36	\N
197	810	34	\N
198	810	36	\N
199	810	38	\N
197	813	36	\N
198	813	38	\N
199	813	40	\N
197	812	38	\N
198	812	40	\N
199	812	42	\N
197	567	40	\N
198	567	42	\N
199	567	44	\N
197	826	42	\N
198	826	44	\N
199	826	46	\N
197	703	44	\N
198	703	46	\N
199	703	48	\N
197	900	46	\N
198	900	48	\N
199	900	50	\N
197	901	48	\N
198	901	50	\N
199	901	52	\N
197	625	50	\N
198	625	52	\N
199	625	54	\N
197	902	52	\N
198	902	54	\N
199	902	56	\N
197	903	54	\N
198	903	56	\N
199	903	58	\N
197	904	56	\N
198	904	58	\N
199	904	60	\N
197	905	58	\N
198	905	60	\N
199	905	62	\N
197	906	60	\N
198	906	62	\N
199	906	64	\N
197	907	62	\N
198	907	64	\N
199	907	66	\N
197	908	64	\N
198	908	66	\N
199	908	68	\N
197	909	66	\N
198	909	68	\N
199	909	70	\N
197	910	68	\N
198	910	70	\N
199	910	72	\N
197	911	70	\N
198	911	72	\N
199	911	74	\N
197	912	72	\N
198	912	74	\N
199	912	76	\N
197	913	74	\N
198	913	76	\N
199	913	78	\N
197	914	76	\N
198	914	78	\N
199	914	80	\N
197	915	78	\N
198	915	80	\N
199	915	82	\N
197	916	80	\N
198	916	82	\N
199	916	84	\N
197	917	82	\N
198	917	84	\N
199	917	86	\N
197	918	84	\N
198	918	86	\N
199	918	88	\N
197	919	86	\N
198	919	88	\N
199	919	90	\N
197	920	88	\N
198	920	90	\N
199	920	92	\N
197	828	90	\N
198	828	92	\N
199	828	94	\N
197	921	92	\N
198	921	94	\N
199	921	96	\N
197	922	96	\N
198	922	98	\N
199	922	100	\N
197	923	98	\N
198	923	100	\N
199	923	102	\N
197	769	100	\N
198	769	102	\N
199	769	104	\N
197	924	102	\N
198	924	104	\N
199	924	106	\N
197	925	104	\N
198	925	106	\N
199	925	108	\N
197	696	106	\N
198	696	108	\N
199	696	110	\N
197	926	108	\N
198	926	110	\N
199	926	112	\N
197	927	110	\N
198	927	112	\N
199	927	114	\N
197	699	112	\N
198	699	114	\N
199	699	116	\N
197	928	114	\N
198	928	116	\N
199	928	118	\N
197	929	116	\N
198	929	118	\N
199	929	120	\N
197	814	118	\N
198	814	120	\N
199	814	122	\N
197	930	120	\N
198	930	122	\N
199	930	124	\N
197	931	122	\N
198	931	124	\N
199	931	126	\N
197	932	122	\N
198	932	124	\N
199	932	126	\N
196	736	12	\N
200	741	50	\N
200	772	8	\N
\.


--
-- TOC entry 2070 (class 0 OID 16449)
-- Dependencies: 171 2090
-- Data for Name: depots_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY depots_tb (dbid, nom, surnom, volume, poid, prix_unite, dbid_genre, dbid_contrat, nb_paquet, nb_carton, quantite, remarque) FROM stdin;
159	Clemenceau	DP	99	12	0.5	1	54	0	2	1000	ha oui
161	Staline	DS	999	4	0.200000003	4	54	0	3	2000	ha bof
160	Kroutcheff	DC	99.9899979	11	2.9000001	1	54	0	5	99	ha non 
162	Asterix	AST	99	12	0.5	1	55	0	2	1000	ha oui
163	Superman	SUP	999	11	0.899999976	3	55	0	5	3000	ha non 
164	Muscorsss	MUSC	99.9899979	4	0.200000003	1	55	0	3	99	ha bof
169	Depress	DEP	99	12	0.5	1	57	0	2	1000	ha oui
170	Kill me	KM	999	11	0.899999976	3	57	0	5	3000	ha non 
166	Depress	DEP	99	12	0.5	1	59	0	2	1000	ha oui
167	Kill me	KM	999	11	0.899999976	3	59	0	5	3000	ha non 
168	Rip me	RM	999	4	0.200000003	4	59	0	3	2000	ha bof
175	Polux	POL	99	12	0.5	1	58	0	2	1000	ha oui
196	Nécrose	NEC	99.9899979	4	1	1	68	0	3	99	ha bof
176	Astral	AST	999	11	0.899999976	3	58	0	5	3000	ha non 
177	Polux	POL	99	12	0.5	1	58	0	2	1000	ha oui
178	Astral	AST	999	11	0.899999976	3	58	0	5	3000	ha non 
179	Polux	POL	99	12	0.5	1	55	0	2	1000	ha oui
180	Astral	AST	999	11	0.899999976	3	55	0	5	3000	ha non 
181	Polux	POL	99	12	0.5	1	56	0	2	1000	ha oui
182	Astral	AST	999	11	0.899999976	3	58	0	5	3000	ha non 
195	Herpes	HER	99.9899979	11	1	1	68	0	5	99	ha non 
200	MST	mst	0	0	0.100000001	1	68	0	0	3	Sans remarque
198	Echecs	HER	999	11	0.899999976	3	91	0	5	3000	ha non 
187	Polux PUTE	POL	99	12	0.5	3	82	0	2	1000	ha oui
188	Astral PUTE	AST	999	11	0.899999976	1	82	0	5	3000	ha non 
199	Go	NEC	999	4	0.200000003	3	91	0	3	2000	ha bof
183	Nouveau Depot	surnom inconnu	0	0	0.100000001	1	54	0	0	5	kkk
173	Herpes	HER	999	11	0.200000003	3	56	0	5	3000	ha non 
172	Furoncle	FUR	99	12	0.100000001	1	56	0	2	1000	ha oui
171	Rip me	RM	999	4	0.100000001	4	57	0	3	2000	ha bof
165	Batman	BAT	0	0	1	1	55	0	0	5	
189	Sans nom	Sans nom	0	0	5	1	82	0	0	22	Sans remarque
190	Sans nom	Sans nom	0	0	5	3	82	0	0	2	Sans remarque
192	0 007	bonde jeannonde	0	0	5	1	75	0	0	2	Sans remarque
197	Art	FUR	99	12	0.5	3	91	0	2	99	ha oui
185	O Superman	SUP	99.9899979	15	0.899999976	1	75	0	5	9	ha non 
184	A Asterix	AST	99	12	0.5	1	75	0	2	99	ha oui
186	Et Muscor	MUSC	99.9899979	4	0.200000003	3	75	0	3	99	ha bof
194	Furoncle	FUR	99	12	3	1	68	0	2	99	ha oui
193	Tintin	TT	5	1	1	2	75	0	1	4	Sans remarque
174	Nécrose	NEC	999	4	1	4	56	0	3	2000	ha bof
\.


--
-- TOC entry 2071 (class 0 OID 16456)
-- Dependencies: 172 2090
-- Data for Name: etatslieux_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY etatslieux_tb (dbid, etat) FROM stdin;
1	ouvert
2	fermé
3	en travaux
4	fermeture definitive
5	trop loin
6	inconnu
\.


--
-- TOC entry 2110 (class 0 OID 0)
-- Dependencies: 173
-- Name: etatslieux_tb_id_etatlieu_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('etatslieux_tb_id_etatlieu_seq', 4, true);


--
-- TOC entry 2074 (class 0 OID 16466)
-- Dependencies: 175 2090
-- Data for Name: genresclients_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY genresclients_tb (dbid, genre) FROM stdin;
1	théâtre                                           
2	troupe                                            
3	cinéma                                            
4	bar                                               
5	concert                                           
6	institution                                       
7	privé                                             
8	autre                                             
9	galerie                                           
\.


--
-- TOC entry 2075 (class 0 OID 16470)
-- Dependencies: 176 2090
-- Data for Name: genrescontrats_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY genrescontrats_tb (dbid, genre) FROM stdin;
1	contrat
2	devis
\.


--
-- TOC entry 2111 (class 0 OID 0)
-- Dependencies: 177
-- Name: genrescontrats_tb_dbid_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('genrescontrats_tb_dbid_seq', 2, true);


--
-- TOC entry 2077 (class 0 OID 16478)
-- Dependencies: 178 2090
-- Data for Name: genresdepots_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY genresdepots_tb (dbid, genre) FROM stdin;
1	Flyer
2	Dépliant
3	Brochure
4	Affiche
5	Autre
\.


--
-- TOC entry 2112 (class 0 OID 0)
-- Dependencies: 179
-- Name: genresdepots_tb_id_genre_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('genresdepots_tb_id_genre_seq', 5, true);


--
-- TOC entry 2079 (class 0 OID 16486)
-- Dependencies: 180 2090
-- Data for Name: genreslieux_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY genreslieux_tb (dbid, genre) FROM stdin;
1	Théâtre
2	Lieux culturel
3	Administration
5	Boutique
4	Mairie
6	Inconnu
\.


--
-- TOC entry 2113 (class 0 OID 0)
-- Dependencies: 181
-- Name: genreslieux_tb_id_genre_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('genreslieux_tb_id_genre_seq', 6, true);


--
-- TOC entry 2114 (class 0 OID 0)
-- Dependencies: 164
-- Name: id_client_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('id_client_seq', 28, true);


--
-- TOC entry 2115 (class 0 OID 0)
-- Dependencies: 166
-- Name: id_contrat_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('id_contrat_seq', 97, true);


--
-- TOC entry 2116 (class 0 OID 0)
-- Dependencies: 170
-- Name: id_depot_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('id_depot_seq', 200, true);


--
-- TOC entry 2117 (class 0 OID 0)
-- Dependencies: 174
-- Name: id_genre_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('id_genre_seq', 9, true);


--
-- TOC entry 2118 (class 0 OID 0)
-- Dependencies: 183
-- Name: id_lieu_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('id_lieu_seq', 932, true);


--
-- TOC entry 2081 (class 0 OID 16494)
-- Dependencies: 182 2090
-- Data for Name: lieux_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY lieux_tb (dbid, nom, dbid_genre, dbid_etat, pertinence, commentaire, saturation_max) FROM stdin;
563	Office du Tourisme de Paris	1	1	0	\N	\N
619	Centre d'Animation Solidarité	1	1	0	\N	\N
620	Centre d'Animation Places des Fêtes	1	1	0	\N	\N
621	Espace jeune Centre social	1	1	0	\N	\N
622	Centre d'animations Les Amandiers	1	1	0	\N	\N
623	Centre d'animations Louis Lumière	1	1	0	\N	\N
624	Centre d’animation Espace Saint Blaise	1	1	0	\N	\N
625	PIJ / Antenne Jeunes Pyhton	1	1	0	\N	\N
626	Centre d'animation Louis Lumière	1	1	0	\N	\N
627	Antenne Jeunes Davoult	1	1	0	\N	\N
628	Les Funambules	1	1	0	\N	\N
629	Marquise Café	1	1	0	\N	\N
603	esppp	1	1	0	\N	\N
633	Colette	1	1	0	\N	\N
634	Le Laboratoire	1	1	0	\N	\N
635	FORUM DES IMAGES	1	1	0	\N	\N
637	ARTS ET METIERS	1	1	0	\N	\N
638	Mariam Goodmann	1	1	0	\N	\N
575	Centre d'animations  Beaujon	1	1	0	\N	\N
666	Kamel Mennour	1	1	0	\N	\N
557	SACD librairie	1	1	0		\N
561	DDJS	1	1	0	bof	\N
668	Centre Calouste Gulbenkian	1	1	0	\N	\N
669	Reflet Médicis (Quartier Latin)	1	1	0	\N	\N
568	GRETA	1	1	0	\N	\N
559	ARCADI	1	1	0	\N	\N
640	POLKA GALERIE	1	1	0	\N	\N
650	Filles du Calvaire	1	1	0	\N	\N
641	GALERIE CHANTAL CROUSEL	1	1	0	\N	\N
567	IRMA	1	1	0	\N	\N
645	INSTITUT SUEDOIS	1	1	0	\N	\N
646	Galerie Almine Rech	1	1	0	\N	\N
569	AFDAS	1	1	0	\N	\N
639	Gaité Lyrique	1	1	0	\N	\N
572	Centre d'animations Censier	1	1	0	\N	\N
649	Galerie Thaddaeus Ropac	1	1	0	\N	\N
644	GALERIE PAUL FRECHES	1	1	0	\N	\N
630	Le Petit ney	1	1	0	\N	\N
653	GALERIE PARTICULIERE	1	1	0	\N	\N
654	PARISIENNE DE LA PHOTOGRAPHIE	1	1	0	\N	\N
655	Librairie OFR	1	1	0	\N	\N
656	Centre culturel Suisse	1	1	0	\N	\N
657	GALERIE DU JOUR AGNES B	1	1	0	\N	\N
658	Galerie Nathalie Obadia	1	1	0	\N	\N
659	MEP	1	1	0	\N	\N
661	ENSAD	1	1	0	\N	\N
662	THEATRE DE l' ODEON	1	1	0	\N	\N
663	Beaux Arts de Paris - ENSBA	1	1	0	\N	\N
664	Galerie Magnum	1	1	0	\N	\N
665	Galerie Loevenbruck	1	1	0	\N	\N
556	DRAC	1	1	0		\N
667	Centre Culturel Canadien	1	1	0	\N	\N
562	Centre national du Théâtre	1	1	0		\N
573	Centre d'animations Arras	1	1	0	\N	\N
647	Yvon Lambert librairie	1	1	0	\N	\N
651	Martine Aboucaya	1	1	0	\N	\N
652	Galerie Michel Rein	1	1	0	\N	\N
574	Centre d'animations St Michel	1	1	0	\N	\N
577	PIJ / Antenne Jeunes 9e	1	1	0	\N	\N
578	Centre d'animations Jean Verdier	1	1	0	\N	\N
579	Centre d'animations Château Landon	1	1	0	\N	\N
580	Centre d'animations La grange aux Belles	1	1	0	\N	\N
581	Centre Social Le Pari's des faubourgs	1	1	0	\N	\N
582	Centre d'animatrion Jemmapes	1	1	0	\N	\N
583	PIJ / MJC Mercoeur	1	1	0	\N	\N
584	PIJ / Antenne Jeune Orillon	1	1	0	\N	\N
586	centre d'animations villiot	1	1	0	\N	\N
587	PIJ / Antenne Jeune Claude Decean	1	1	0	\N	\N
588	Centre d'animations La Poterne des peupliers	1	1	0	\N	\N
589	Centre d'animation Charles Richet	1	1	0	\N	\N
591	Centre d'Animation Baudricourt	1	1	0	\N	\N
592	Centre d'animation Dunois	1	1	0	\N	\N
593	Antenne Jeunes  Fontaine à Mulard	1	1	0	\N	\N
594	Antenne jeunes Campo Formio	1	1	0	\N	\N
595	Antennes jeunes SUD	1	1	0	\N	\N
596	Maison des associations	1	1	0	\N	\N
597	centre d'animations Marc Sangnier	1	1	0	\N	\N
598	Point jeune	1	1	0	\N	\N
599	Centre d'animations Brancion	1	1	0	\N	\N
600	centre d'animations frère voisins	1	1	0	\N	\N
601	Centre d'animation Sohane	1	1	0	\N	\N
602	PIJ / antenne jeune information Didot	1	1	0	\N	\N
631	espace cévennes	1	1	0	\N	\N
604	Conservatoire Francis Poulenc	1	1	0	\N	\N
606	centre d'animations la jonquière	1	1	0	\N	\N
607	PIJ / Antenne Jeunes Louis Loucheur	1	1	0	\N	\N
608	Interclub 17	1	1	0	\N	\N
609	Antennes jeunes Haut de Malesherbes	1	1	0	\N	\N
610	Centre d'animations Hébert	1	1	0	\N	\N
611	Centre d'animations René Binet	1	1	0	\N	\N
612	PIJ / Antenne jeunes Henri Brisson	1	1	0	\N	\N
632	Centre Binet	1	1	0	\N	\N
614	Antenne jeunes Mont Cenis	1	1	0	\N	\N
615	Centre d'animations Clavel	1	1	0	\N	\N
616	Centre d'animations Curial	1	1	0	\N	\N
617	Centre d'animations Mathis	1	1	0	\N	\N
618	Centre d'animations Rébeval	1	1	0	\N	\N
636	Ministère de la culture Immeuble des bons enfants	1	1	0	\N	\N
648	Galerie Xippas (à l'étage)	1	1	0	\N	\N
642	SURFACE TO AIR	1	1	0	\N	\N
571	Maison des associations	1	1	0	\N	\N
700	FRAC Plateau	1	1	0	\N	\N
701	GALERIE SUZANNE TARASIEVE	1	1	0	\N	\N
703	Belleviloise 	1	1	0	\N	\N
704	Maronquinerie 	1	1	0	\N	\N
672	PINACOTHEQUE DE PARIS	1	1	0	\N	\N
590	Centre d'animation Daviel	1	1	0		\N
698	INSTITUT DE CULTURE DE L'ISLAM	1	1	0	\N	\N
699	Trabendo 	1	1	0	\N	\N
673	SCAM	1	1	0	\N	\N
674	Galerie Leica Paris	1	1	0	\N	\N
675	Musée de la Vie romantique\nHôtel Scheffer-Renan 	1	1	0	\N	\N
676	GALERIE VU	1	1	0	\N	\N
677	Galerie des galeries	1	1	0	\N	\N
678	ICCOM	1	1	0	\N	\N
705	Le laboratoire de la création	1	1	0	\N	\N
680	Bibliothèque Château d’Eau 	1	1	0	\N	\N
723	Librairie comme un roman	1	1	0	\N	\N
724	Librairie Marelle	1	1	0	\N	\N
736	IRCAM	1	1	0	\N	\N
684	MAISON DES MÉTALLOS	1	1	0	\N	\N
685	Maison Rouge	1	1	0	\N	\N
687	Bétonsalon	1	1	0	\N	\N
688	Cinéma L'entrepôt	1	1	0	\N	\N
689	Fondation Cartier	1	1	0	\N	\N
774	Ecole Charles Dullin	1	1	0	\N	\N
691	Musée d'art moderne de la ville de paris	1	1	0	\N	\N
709	Espace st roch	1	1	0	\N	\N
710	Mairie du 1e	1	1	0	\N	\N
682	Alimentation Générale	1	1	0	\N	\N
695	LE TRIANON 	1	1	0	\N	\N
696	HALLE SAINT-PIERRE	1	1	0	\N	\N
697	La Femis	1	1	0	\N	\N
737	Centre de doc° et de format° de la Ville	1	1	0	\N	\N
738	Biblio. Historique de la Ville de Paris	1	1	0	\N	\N
739	Librairie de la BHVP	1	1	0	\N	\N
740	Bibliothèque Forney	1	1	0	\N	\N
741	KIOSQUE JEUNES LE MARAIS	1	1	0	\N	\N
742	Micadanses	1	1	0	\N	\N
743	Mairie du 4e	1	1	0	\N	\N
744	Bibliothèque Baudoyer	1	1	0	\N	\N
745	La belle Lurette	1	1	0	\N	\N
746	Direction des Affaires Culturelles	1	1	0	\N	\N
747	CENTRE DE DANSE DU MARAIS	1	1	0	\N	\N
748	Maison des contes et des histoires	1	1	0	\N	\N
749	Pôle Simon Lefranc	1	1	0	\N	\N
750	Librairie Lire Elire	1	1	0	\N	\N
751	L'harmattan	1	1	0	\N	\N
752	Mairie du 5e	1	1	0	\N	\N
754	Librairie Compagnie	1	1	0	\N	\N
755	Mots et merveilles	1	1	0	\N	\N
756	Librairie La Boucherie	1	1	0	\N	\N
757	CROUS Paris	1	1	0	\N	\N
758	Maison des cultures du monde	1	1	0	\N	\N
759	Librairie l'Escalier	1	1	0	\N	\N
760	Librairie Tschann	1	1	0	\N	\N
761	Librairie La Hune	1	1	0	\N	\N
762	Librairie L'écume des pages	1	1	0	\N	\N
763	Librairie Le Coupe-Papier	1	1	0	\N	\N
764	Conservatoire JP Rameau	1	1	0	\N	\N
766	Librairie du Spectacle Garnier Arnoult	1	1	0	\N	\N
767	Sciences Po - Bureau des Arts	1	1	0	\N	\N
768	Conservatoire Sup National d'art dramatique	1	1	0	\N	\N
769	SACD	1	1	0	\N	\N
770	ONDA	1	1	0	\N	\N
771	Conservatoire Nadia et Lili Boulanger	1	1	0	\N	\N
772	Théâtre de l'Athénée	1	1	0	\N	\N
773	DRAC	1	1	0	\N	\N
690	Fondation Henri Cartier Bresson	1	1	0	\N	\N
692	Palais de tokyo	1	1	0	\N	\N
775	Ecole Jacques Lecoq	1	1	0	\N	\N
776	Conservatoire Hector Berlioz	1	1	0	\N	\N
777	mairie du 10e	1	1	0	\N	\N
778	Espace Kiron	1	1	0	\N	\N
779	Ménagerie de Verre	1	1	0	\N	\N
780	Cours Simon	1	1	0	\N	\N
781	Le local	1	1	0	\N	\N
782	BIBLIOTHEQUE ADULTE FAIDHERBE	1	1	0	\N	\N
783	BIBLIOTHEQUE ADULTE PARMENTIER	1	1	0	\N	\N
784	Librairie Quilombo	1	1	0	\N	\N
785	Librairie La Friche	1	1	0	\N	\N
679	Centre Commercial	1	1	0	\N	\N
681	Le Point Ephémère	1	1	0	\N	\N
706	Office du Tourisme de Paris	1	1	0	\N	\N
707	Les Déchargeurs	1	1	0	\N	\N
708	Librairies théâtrales	1	1	0	\N	\N
693	Le Divan du Monde 	1	1	0	\N	\N
694	Kadist Foundation	1	1	0	\N	\N
711	Maison du Geste et de l'Image	1	1	0	\N	\N
712	Centre Wallonie Bruxelles	1	1	0	\N	\N
713	Médiathèque musicale de Paris	1	1	0	\N	\N
714	Forum des Images	1	1	0	\N	\N
715	Conservatoire Mozart	1	1	0	\N	\N
716	Bibliothèque Charlotte Delbo	1	1	0	\N	\N
717	Ecole de l'Acteur Côté Cour	1	1	0	\N	\N
718	Mairie du 2e	1	1	0	\N	\N
719	Bibliothèque Marguerite Audoux	1	1	0	\N	\N
720	Mairie du 3e	1	1	0	\N	\N
722	Maison des associations	1	1	0	\N	\N
683	MAGDA DANYSZ	1	1	0	\N	\N
725	AGECIF	1	1	0	\N	\N
726	Musée d'art et d'hist. Du Judaïsme	1	1	0	\N	\N
727	Les Cahiers de Colette	1	1	0	\N	\N
728	CENTRE CULTUREL SUISSE et LIBRAIRIE CCS	1	1	0	\N	\N
729	AICOM PARIS 	1	1	0	\N	\N
730	Librairie L'arbres à lettres	1	1	0	\N	\N
731	Maison des initiatives étudiantes	1	1	0	\N	\N
732	Ministère de la Culture et de la Communication	1	1	0	\N	\N
733	Centre LGBT Paris-ÎdF	1	1	0	\N	\N
734	Centre Wallonie Bruxelles	1	1	0	\N	\N
735	Librairie Wallonie Bruxelles	1	1	0	\N	\N
830	THEATRE DE L'ATELIER	1	1	0	\N	\N
831	THEATRE DE L'ATELIER	1	1	0	\N	\N
832	THEATRE DE L'ATELIER	1	1	0	\N	\N
833	Lieu Inconnu	1	1	0	\N	\N
834	Nom inconnu	1	1	0	\N	\N
887	THEATRE DE L'ATELIER	6	6	\N		10
564	Actes-If Maison des réseaux artistiques et culturels	1	1	0	\N	\N
565	DAC / Rectorat de Paris	1	1	0	\N	\N
566	Rectorat de Paris	1	1	0	\N	\N
835	Nom inconnu	1	1	0	\N	\N
836	Nom inconnu	1	1	0	\N	\N
837	Nom inconnu	1	1	0	\N	\N
838	Nom inconnu	1	1	0	\N	\N
839	Nom inconnu	1	1	0	\N	\N
840	Nom inconnu	1	1	0	\N	\N
841	Nom inconnu	1	1	0	\N	\N
842	Nom inconnu	1	1	0	\N	\N
843	Nom inconnu	1	1	0	\N	\N
844	Nom inconnu	1	1	0	\N	\N
845	Nom inconnu	1	1	0	\N	\N
846	Pute	1	1	0	\N	\N
847	super nom inconnu	1	1	0	\N	\N
848	super nom inconnu	1	1	0	\N	\N
849	super nom inconnu	1	1	0	\N	\N
850	super nom inconnu	1	1	0	\N	\N
851	super nom inconnu	1	1	0	\N	\N
852	super nom inconnu	1	1	0	\N	\N
882	Colette	1	1	0		\N
880	super nom inconnu	1	1	0		\N
886	Mariam Goodmann	1	1	0		\N
702	LE CENTQUATRE le merle moqueur - librairie 	1	1	0	\N	\N
570	Ass forum, animation, loisirs	1	1	0	\N	\N
883	Le Laboratoire	1	1	0		\N
585	centre d'animations maurice ravel	1	1	0	\N	\N
815	Librairie Anima	1	1	0	\N	\N
816	Librairie L'Humeur Vagabonde	1	1	0	\N	\N
817	LIBRAIRIE VENDREDI 	1	1	0	\N	\N
818	Ecole Nat Sup d'Architecture de Paris 	1	1	0	\N	\N
819	Boutique livres et DVD Mk2 Quai de Loire  	1	1	0	\N	\N
820	Librairie du 104 et Accueil du 104	1	1	0	\N	\N
821	La Maroquinerie  (salle de concert/ restau)	1	1	0	\N	\N
823	librairie Le Comptoir des mots	1	1	0	\N	\N
824	Librairie Le Genre Urbain	1	1	0	\N	\N
825	Librairie L'équipage	1	1	0	\N	\N
826	Librairie Gâtines	1	1	0	\N	\N
827	Théâtre de l'Echangeur 	1	1	0	\N	\N
828	 Mains D'oeuvres (salle de concerts, événements)	1	1	0	\N	\N
829	Anis Gras  (lieu de création)	1	1	0	\N	\N
643	GALERIE FLORENCE LOEWY	1	1	0	\N	\N
670	Jeu de Paume	1	1	0	\N	\N
753	Ecole Normale Supérieure - Bureau des Arts	1	1	0	\N	\N
765	Maison des pratiques artistiques amateurs - Auditorium saint germain	1	1	0	\N	\N
786	Artistic Athévain	1	1	0	\N	\N
787	Café de la Danse	1	1	0	\N	\N
788	Pôle Emploi Spectacle	1	1	0	\N	\N
789	Librairie la Manœuvre	1	1	0	\N	\N
790	Théâtre de la Bastille 	1	1	0	\N	\N
791	Librairie L'Arbre à lettres	1	1	0	\N	\N
560	Hors les murs	1	1	100	geniale	\N
792	Conservatoire Charles Münch	1	1	0	\N	\N
793	Maison des métallos	1	1	0	\N	\N
795	La cartoucherie Théatre de la Tempète	1	1	0	\N	\N
797	Conservatoire Darius Milhaud	1	1	0	\N	\N
798	ANRAT	1	1	0	\N	\N
605	Centre d'animations Point du jour	1	1	0	\N	\N
721	Association culturelle CNAM (pas facile à trouver !)	1	1	0	\N	\N
801	Conservatoire Claude Debussy	1	1	0	\N	\N
802	Cons. municipal du 18 eme	1	1	0	\N	\N
803	LE VENT SE LEVE	1	1	0	\N	\N
804	Cours Florent	1	1	0	\N	\N
805	Cours Florent	1	1	0	\N	\N
806	L’ATELIER DU PLATEAU	1	1	0	\N	\N
807	Le Rosa Bonheur  	1	1	0	\N	\N
808	Acting International 	1	1	0	\N	\N
809	Conservatoire Jacques Ibert	1	1	0	\N	\N
810	Confluences	1	1	0	\N	\N
811	Au QG formation	1	1	0	\N	\N
812	Théâtre de la Colline  	1	1	0	\N	\N
813	Librairie Le Merle moqueur	1	1	0	\N	\N
814	Conservatoire Georges Bizet	1	1	0	\N	\N
671	Fondation Ricard	1	1	0	\N	\N
686	Cinémathèque française	1	1	0	\N	\N
888	Mairie du 18e	6	6	\N		10
889	Kiosque jeunes - Centre Musical Fleury Goutte d’Or-Barbara	6	6	\N		10
890	Universite Paris Iv - Service culturel	6	6	\N		10
891	Théâtre de Chaillot – Espace librairie	6	6	\N		10
892	Kiosque Jeunes - Cidj	6	6	\N		10
893	Université Paris 4 - Centre Malesherbes	6	6	\N		10
894	LIBRAIRIE IMAGIGRAPHE	6	6	\N		10
895	SOUFFLE CONTINU	6	6	\N		10
896	AU CLAIR DE LUNE	6	6	\N		10
897	CNSMP	6	6	\N		10
898	LE VENT SE LEVE	6	6	\N		10
899	BIBLIOTHEQUE ADULTE 	6	6	\N		10
900	ANTENNES JEUNES 	6	6	\N		10
901	VINGTIEME THEATRE 	6	6	\N		10
902	ANTENNES JEUNES 	6	6	\N		10
903	ANTENNES JEUNES 	6	6	\N		10
904	BIBLIOTHEQUE ADULTE 	6	6	\N		10
905	ECOLE DE MUSIQUE	6	6	\N		10
906	THEATRE DE LA GIRANDOLE	6	6	\N		10
907	LIBRAIRIE FOLIES D'ENCRE 	6	6	\N		10
908	LA PAROLE ERRANTE	6	6	\N		10
909	CDN MONTREUIL  	6	6	\N		10
910	LA MAISON POPULAIRE	6	6	\N		10
911	LES INSTANTS CHAVIRES	6	6	\N		10
912	THEATRE DES BERGERIES	6	6	\N		10
913	THEATRE GERARD PHILIPPE	6	6	\N		10
914	LE TRITON	6	6	\N		10
915	BIBLIOTHEQUE ANDRE MALRAUX	6	6	\N		10
916	CENTRE CULTUREL JEAN COCTEAU	6	6	\N		10
917	LILAS EN SCENE	6	6	\N		10
918	THEATRE DE LA COMMUNE	6	6	\N		10
919	CNR D'AUBERVILLIERS ( locaux d'Aubervilliers )	6	6	\N		10
920	LIBRAIRIE FOLIES D’ENCRE 	6	6	\N		10
921	LA DYNAMO	6	6	\N		10
922	JTN 	6	6	\N		10
923	PARIS III CENTRE CENSIER (Kiosque Billetterie)	6	6	\N		10
924	COURS  RENE SIMON	6	6	\N		10
925	LA MAISON ROUGE Fondation Antoine de Galbert	6	6	\N		10
926	SUDDEN THEATRE	6	6	\N		10
927	THEATRE PARIS VILETTE	6	6	\N		10
928	BIBLIOTHEQUE ADULTE	6	6	\N		10
929	LE TARMAC	6	6	\N		10
930	CINE 104	6	6	\N		10
931	THEATRE ECOLE	6	6	\N		10
932	BIBLIOTHÈQUE GOUTTE D'OR	6	6	\N		10
613	Centre Binet	1	1	0	\N	\N
796	Théatre de L'aquirium 	1	1	0		\N
794	La cartoucherie Théâtre du Soleil	1	1	0	wdcdwcdc	\N
576	Centre d'animations  Valeyre	1	1	0		\N
853	super nom inconnu	1	1	0	\N	\N
854	super nom inconnu	1	1	0	\N	\N
855	super nom inconnu	1	1	0	\N	\N
856	super nom inconnu	1	1	0	\N	\N
857	super nom inconnu	1	1	0	\N	\N
858	super nom inconnu	1	1	0	\N	\N
859	ex chez moi	1	1	0	\N	\N
860	exxx chez moi	1	1	0	\N	\N
861	exx cm	1	1	0	\N	\N
863	popopo	1	1	0	\N	\N
864	toto	1	1	0	\N	\N
871	testtesttest	1	1	0	\N	\N
872	testtesttest	1	1	0	\N	\N
873	axou et tanyou	1	1	0	\N	\N
862	Tour effeil	1	1	0	\N	\N
875	FNAC montparnasse	1	1	0	\N	\N
822	La Bellevilloise   (café, concerts, événements) 	1	1	0	\N	\N
558	SACD acceuil	1	1	0	sacd c est bien	\N
660	Institut du Monde Arabe	1	1	0	\N	\N
799	Théâtre de la Cité internationale 	1	1	0	\N	\N
800	Conservatoire Frédéric Chopin	1	1	0	\N	\N
878	bidule	1	1	0		\N
876	ZZZ	1	1	10	vdvvdvf	\N
879	super nom inconnu	1	1	0		\N
874	axel hoffmann	1	1	0		\N
881	ededed	1	1	0		\N
884	FORUM DES IMAGES	1	1	0		\N
877	merde	1	1	0		\N
885	MINISTERE DE LA CULTURE // POINT CULTURE/ DIC 	1	1	0		\N
\.


--
-- TOC entry 2119 (class 0 OID 0)
-- Dependencies: 184
-- Name: localites_tb_id_localite_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('localites_tb_id_localite_seq', 38966, true);


--
-- TOC entry 2087 (class 0 OID 16677)
-- Dependencies: 188 2090
-- Data for Name: parcours_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY parcours_tb (dbid, dbid_tournee, dbid_pedaleur, list_dbid_lieu, polygon, line) FROM stdin;
29	7	3	{725,719,720,788,560,777,730,559,774,775,776,768,571,578,581,580,582}	((2.357765253025081,48.8776942149217177),(2.34430047183534107,48.8722178047084768),(2.3466810952848931,48.8717503298246712),(2.35762973827108313,48.8714780128425019),(2.35920258954658513,48.8692424652109878),(2.35901964668218822,48.8637798339724725),(2.36504357668200882,48.862411382006762),(2.37357529519531996,48.8654115262817612),(2.369625958592112,48.8775089788964365),(2.357765253025081,48.8776942149217177))	{768,559,775,777,776,578,719,720,571,725,730,788,560,580,774,582,581}
15	7	2	{787,810,812,789,825,569,791,778,779,786,780,813,823,782,567,811,790,814,783,784,826,792,827,586,583,585,568,587}	((2.36895956081179015,48.8429423129310081),(2.39469898072526011,48.8343335295841996),(2.4247626603823198,48.8435327512926989),(2.42624027814597021,48.8689649764500871),(2.38610320409068022,48.8698876454497011),(2.37535193190274985,48.8654632042998003),(2.36902642223292981,48.8541214496973097),(2.36895956081179015,48.8429423129310081))	{586,587,585,811,784,782,791,791,791,787,789,790,786,583,778,780,783,779,792,814,567,826,812,823,569,568,825,813,810}
2	4	2	{607}	((0,1),(1,0),(1,1),(0,1))	{}
1	3	3	{611,557,607,608,612,558,614,562,606,563,630,632,816,802,801,828,697,769,817,770,815}	((2.35179308416062005,48.8902168077090025),(2.34514112362957983,48.9099782324226027),(2.32034513578719981,48.9013358753052074),(2.29998509900216019,48.8787182907366926),(2.33694637052527998,48.878017000503803),(2.34908292960682008,48.8834470651687027),(2.35179308416062005,48.8902168077090025))	{801,608,606,607,612,630,611,632,828,614,802,697,815,563,817,770,557,769}
3	3	3	{723,822,755,803,785,795,821,744,766,756}	((0.146203445840251994,0.0981973583927815002),(-0.0641874781168306069,0.00593085180615419982),(0.0649615773673307001,-0.126087943110265999),(0.146203445840251994,0.0981973583927815002))	{723}
14	7	3	{829,752,663,765,757,798,753,797,760,750,759,758,754,751,799,764,761,762,763,767,800,592,588,593,591,595,596,605,572,631,594,599,574,598,597,590,573,602,601,589,604,600}	((2.32321236005848997,48.807029040456797),(2.39595681334097987,48.8142694479518866),(2.36968243892567987,48.8404357581203072),(2.3457514138409401,48.8563280446209021),(2.33181692562595,48.8584863279387918),(2.29510000000000014,48.8596000000000075),(2.27739827390873995,48.8626012333456003),(2.25006290650736007,48.8305843491461999),(2.32321236005848997,48.807029040456797))	{631,605,604,600,599,597,598,800,601,602,797,829,799,588,593,596,591,595,590,589,592,594,572,750,753,757,798,760,758,767,762,663,761,764,765,763,759,574,754,752,751,573}
4	3	2	{572,573,588,599,591,590,592,601,594,593,589,561,574,602,597,598,596,631,798,752,751,753,764,762,750,758,759,799,760,767,763,800,761,663,765,757,754,797}	((2.38923357769572986,48.8280479518481982),(2.35737364890123002,48.8506906168420088),(2.32459854539031019,48.8626498748276035),(2.29678534455304018,48.8618345007345027),(2.26915135863259998,48.839259266536601),(2.28818587022523001,48.8287282498908013),(2.34554014493357998,48.8169738943515128),(2.37790831276248982,48.8218704060874984),(2.38923357769572986,48.8280479518481982))	{631,800,601,598,602,797,599,597,799,588,593,590,596,591,561,589,592,594,572,750,753,798,757,760,758,767,762,761,764,765,763,759,754,752,751,573,574,663}
5	3	4	{583,623,578,584,625,570,564,610,585,622,582,587,567,627,565,619,586,620,579,569,559,621,618,571,617,626,616,560,624,568,580,628,615,566,581,629,791,787,796,776,734,740,681,749,786,747,827,779,804,808,712,735,728,748,729,819,782,792,774,783,731,825,820,823,781,709,806,794,733,710,707,743,805,636,826,784,812,732,705,715,814,725,706,811,746,793,737,718,711,778,736,777,810,788,789,741,714,813,742,727,780,818,639,717,739,824,730,745,719,721,720,809,775,790,716}	((2.36891869111093012,48.8418710680888992),(2.40356283523309999,48.8327134347440932),(2.45998961201829003,48.833419433815898),(2.42998016189890986,48.8727182643709099),(2.39531573134170994,48.8935444016205878),(2.36144432162040019,48.9017509705522997),(2.35941056330897991,48.8853156342655026),(2.35182424893862008,48.8779362333968876),(2.35126633719848988,48.8707990317389971),(2.34308083455169003,48.8699846638360924),(2.33043724766567006,48.8688334870956993),(2.33074278385787981,48.8632384225228122),(2.33998577863266011,48.8586806149330002),(2.35858048711906987,48.8512621340989028),(2.36891869111093012,48.8418710680888992))	{709}
30	7	5	{781,793,806,809,808,818,804,681,724,819,824,618,579,584,615}	((2.37333736013866314,48.8708414942124278),(2.37647757592032782,48.8664349169804595),(2.386527660843623,48.8714720120438386),(2.39422814355752189,48.8828085160308632),(2.37726689158303905,48.8864954187346967),(2.35343587935083987,48.8871020830853311),(2.35580666098117186,48.8827136841400005),(2.37072957290370878,48.8785313473554481),(2.37333736013866314,48.8708414942124278))	{579,681,818,618,824,584,781,793,615,806,808}
27	7	2	{769,802,816,801,770,771,805,772,773,630,820,815,697,817,562,617,607,575,632,608,606,609,611,576,577,610,612,614,616}	((2.30330621949176306,48.899301841215788),(2.29595252151177309,48.8933991638653822),(2.30234059571488503,48.8729926111805995),(2.33171794750019412,48.8701175604426865),(2.3557473808654561,48.8802601419973826),(2.35213937952959906,48.8882654742424734),(2.37812673198228008,48.8878461721846591),(2.38913577544213318,48.898569489453422),(2.33299551628073987,48.9019685211037469),(2.30330621949176306,48.899301841215788))	{575,801,608,609,606,562,607,612,630,611,632,816,614,802,697,815,769,770,817,772,773,577,771,576,610,616,617,805,820}
28	7	2	{714,742,743,639,717,718,745,732,734,749,708,727,731,636,746,721,712,729,570,709,710,740,733,705,737,715,735,716,706,747,748,736,739,728,741,711,707}	((2.33035042457265584,48.8685721395526471),(2.33119626347445497,48.8600500588754514),(2.34964556471654484,48.8575973439390481),(2.35659658532005212,48.8523864490859268),(2.36751114249005301,48.8521428201617027),(2.36992468733883088,48.8584532753079799),(2.35829666821859085,48.8632738459677682),(2.35720666319928718,48.8711601542641105),(2.33790962777582489,48.8717254119196198),(2.33035042457265584,48.8685721395526471))	{708,709,706,718,716,636,705,710,707,714,570,715,711,735,734,736,737,743,741,742,740,745,731,739,746,728,748,747,749,727,733,732,721,639,729,717}
10	6	2	{816,630,817,801,562,828,769,770,819,697,809,804,681,805,820,724,815,802,609,608,558,612,610,617,614,616,557,563,607,575,579,606,611,632}	((2.30476581447306206,48.8737561859909491),(2.31621049794280109,48.8809357311466073),(2.3365168448461171,48.8775867690618995),(2.35340456325868086,48.8825551100596911),(2.36765395086393893,48.8797775674554629),(2.38023008933754721,48.8834547758600593),(2.36954777774647507,48.8872286845993784),(2.39114836663793184,48.9000984001905294),(2.34672807438018705,48.9136355733326909),(2.29195184356318915,48.895671174593538),(2.30476581447306206,48.8737561859909491))	{}
11	6	5	{782,721,783,740,793,823,709,768,788,710,733,743,794,720,826,813,774,715,784,735,706,812,560,771,746,727,737,777,739,569,791,567,775,736,708,741,787,714,747,827,811,742,711,780,716,639,772,818,717,810,730,636,745,792,719,712,734,825,781,806,776,773,748,790,707,749,786,808,778,789,732,559,814,779,824,796,725,731,729,728,705,570,718,586,618,578,576,626,627,587,583,625,585,619,566,581,628,615,556,571,621,584,568,564,622,624,580,577,582,623,620,565,629}	((2.38534885567300581,48.8806892254717127),(2.36835347097009885,48.8789500684121876),(2.34897717507153381,48.8803741158486389),(2.32427823890465302,48.8731910941486234),(2.33525732543309106,48.8607497019606001),(2.3559227685017099,48.8527080706902126),(2.36948478655097494,48.8402323091726132),(2.39129530032211202,48.8369044679223734),(2.43965215078990205,48.8309679843094173),(2.47040150429418581,48.8360985711482769),(2.43318733400823817,48.8604915359460605),(2.39494987114169788,48.8918148030834132),(2.38534885567300581,48.8806892254717127))	{}
12	6	3	{761,800,759,760,798,751,762,763,767,797,765,663,754,753,757,758,752,764,601,574,605,602,597,598,573,599,604,631}	((2.32141804867129808,48.8106843670067576),(2.35664831588544299,48.8484661378463798),(2.33600085909247301,48.8587601817267085),(2.27442278278551013,48.8573446589365403),(2.25596843521354717,48.8358511484810691),(2.32141804867129808,48.8106843670067576))	{}
13	6	4	{750,829,799,592,594,589,590,593,572,596,588,591}	((2.32513993700229005,48.8086558112836428),(2.32902388493639911,48.8052424307782715),(2.38329883585688407,48.8293978772127488),(2.35338393879184604,48.8441807885697372),(2.32513993700229005,48.8086558112836428))	{}
\.


--
-- TOC entry 2120 (class 0 OID 0)
-- Dependencies: 187
-- Name: parcours_tb_dbid_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('parcours_tb_dbid_seq', 30, true);


--
-- TOC entry 2089 (class 0 OID 16731)
-- Dependencies: 190 2090
-- Data for Name: pedaleurs_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY pedaleurs_tb (dbid, nom, prenom, surnom, dbid_lieu, couleur) FROM stdin;
2	Duvivier	Jonas	Jojo	\N	#00ff00
5	Hoffmann	Axel	Axou	\N	#ffff00
4	Banlieue	Arthur	Artho	\N	#ffc0cb
6	J	Frank	JF	\N	#ff0000
3	Reux	Matthias	Matt	\N	#ffd700
\.


--
-- TOC entry 2121 (class 0 OID 0)
-- Dependencies: 189
-- Name: pedaleurs_tb_dbid_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('pedaleurs_tb_dbid_seq', 6, true);


--
-- TOC entry 2084 (class 0 OID 16504)
-- Dependencies: 185 2090
-- Data for Name: tournees_tb; Type: TABLE DATA; Schema: public; Owner: axou
--

COPY tournees_tb (dbid, date_ouverture, date_cloture) FROM stdin;
3	2014-02-12	\N
4	2011-03-02	\N
5	1555-01-18	\N
6	\N	\N
7	\N	\N
8	\N	\N
\.


--
-- TOC entry 2122 (class 0 OID 0)
-- Dependencies: 186
-- Name: tournees_tb_dbid_seq; Type: SEQUENCE SET; Schema: public; Owner: axou
--

SELECT pg_catalog.setval('tournees_tb_dbid_seq', 8, true);


--
-- TOC entry 1942 (class 2606 OID 16518)
-- Dependencies: 185 185 2091
-- Name: cle_p; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY tournees_tb
    ADD CONSTRAINT cle_p PRIMARY KEY (dbid);


--
-- TOC entry 1934 (class 2606 OID 16520)
-- Dependencies: 176 176 2091
-- Name: cle_pri; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY genrescontrats_tb
    ADD CONSTRAINT cle_pri PRIMARY KEY (dbid);


--
-- TOC entry 1946 (class 2606 OID 16739)
-- Dependencies: 190 190 2091
-- Name: clef_p_dbid_pedaleurs_tb; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY pedaleurs_tb
    ADD CONSTRAINT clef_p_dbid_pedaleurs_tb PRIMARY KEY (dbid);


--
-- TOC entry 1944 (class 2606 OID 16682)
-- Dependencies: 188 188 2091
-- Name: clef_p_parcours_tb; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY parcours_tb
    ADD CONSTRAINT clef_p_parcours_tb PRIMARY KEY (dbid);


--
-- TOC entry 1919 (class 2606 OID 16522)
-- Dependencies: 165 165 2091
-- Name: id_client_cons; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY clients_tb
    ADD CONSTRAINT id_client_cons PRIMARY KEY (dbid);


--
-- TOC entry 1932 (class 2606 OID 16524)
-- Dependencies: 175 175 2091
-- Name: id_genre_cons; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY genresclients_tb
    ADD CONSTRAINT id_genre_cons PRIMARY KEY (dbid);


--
-- TOC entry 1926 (class 2606 OID 16526)
-- Dependencies: 169 169 169 2091
-- Name: p_depot_lieu; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY depots_lieux_tb
    ADD CONSTRAINT p_depot_lieu PRIMARY KEY (dbid_depot, dbid_lieu);


--
-- TOC entry 1917 (class 2606 OID 16528)
-- Dependencies: 162 162 2091
-- Name: p_id_adresse; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY adresses_tb
    ADD CONSTRAINT p_id_adresse PRIMARY KEY (dbid);


--
-- TOC entry 1922 (class 2606 OID 16530)
-- Dependencies: 167 167 2091
-- Name: p_id_contrat; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY contrats_tb
    ADD CONSTRAINT p_id_contrat PRIMARY KEY (dbid);


--
-- TOC entry 1928 (class 2606 OID 16532)
-- Dependencies: 171 171 2091
-- Name: p_id_depot; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY depots_tb
    ADD CONSTRAINT p_id_depot PRIMARY KEY (dbid);


--
-- TOC entry 1930 (class 2606 OID 16534)
-- Dependencies: 172 172 2091
-- Name: p_id_etatlieu; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY etatslieux_tb
    ADD CONSTRAINT p_id_etatlieu PRIMARY KEY (dbid);


--
-- TOC entry 1938 (class 2606 OID 16536)
-- Dependencies: 180 180 2091
-- Name: p_id_genre; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY genreslieux_tb
    ADD CONSTRAINT p_id_genre PRIMARY KEY (dbid);


--
-- TOC entry 1936 (class 2606 OID 16538)
-- Dependencies: 178 178 2091
-- Name: p_id_genresdepots; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY genresdepots_tb
    ADD CONSTRAINT p_id_genresdepots PRIMARY KEY (dbid);


--
-- TOC entry 1940 (class 2606 OID 16540)
-- Dependencies: 182 182 2091
-- Name: p_id_lieu; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY lieux_tb
    ADD CONSTRAINT p_id_lieu PRIMARY KEY (dbid);


--
-- TOC entry 1924 (class 2606 OID 16542)
-- Dependencies: 168 168 2091
-- Name: p_id_localite; Type: CONSTRAINT; Schema: public; Owner: axou; Tablespace: 
--

ALTER TABLE ONLY cp_villes_tb
    ADD CONSTRAINT p_id_localite PRIMARY KEY (dbid);


--
-- TOC entry 1920 (class 1259 OID 16543)
-- Dependencies: 167 2091
-- Name: fki_cle_e_contrats_genrescontrats; Type: INDEX; Schema: public; Owner: axou; Tablespace: 
--

CREATE INDEX fki_cle_e_contrats_genrescontrats ON contrats_tb USING btree (dbid_genre);


--
-- TOC entry 1950 (class 2606 OID 16544)
-- Dependencies: 1933 167 176 2091
-- Name: cle_e_contrats_genrescontrats; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY contrats_tb
    ADD CONSTRAINT cle_e_contrats_genrescontrats FOREIGN KEY (dbid_genre) REFERENCES genrescontrats_tb(dbid);


--
-- TOC entry 1959 (class 2606 OID 16740)
-- Dependencies: 1939 190 182 2091
-- Name: cle_e_dbid_lieu_pedaleurs_tb_lieux_tb; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY pedaleurs_tb
    ADD CONSTRAINT cle_e_dbid_lieu_pedaleurs_tb_lieux_tb FOREIGN KEY (dbid_lieu) REFERENCES lieux_tb(dbid);


--
-- TOC entry 1958 (class 2606 OID 16683)
-- Dependencies: 188 1941 185 2091
-- Name: clef_e_dbid_tournee_parcours_tb; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY parcours_tb
    ADD CONSTRAINT clef_e_dbid_tournee_parcours_tb FOREIGN KEY (dbid_tournee) REFERENCES tournees_tb(dbid);


--
-- TOC entry 1954 (class 2606 OID 16549)
-- Dependencies: 171 178 1935 2091
-- Name: e-depots_tb_genre; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY depots_tb
    ADD CONSTRAINT "e-depots_tb_genre" FOREIGN KEY (dbid_genre) REFERENCES genresdepots_tb(dbid);


--
-- TOC entry 1947 (class 2606 OID 16554)
-- Dependencies: 182 1939 162 2091
-- Name: e_adresses_tb_lieu; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY adresses_tb
    ADD CONSTRAINT e_adresses_tb_lieu FOREIGN KEY (dbid_lieu) REFERENCES lieux_tb(dbid);


--
-- TOC entry 1948 (class 2606 OID 16559)
-- Dependencies: 162 1923 168 2091
-- Name: e_adresses_tb_localite; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY adresses_tb
    ADD CONSTRAINT e_adresses_tb_localite FOREIGN KEY (dbid_cp_ville) REFERENCES cp_villes_tb(dbid);


--
-- TOC entry 1949 (class 2606 OID 16564)
-- Dependencies: 165 1931 175 2091
-- Name: e_clients_tb_genre; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY clients_tb
    ADD CONSTRAINT e_clients_tb_genre FOREIGN KEY (dbid_genre) REFERENCES genresclients_tb(dbid);


--
-- TOC entry 1951 (class 2606 OID 16569)
-- Dependencies: 167 1918 165 2091
-- Name: e_contrats_tb_client; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY contrats_tb
    ADD CONSTRAINT e_contrats_tb_client FOREIGN KEY (dbid_client) REFERENCES clients_tb(dbid);


--
-- TOC entry 1952 (class 2606 OID 16574)
-- Dependencies: 169 1927 171 2091
-- Name: e_depots_lieux_tb_depot; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY depots_lieux_tb
    ADD CONSTRAINT e_depots_lieux_tb_depot FOREIGN KEY (dbid_depot) REFERENCES depots_tb(dbid);


--
-- TOC entry 1955 (class 2606 OID 16579)
-- Dependencies: 171 1921 167 2091
-- Name: e_depots_tb_contrat; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY depots_tb
    ADD CONSTRAINT e_depots_tb_contrat FOREIGN KEY (dbid_contrat) REFERENCES contrats_tb(dbid);


--
-- TOC entry 1956 (class 2606 OID 16584)
-- Dependencies: 1929 172 182 2091
-- Name: e_lieux_tb_etat; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY lieux_tb
    ADD CONSTRAINT e_lieux_tb_etat FOREIGN KEY (dbid_etat) REFERENCES etatslieux_tb(dbid);


--
-- TOC entry 1957 (class 2606 OID 16589)
-- Dependencies: 1937 182 180 2091
-- Name: e_lieux_tb_genre; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY lieux_tb
    ADD CONSTRAINT e_lieux_tb_genre FOREIGN KEY (dbid_genre) REFERENCES genreslieux_tb(dbid);


--
-- TOC entry 1953 (class 2606 OID 16594)
-- Dependencies: 1939 169 182 2091
-- Name: p_depots_lieux_tb_lieu; Type: FK CONSTRAINT; Schema: public; Owner: axou
--

ALTER TABLE ONLY depots_lieux_tb
    ADD CONSTRAINT p_depots_lieux_tb_lieu FOREIGN KEY (dbid_lieu) REFERENCES lieux_tb(dbid);


--
-- TOC entry 2096 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-03-02 01:50:45 CET

--
-- PostgreSQL database dump complete
--

