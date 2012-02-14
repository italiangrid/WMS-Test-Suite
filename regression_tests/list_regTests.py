
#! /usr/bin/python

import sys
import getopt
import sqlite
import os.path
import os


def usage(cmd):

        print '\nUsage: '
        print ''
        print '%s [-h] [-d <level>] [-o <filename>]'%(cmd)
        print ''
        print " -h               this help"
        print " -d <level >      print verbose messages (level = (1|2|3)"
        print " -o <filename>    save only bug numbers at filename"
        print ""


def main():


    verbose=1
    output_file=''
    counter=1


    try:

          opts,sys.argv[1:] = getopt.getopt(sys.argv[1:],'hd:o:')

    except getopt.GetoptError,err:

          print ''
          print str(err)
          usage(sys.argv[0])
          sys.exit(0)

    for option,value in opts:

         if option=="-h":
            usage(sys.argv[0])
            sys.exit(0)
         elif option=="-d":
            verbose=int(value)
         elif option=="-o":
            output_file=value

  
    con = sqlite.connect('testdata/tests.db')

    cur=con.cursor()
   
    cur.execute("select * from tests order by bug_number")


    if cur.rowcount == 0 :
        print "\nUnable to find any registerd test.\n"
    else:

        if output_file!='':

            if os.path.isfile("%s"%(output_file)):
                os.system("rm -f %s"%(output_file))

            for row in cur:
              os.system("echo %s >> %s"%(row[1],output_file))

        else:

            print "\n==============================================="
            print " Total number of available tests %s"%(cur.rowcount)
            print "===============================================\n"

            for row in cur:

                print "-------------- Test %s/%s --------------"%(counter,cur.rowcount)

                print " Bug: %s "%row[1]

                if verbose >1 :
                    print " Link: %s"%(row[2])
                    print " Summary: %s"%(row[3])

                if verbose == 3:
                    print " Description:"
                    print ""
                    print "%s"%(row[4])

                print ""

                counter=counter+1


    con.close()
   


if __name__ == "__main__":
    main()


