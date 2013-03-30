#
# Bug: 98524
# Title:  glite-wms-job-output requires a valid delegated proxy on the WMS to enable output retrieval
# Link: https://savannah.cern.ch/bugs/?98524
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='98524'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
 
    logging.info("Submit a job and wait to finish")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    utils.add_jdl_attribute(utils.get_jdl_file(),"myproxyserver","")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    prefix=JOBID.split("https://%s:9000/"%(utils.get_WMS()))[1][0:2]

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    sbd_files=utils.execute_remote_cmd(ssh,"ls -l /var/SandboxDir/%s"%(prefix))

    target=""

    for line in sbd_files.split("\n"):

       if line.find(JOBID.split("https://%s:9000/"%(utils.get_WMS()))[1])!=-1:
          target="https_%s"%(line.lstrip().split("https_")[1])

    logging.info("Wait until job finished")
    
    utils.wait_until_job_finishes(JOBID)

    logging.info("Check job's final status")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done") != -1:

         logging.info("Get user proxy files from the job sandbox")

         output = utils.execute_remote_cmd(ssh,"find /var/SandboxDir/%s/%s/ -iname \"*proxy*\""%(prefix,target))

         proxy_files=[]

         for proxy in output.split("\n"):
           if proxy.find("user.proxy")!=-1:
              proxy_files.append(proxy.strip(" \n\t"))

         logging.info("User proxy files: %s"%(proxy_files))

         logging.info("Remove the user proxy files")

         for proxy in proxy_files:
            utils.execute_remote_cmd(ssh,"rm -f %s"%(proxy))

         utils.remove(utils.get_tmp_file())

         logging.info("Retrieve the output")

         utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

         utils.info("Check if the output files are correctly retrieved")

         if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
               logging.info("Output files are correctly retrieved")
         else:
               logging.error("Output files are not correctly retrieved")
               raise GeneralError("Check output files","Output files are not correctly retrieved")

    else:
         logging.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
         raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
