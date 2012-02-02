import socket
import paramiko
import logging

from Exceptions import *


def open_ssh(host,user,passwd):

  try:

        logging.info("Create ssh connection for host %s",host)

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(host,username=user,password=passwd)


  except (socket.error,paramiko.BadHostKeyException,paramiko.AuthenticationException,paramiko.SSHException) , e:
         logging.error("Error description => %s",e)
         raise GeneralError("method open_ssh","Error description => %s"%(e))

  return ssh


def close_ssh(ssh):

        logging.info("Close ssh connection")

        ssh.close()


def ssh_put_file(ssh,src,dst):

        logging.info("Send file: %s at remote host"%(file))

        try:

            ftp = ssh.open_sftp()

            ftp.put(src,dst)

            ftp.close()

        except Exception, e:
           logging.error("Error while transfer file %s at remote host",src)
           logging.error("Error Description: %s",e)
           raise GeneralError("Method ssh_put_file","Error while transfer file %s at remote host"%(src))


def ssh_get_file(ssh,src,dst):

        logging.info("Get file: %s from remote host"%(file))

        try:

            ftp = ssh.open_sftp()

            ftp.get(src,dst)

            ftp.close()

        except Exception, e:
           logging.error("Error while transfer file %s from remote host",src)
           logging.error("Error Description: %s",e)
           raise GeneralError("Method ssh_get_file","Error while transfer file %s from remote host"%(src))



def execute_remote_cmd(ssh,cmd):

       logging.info("Execute remote command %s",cmd)

       stdin,stdout,stderr=ssh.exec_command(cmd)

       errors=stderr.readlines()
       output_lines=stdout.readlines()

       output=' '.join(output_lines)


       if len(errors)!=0 :

          #Warning during glite-wms-wmproxy restart
          if errors[0].find("warn")==-1 :
            logging.error("Error while executing remote command => %s",cmd)
            logging.error("Error Description: %s",errors)
            raise GeneralError("Method execute_remote_cmd","Error while executing remote command => %s"%(cmd))
       else:
         logging.info('Command %s executed successfully',cmd)
         logging.debug("Command output: %s",output)

       return output


def execute_remote_cmd_failed(ssh,cmd):

       logging.info("Execute remote command %s",cmd)

       stdin,stdout,stderr=ssh.exec_command(cmd)

       errors=stderr.readlines()
       output_lines=stdout.readlines()

       output=' '.join(output_lines)

       if len(errors)!=0 :
          error_msg=' '.join(errors)
          logging.debug("Command error message: %s",error_msg)

       else:
          logging.error("Remote command %s not failed as expected",cmd)
          raise GeneralError("Method execute_remote_cmd","Error while executing remote command => %s"%(cmd))
         
       return error_msg


#When olds="*" then the method find the current value of the attribute
def change_remote_file(utils,ssh,file,attributes,olds,news):

    logging.info("Change attributes at remote file %s"%(file))

    utils.remove("%s/local_copy"%(utils.get_tmp_dir()))

    try:

            execute_remote_cmd(ssh, "cp -f %s %s.bak"%(file,file))

            ftp = ssh.open_sftp()

            logging.info("Get file %s"%(file))

            #Get required file from remote host
            ftp.get(file,"%s/local_copy"%(utils.get_tmp_dir()))

            logging.info("Read file %s"%(file))

            #Read contents from file
            FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"r")
            lines=FILE.readlines()
            FILE.close()

            counter=0
            find=0

            for attribute in attributes:

                old=olds[counter]
                new=news[counter]
                find=0

                #find the current value of attribute
                if old=="*":

                  for line in lines:
                     if line.find(attribute)!=-1:
                        old=line.split("=")[1][:-2].strip()


                logging.info("For attribute %s change the value from %s to %s"%(attribute,old,new))

                for line in lines:

                    if line.find("=")!= -1:

                       attr=line.split("=")

                       if attr[0].strip()==attribute  and attr[1].find(old)!=-1 :
                            logging.info("Attribute %s found."%(attribute))
                            lines[lines.index(line)]=line.replace(old,new)
                            find=1

                if find==0:
                    logging.error("Unable to find attribute %s"%(attribute))
                    raise GeneralError("Method change_remote_file","Unable to find attribute %s"%(attribute))

                counter=counter+1

            #write changes to local copy of file
            logging.info("Save changes to %s/local_copy"%(utils.get_tmp_dir()))
            FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"w")
            FILE.writelines(lines)
            FILE.close()

            #Save file again to remote host
            logging.info("Upload new version of file %s to remote host"%(file))
            ftp.put("%s/local_copy"%(utils.get_tmp_dir()),file)

            ftp.close()


    except Exception, e:
            logging.error("Error while edit file %s at remote host",file)
            logging.error("Error Description: %s",e)
            raise GeneralError("Method change_remote_file","Error while edit file %s at remote host"%(file))

