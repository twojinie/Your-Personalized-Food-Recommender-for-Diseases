import psycopg2

IP_ADDRESS = ""
PORT = ""
DB_NAME = ""
ID = ""
PASSWD = ""

def createTable():
    try:
        connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                      host=IP_ADDRESS, port=PORT)
        cursor = connection.cursor()
        sql = """
        CREATE TABLE gene(
            tax_id INTEGER NOT NULL DEFAULT 0,
            gene_id INTEGER NOT NULL DEFAULT 0,
            symbol VARCHAR(30) NOT NULL,
            chro_num VARCHAR(20),
            map_location VARCHAR(50),
            description VARCHAR(200),
            type_of_gene VARCHAR(30),
            modified_date DATE,
            PRIMARY KEY(gene_id)
        );
        CREATE TABLE gene_synonyms(
            synonyms VARCHAR(50) NOT NULL,
            gene_id INTEGER,
            PRIMARY KEY(synonyms, gene_id),
            FOREIGN KEY(gene_id) REFERENCES gene(gene_id) ON DELETE CASCADE
        );
        CREATE TABLE disease(
            OMIM_id INTEGER NOT NULL DEFAULT 0,
            disease_name VARCHAR(150),
            PRIMARY KEY(OMIM_id)
        );
        CREATE TABLE gene_disease(
            OMIM_id INTEGER NOT NULL DEFAULT 0,
            gene_symbol VARCHAR(30) NOT NULL,
            PRIMARY KEY (OMIM_id, gene_symbol)
        );
        CREATE TABLE gene_pathway(
            smpdb_id VARCHAR(10) NOT NULL,
            gene_symbol VARCHAR(10) NOT NULL,
            pathway_name VARCHAR(100),
            pathway_subject VARCHAR(20),
            uniprot_id VARCHAR(20),
            locus VARCHAR(30),
            PRIMARY KEY (smpdb_id, gene_symbol, uniprot_id)
        );
        CREATE TABLE pathway(
            pathway_id INTEGER NOT NULL,
            smpdb_id VARCHAR(10) NOT NULL,
            PRIMARY KEY (pathway_id)
        );
        CREATE TABLE compound(
            compound_id INTEGER NOT NULL,
            name VARCHAR(300),
            annotation VARCHAR(15000),
            PRIMARY KEY (compound_id)
        );
        CREATE TABLE compound_pathway(
            cp_id INTEGER NOT NULL, 
            compound_id INTEGER NOT NULL,
            pathway_id INTEGER NOT NULL,
            PRIMARY KEY (cp_id)
        );
        CREATE TABLE food(
            food_id INTEGER NOT NULL,
            food_name VARCHAR(60),
            food_group VARCHAR(30),
            PRIMARY KEY(food_id)
        );
        CREATE TABLE compound_food(
            cpf_id INTEGER NOT NULL,
            compound_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            amount NUMERIC(8,2) NOT NULL DEFAULT 0,
            PRIMARY KEY(cpf_id)
        );
        CREATE TABLE health(
            health_effect_id INTEGER NOT NULL,
            name VARCHAR(70),
            description VARCHAR(700),
            PRIMARY KEY(health_effect_id)
        );
        CREATE TABLE compound_health(
            compound_id INTEGER NOT NULL,
            health_effect_id INTEGER NOT NULL,
            PRIMARY KEY(compound_id, health_effect_id)
        );
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)

def createIndex():
    try:
        connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                      host=IP_ADDRESS, port=PORT)
        cursor = connection.cursor()
        sql = """
        CREATE INDEX ix_gene_id ON gene_synonyms(gene_id);
        CREATE INDEX ix_disease_name ON disease(disease_name);
        CREATE INDEX ix_smpdb_id ON pathway(smpdb_id);
        CREATE INDEX ix_compound_id ON compound_food(compound_id);
        CREATE INDEX ix_food_id ON compound_food(food_id);
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
