import psycopg2, csv

IP_ADDRESS = ""
PORT = ""
DB_NAME = ""
ID = ""
PASSWD = ""
dir_path = "./data/"

def insertDisease():
  filename = dir_path + "disease_OMIM.txt"
  with open(filename) as file:
    # disease_OMIM_ID disease_name
    header = file.readline()
    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for line in file:
        values = line.strip().split('\t')
        sql = f"INSERT INTO disease (OMIM_id, disease_name) values ({int(values[0])}, \'{values[1].replace('$','').replace('[','').replace(']','')}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertGene():
  filename = dir_path + "Homo_sapiens_gene_info.txt"
  with open(filename) as file:
    #tax_id GeneID  Symbol  Synonyms        chromosome      map_location    description     type_of_gene    Modification_date
    #0        1       2      3                   4              5              6                7                8
    header = file.readline()
    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for line in file:
        values = line.strip().split('\t')
        sql = f"INSERT INTO gene (tax_id, gene_id, symbol, chro_num, map_location, description, type_of_gene, modified_date) \
                Values ({int(values[0])}, {int(values[1])}, \'{values[2]}\', \'{values[4]}\', \'{values[5]}\', \'{values[6].replace('$','')}\', \'{values[7]}\', \'{values[8][:4]+'-'+values[8][4:6]+'-'+values[8][6:]}\');"
        cursor.execute(sql)
        if values[3] != '-':
          for synonym in values[3].split('|'):
            sql = f"INSERT INTO gene_synonyms (synonyms, gene_id) VALUES (\'{synonym}\', {int(values[1])});"
            cursor.execute(sql)
        #else:
      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertDG():
  filename = dir_path + "gene_OMIM.txt"
  with open(filename) as file:
    # gene_symbol     disease_OMIM_ID
    #   0                 1
    header = file.readline()
    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for line in file:
        values = line.strip().split('\t')
        sql = f"INSERT INTO gene_disease (gene_symbol, OMIM_id) values (\'{values[0]}\', \'{values[1]}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

# Compound.csv  CompoundsHealthEffect.csv  CompoundsPathway.csv  Content.csv
# Food.csv  HealthEffect.csv  Pathway.csv  SMP_proteins.csv

def insertGenePathway():
  filename = dir_path + "SMP_proteins.csv"
  with open(filename,'r',newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        if row[7]:
          sql = f"INSERT INTO gene_pathway (smpdb_id, gene_symbol, pathway_name, pathway_subject, uniprot_id, locus) \
                  values (\'{row[0]}\', \'{row[7]}\', \'{row[1]}\', \'{row[2]}\', \'{row[3]}\', \'{row[8]}\');"
          cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertPathway():
  filename = dir_path + "Pathway.csv"
  with open(filename,'r', newline='', encoding='utf-8') as file:
    # compound_id name annotation
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        sql = f"INSERT INTO pathway (pathway_id, smpdb_id) values (\'{row[0]}\', \'{row[1]}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertCompound():
  filename = dir_path + "Compound.csv"
  with open(filename,'r', newline='', encoding='utf-8') as file:
    # compound_id name annotation
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        name = row[2].replace("'","''")
        ann = row[5].replace("'","''").strip()
        sql = f"INSERT INTO compound (compound_id, name, annotation) values ({int(row[0])}, \'{name}\', \'{ann}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertCompoundPathway():
  filename = dir_path + "CompoundsPathway.csv"
  with open(filename,'r', newline='', encoding='utf-8') as file:
    # compound_id name annotation
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        sql = f"INSERT INTO compound_pathway (cp_id, compound_id, pathway_id) values ({int(row[0])}, {int(row[1])}, \'{row[2]}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertFood():
  filename = dir_path + "Food.csv"
  with open(filename,'r', newline='', encoding='utf-8') as file:
    # compound_id name annotation
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        name = row[1].replace("\'","\'\'")
        sql = f"INSERT INTO food (food_id, food_name, food_group) values ({int(row[0])}, \'{name}\', \'{row[11]}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertCompoundFood():
  filename = dir_path + "Content.csv"
  with open(filename,'r', newline='', encoding='utf-8') as file:
    # compound_id name annotation
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        if row[2] == 'Compound':
          sql = f"INSERT INTO compound_food (cpf_id, compound_id, food_id, amount) values ({int(row[0])}, {int(row[1])}, \'{row[3]}\', \'{row[10] if row[10] else 0}\');"
          cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertHealth():
  filename = dir_path + "HealthEffect.csv"
  with open(filename,'r', newline='', encoding='utf-8') as file:
    # compound_id name annotation
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        name = row[1].replace("\'","\'\'")
        des = row[2].strip() + row[9].strip()
        des = des.replace("\'","\'\'")
        des = des.replace(u'\xa0',u' ')
        sql = f"INSERT INTO health (health_effect_id, name, description) values ({int(row[0])}, \'{name}\', \'{des}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return

def insertCompoundHealth():
  filename = dir_path + "CompoundsHealthEffect.csv"
  with open(filename,'r', newline='', encoding='utf-8') as file:
    # compound_id name annotation
    reader = csv.reader(file)
    next(reader) # skip header

    try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      for row in reader:
        sql = f"INSERT INTO compound_health (compound_id, health_effect_id) values ({int(row[1])}, \'{int(row[2])}\');"
        cursor.execute(sql)

      connection.commit()
      connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
      connection.close()

    file.close()
  return
