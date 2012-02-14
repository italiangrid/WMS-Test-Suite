import socket
import paramiko

from Exceptions import *


def open_ssh(host,user,passwd,utils):

  try:

        utils.log_info("Create ssh connection for host %s"%host)

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(host,username=user,password=passwd)


  except (socket.error,paramiko.BadHostKeyException,paramiko.AuthenticationException,paramiko.SSHException) , e:
         utils.log_info("Error description => %s"%e)
         raise GeneralError("method open_ssh","Unable to create ssh connection for host %s. Error description => %s"%(host,e))

  return ssh


def close_ssh(ssh,utils):

        utils.log_info("Close ssh connection")

        ssh.close()


def ssh_put_file(ssh,src,dst,utils):

        utils.log_info("Send file: %s at remote host"%(file))

        try:

            ftp = ssh.open_sftp()

            ftp.put(src,dst)

            ftp.close()

        except Exception, e:
           utils.log_info("Error while transfer file %s at remote host"%src)
           utils.log_info("Error Description: %s"%e)
           raise GeneralError("Method ssh_put_file","Error while transfer file %s at remote host"%(src))


def ssh_get_file(ssh,src,dst,utils):

        utils.log_info("Get file: %s from remote host"%(file))

        try:

            ftp = ssh.open_sftp()

            ftp.get(src,dst)

            ftp.close()

        except Exception, e:
           utils.log_info("Error while transfer file %s from remote host"%src)
           utils.log_info("Error Description: %s"%e)
           raise GeneralError("Method ssh_get_file","Error while transfer file %s from remote host"%(src))


def execute_remote_cmd(ssh,cmd,utils):

       utils.log_info("Execute remote command %s"%cmd)

       stdin,stdout,stderr=ssh.exec_command(cmd)

       errors=stderr.readlines()
       output_lines=stdout.readlines()

       output=' '.join(output_lines)


       if len(errors)!=0 :

          #Warning during glite-wms-wmproxy restart
          if errors[0].find("warn")==-1 :
            utils.log_info("Error while executing remote command => %s"%cmd)
            utils.log_info("Error Description: %s"%errors)
            raise GeneralError("Method execute_remote_cmd","Error while executing remote command => %s"%(cmd))
       else:
         utils.log_info('Command %s executed successfully'%cmd)
         utils.log_info("Command output: %s"%output,'DEBUG')

       return output


def execute_remote_cmd_failed(ssh,cmd,utils):

       utils.log_nfo("Execute remote command %s"%cmd)

       stdin,stdout,stderr=ssh.exec_command(cmd)

       errors=stderr.readlines()
       output_lines=stdout.readlines()

       output=' '.join(output_lines)

       if len(errors)!=0 :
          error_msg=' '.join(errors)
          utils.log_info("Command error message: %s"%error_msg,'DEBUG')

       else:
          utils.log_info("Remote command %s not failed as expected"%cmd)
          raise GeneralError("Method execute_remote_cmd","Error while executing remote command => %s"%(cmd))
         
       return error_msg



#When olds="*" then the method find the current value of the attribute
def change_remote_file(utils,ssh,file,attributes,olds,news):

    utils.log_info("Change attributes at remote file %s"%(file))

    utils.remove("%s/local_copy"%(utils.get_tmp_dir()))

    try:

            execute_remote_cmd(ssh, "cp -f %s %s.bak"%(file,file))

            ftp = ssh.open_sftp()

            utils.log_info("Get file %s"%(file))

            #Get required file from remote host
            ftp.get(file,"%s/local_copy"%(utils.get_tmp_dir()))

            utils.log_info("Read file %s"%(file))

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


                utils.log_info("For attribute %s change the value from %s to %s"%(attribute,old,new))

                for line in lines:

                    if line.find("=")!= -1:

                       attr=line.split("=")

                       if attr[0].strip()==attribute  and attr[1].find(old)!=-1 :
                            utils.log_info("Attribute %s found."%(attribute))
                            lines[lines.index(line)]=line.replace(old,new)
                            find=1

                if find==0:
                    utils.log_info("Unable to find attribute %s"%(attribute))
                    raise GeneralError("Method change_remote_file","Unable to find attribute %s"%(attribute))

                counter=counter+1

            #write changes to local copy of file
            utils.log_info("Save changes to %s/local_copy"%(utils.get_tmp_dir()))
            FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"w")
            FILE.writelines(lines)
            FILE.close()

            #Save file again to remote host
            utils.log_info("Upload new version of file %s to remote host"%(file))
            ftp.put("%s/local_copy"%(utils.get_tmp_dir()),file)

            ftp.close()


    except Exception, e:
            utils.log_info("Error while edit file %s at remote host"%file)
            utils.log_info("Error Description: %s"%e)
            raise GeneralError("Method change_remote_file","Error while edit file %s at remote host"%(file))

