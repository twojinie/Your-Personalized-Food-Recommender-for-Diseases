from db.schema import createTable, createIndex
from db.insert import *
from db.query import *

if __name__ == '__main__':

  createTable()
  createIndex()
  dir_path = "/work/home/bis332/bio_data/"
  # disease_OMIM.txt  gene_OMIM.txt  Homo_sapiens_gene_info.txt
  insertDisease()
  insertGene()
  insertDG()
  dir_path = "/work/home/project/phase3/"
  # Compound.csv  CompoundsHealthEffect.csv  CompoundsPathway.csv  Content.csv
  # Food.csv  HealthEffect.csv  Pathway.csv  SMP_proteins.csv
  insertGenePathway()
  insertPathway()
  insertCompound()
  insertCompoundPathway()
  insertFood()
  insertCompoundFood()
  insertHealth()
  insertCompoundHealth()

  # greeting
  print("    ______                 ____        \n\
   / ____/ ____   ____    / __ \  ___   ___   \n\
  / /_    / __ \ / __ \  / / / / / _ \ / _ \ \n\
 / __/   / /_/ // /_/ / / /_/ / /  __//  __/\n\
/_/      \____/ \____/ /_____/  \___/ \___/ \n\
                                            ")
  print("------------------------------")
  print("BIPro Spring Class 2023-06-05")
  print("Hello ! we are team 6")
  print("------------------------------")
  active = True
  while active:
    # print option
    print("0: Find compounds related to a disease")
    print("1: Suggest healthy foods for a disease")
    print("2: Discover health effects of a compound")
    print("3: Get a list of foods with a specific compound")
    print("4: Learn about a compound's description")
    print("e: exit")
    print("------------------------------")
    print("Enter option you want to execute: ")
    x = input()
    if x == str(0):
      print("Enter disease name: ")
      omim_id = input()
      print("Compounds related to the disease " + omim_id + " are as follows")
      searchCombyOMIM(omim_id)
    elif x == str(1):
      print("Enter disease name: ")
      omim_id = input()
      print("Suggestion of healthy foods for the disease " + omim_id + " are as follows")
      searchFoodbyOMIM(omim_id)
    elif x == str(2):
      print("Enter compound name: ")
      compound_id = input()
      print("Health effects of a compound " + compound_id + " are as follows")
      searchHealthbyCom(compound_id)
    elif x == str(3):
      print("Enter compound name: ")
      compound_id = input()
      print("Foods which has compound " + compound_id + " are as follows")
      searchFoodbyCom(compound_id)
    elif x == str(4):
      print("Enter compound name: ")
      compound_id = input()
      print("Information of compound " + compound_id + " are as follows")
      searchComp(compound_id)
    elif x == 'e':
      active = False
      break
    else:
      print("Input character is not recognized!")

    print("------------------------------")
    print("Would you like to continue? [y/n]")
    if input() == 'n':
      active = False
    print("------------------------------")
