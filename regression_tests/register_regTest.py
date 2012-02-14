#! /usr/bin/python

import sys
import getopt
import sqlite
import string
import os.path


def usage(cmd):

        print '\nUsage: '
        print ''
        print '%s [-h] [-f <filename>]'%(cmd)
        print ''
        print " -h               this help"
        print " -f <filename>    filename"
        print ""


def register_from_file(filename):

    bug_number=''
    link=''
    summary=''
    description=''

    print "\n\n+----------------------------------------------+"
    print "   Register regression test (reading from file)"
    print "+----------------------------------------------+"

    FILE = open(filename,"r")
    lines=FILE.readlines()
    FILE.close()


    for line in lines:
                
        line=string.strip(line)

        if line.find("Bug")!=-1:
           ret=line.split("Bug:")
           bug_number=string.strip(ret[1])

        if line.find("Link")!=-1:
           ret=line.split("Link:")
           link=ret[1]

        if line.find("Summary")!=-1:
           ret=line.split("Summary:")
           summary=ret[1]

    counter=0

    
    for line in lines:
                
        line=string.strip(line)

        if line.find("Description")!=-1:
           description="".join(lines[counter+1:len(lines)])

        counter=counter+1
    

    print "\n"
    print "+-----------------------------+"
    print "   Regression Test Details"
    print "+-----------------------------+"
    print ""
    print " Bug Number: %s"%(bug_number)
    print ""
    print " Link: %s"%(link)
    print ""
    print " Summary: %s"%(summary)
    print ""
    print " Description: %s"%(description)
    print ""

    ans=raw_input("Continue with regristration ? (y/n):")

    while ans!='y' and ans!='n':
        ans=raw_input("Continue with regristration ? (y/n):")

    if ans=='y':
      insert_to_db(bug_number,link,summary,description)

    print "\n"



def register_interactive():

    bug_number=''
    link=''
    summary=''
    description=''

    print "\n\n+----------------------------------------------+"
    print "   Register regression test (Interactive mode)"
    print "+----------------------------------------------+\n\n"

    bug_number=raw_input("Bug Number:")
    
    print ""
    link=raw_input("Link:")
    print ""
    summary=raw_input("Summary:")
    print ""
    description=raw_input("Description:")
    print ""

    #print and get answer
    print "\n"
    print "+-----------------------------+"
    print "   Regression Test Details"
    print "+-----------------------------+"
    print ""
    print " Bug Number: %s"%(bug_number)
    print " Link: %s"%(link)
    print " Summary: %s"%(summary)
    print " Description: %s"%(description)
    print ""

    ans=raw_input("Continue with regristration ? (y/n):")

    while ans!='y' and ans!='n':
        ans=raw_input("Continue with regristration ? (y/n):")

    if ans=='y':
      insert_to_db(bug_number,link,summary,description)

    print "\n"

def insert_to_db(bug_number,link,summary,description):


    if check_requirements(bug_number)==1:

        con = sqlite.connect('testdata/tests.db')

        cur=con.cursor()

        cur.execute("select * from tests where bug_number='%s'"%(bug_number))

        if cur.rowcount==0:
            cur.execute("insert into tests(bug_number,link,summary,description) values('%s','%s','%s','%s')"%(bug_number,link,summary,description))
            con.commit()
        else:
            print ""
            print "Regression test for bug %s is already registered."%(bug_number)
            print ""

        con.close()

    else:

        print ""
        print "It seems there is no module %s at bugs package.\nUnable to complete the regression test registration."%(bug_number)
        print ""


def check_requirements(bug_number):


    module_name="bugs/%s.py"%(bug_number)

    if os.path.isfile(module_name):
        return 1
    else:
        return 0


def main():

    input_file=''
    interactive=1
    
    try:

          opts,sys.argv[1:] = getopt.getopt(sys.argv[1:],'hf:')

    except getopt.GetoptError,err:

          print ''
          print str(err)
          usage(sys.argv[0])
          sys.exit(0)

    for option,value in opts:

         if option=="-h":
            usage(sys.argv[0])
            sys.exit(0)
         elif option=="-f":
            input_file=value
            interactive=0


    if interactive==1:
         register_interactive()
    else:

         if os.path.isfile(input_file):
            register_from_file(input_file)
         else:         
            print ""
            print "+-----------------------------------------------------------------------+"
            print "Unable to continue , can not find the input file: %s"%(input_file)
            print "+-----------------------------------------------------------------------+"
            print ""
            sys.exit(0)



if __name__ == "__main__":
    main()



