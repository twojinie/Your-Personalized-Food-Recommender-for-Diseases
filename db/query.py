import psycopg2, sys, io
from prettytable import PrettyTable

IP_ADDRESS = ""
PORT = ""
DB_NAME = ""
ID = ""
PASSWD = ""

"""
3-0. Search compound info by disease name
"""
def searchCombyOMIM(name):
  try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      firstsql = f"SELECT gd.gene_symbol from gene_disease gd where gd.OMIM_id = ( \
                  SELECT omim_id from disease where disease_name = \'{name}\');"
      cursor.execute(firstsql)
      rs = cursor.fetchall()
      symbol = [r[0] for r in rs]
      syn = set(symbol)

      for gene in symbol:
        secondsql = f"SELECT gene_synonyms.synonyms FROM gene NATURAL JOIN gene_synonyms WHERE gene.symbol = \'{gene}\'"
        cursor.execute(secondsql)
        rs = cursor.fetchall()
        for r in rs:
          syn.add(r[0])

      syn_list = '\', \''.join(list(syn))

      sql = f"SELECT cp.name, gp.pathway_subject \
                FROM compound cp \
                JOIN compound_pathway cpath ON cp.compound_id = cpath.compound_id \
                JOIN pathway path ON cpath.pathway_id = path.pathway_id \
                JOIN gene_pathway gp ON path.smpdb_id = gp.smpdb_id \
                WHERE gp.gene_symbol IN (\'"+syn_list+"\');"

      cursor.execute(sql)
      rs = cursor.fetchall()

      columns = [desc[0] for desc in cursor.description]
      table = PrettyTable(["#"] + columns)
      for i, row in enumerate(rs, start=1):
        table.add_row([i] + list(row))
      print(table)

      connection.close()

  except psycopg2.Error as e:
      print(e)

  except RuntimeError as e:
      print(e)

  finally:
      connection.close()
  return

"""
3-1. Search food info (food_id, food_name, food_group) by disease name
"""

def searchFoodbyOMIM(name):
  try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      firstsql = f"SELECT gd.gene_symbol from gene_disease gd where gd.OMIM_id = ( \
                  SELECT omim_id from disease where disease_name = \'{name}\');"
      cursor.execute(firstsql)
      rs = cursor.fetchall()
      symbol = [r[0] for r in rs]
      syn = set(symbol)

      for gene in symbol:
        secondsql = f"SELECT gene_synonyms.synonyms FROM gene NATURAL JOIN gene_synonyms WHERE gene.symbol = \'{gene}\'"
        cursor.execute(secondsql)
        rs = cursor.fetchall()
        for r in rs:
          syn.add(r[0])

      syn_list = '\', \''.join(list(syn))

      sql = f"SELECT DISTINCT cf.amount AS am, cf.food_id, cf.compound_id \
                FROM compound_food cf \
                JOIN compound c ON cf.compound_id = c.compound_id \
                JOIN compound_pathway cp ON c.compound_id = cp.compound_id \
                JOIN pathway p ON cp.pathway_id = p.pathway_id \
                JOIN gene_pathway gp ON p.smpdb_id = gp.smpdb_id \
                WHERE gp.gene_symbol IN (\'"+syn_list+"\') \
                ORDER BY am DESC;"
      cursor.execute(sql)
      topamount = cursor.fetchall()
      top_food = {}   # food_id: [compound_id, amount]

      for r in topamount:
        if len(top_food) <5:
          if r[1] not in top_food:
            top_food[r[1]] = [r[2], r[0]]
        else: break
      top_food_l = '\', \''.join(map(str, top_food))

      if topamount:
        sql = f"SELECT food_id, food_name, food_group from food f where f.food_id in (\'"+top_food_l+"\');"
        cursor.execute(sql)
        rs = cursor.fetchall()
        table = PrettyTable(['food_name', 'food_group', 'compound_name', 'amount'] )

        for row in rs:
          sql = f"SELECT name from compound where compound_id = \'"+str(top_food[row[0]][0])+"\';"
          cursor.execute(sql)
          name = cursor.fetchone()
          table.add_row([row[1], row[2]] + [name[0]] + [top_food[row[0]][1]])
        table.sortby = 'amount'
        table.reversesort = True
        print(table)

      else:
        print("no food")

      connection.close()

  except psycopg2.Error as e:
      print(e)

  except RuntimeError as e:
      print(e)

  finally:
      connection.close()
  return

"""3-2. search health info by compound name """
def searchHealthbyCom(name):
  try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()
      name = name.replace("\'","\'\'")
      sql = f"SELECT name, description from health h where h.health_effect_id in \
       (SELECT ch.health_effect_id from compound_health ch where ch.compound_id = \
       (SELECT compound_id from compound where name = \'{name}\')) ;"

      cursor.execute(sql)

      rs = cursor.fetchall()

      columns = [desc[0] for desc in cursor.description]
      table = PrettyTable(["#"] + columns)
      table.max_width["description"] = 60
      table.align["description"] = "l"
      for i, row in enumerate(rs, start=1):
        table.add_row([i] + list(row))
      print(table)

      connection.close()

  except psycopg2.Error as e:
      print(e)

  except RuntimeError as e:
      print(e)

  finally:
      connection.close()
  return

""" 3-3. searh food info by compound name """
def searchFoodbyCom(name):
  try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      name = name.replace("\'","\'\'")

      sql = f"SELECT food_name, food_group from food f where f.food_id in\
              (SELECT cf.food_id from compound_food cf where cf.compound_id = \
              (SELECT compound_id from compound where name = \'{name}\'));"

      cursor.execute(sql)

      rs = cursor.fetchall()

      columns = [desc[0] for desc in cursor.description]
      table = PrettyTable(["#"] + columns)
      for i, row in enumerate(rs, start=1):
        table.add_row([i] + [row[0].encode().decode('utf-8'), row[1]])

      stdout_wrapper = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
      temp_output = io.StringIO()
      sys.stdout = temp_output
      print(table)
      output_contents = temp_output.getvalue()
      sys.stdout = stdout_wrapper
      print(output_contents)

      connection.close()

  except psycopg2.Error as e:
      print(e)

  except RuntimeError as e:
      print(e)

  finally:
      connection.close()
  return

"""3-4. search compound info by compound name """
def searchComp(name):
  try:
      connection = psycopg2.connect(dbname=DB_NAME, user=ID, password=PASSWD,
                                    host=IP_ADDRESS, port=PORT)
      cursor = connection.cursor()

      name = name.replace("\'","\'\'")
      sql = f"SELECT annotation from compound where name = \'{name}\';"

      cursor.execute(sql)

      rs = cursor.fetchall()
      for r in rs:
        print(r[0])

      connection.close()

  except psycopg2.Error as e:
      print(e)

  except RuntimeError as e:
      print(e)

  finally:
      connection.close()
  return
