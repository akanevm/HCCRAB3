from hc.core.utils.generic.class_func import custom_import

import os
import os.path

class TestSubmit:

  def check(self,app,dic):
    if app == 'core':
      print '[ERROR][%s][test_submit] not available at core app.'%(app)
      return 0

    if not dic.has_key('-t'):
      print '[ERROR][%s][test_submit] Test ID missing.'%(app)
      return 0

    try:
      testid = int(dic['-t'])
    except ValueError:
      print '[ERROR][%s][test_submit] <int>TestID expected, got %s'%(app,dic['-t'])
      return 0

    #IMPORT
    test = custom_import('hc.%s.models.Test'%(app))

    try:
      test = test.objects.get(pk=testid)
    except:
      print '[ERROR][%s][test_submit] Could not get test with id %s from DB.'%(app,testid)
      return 0

    if not test.state == 'submitting':
      print '[ERROR][%s][test_submit] Test %s is on state %s, instead of submitting.'%(app,test.id,test.state)
      return 0

    print '[INFO][%s][test_submit] Submitting jobs for Test %s.'%(app,testid)

    return test
   
  
  def submit(self,test,app,dic):

    # Path of the working directory
    if os.environ.has_key('HCDIR'):
      HCDIR = os.environ['HCDIR']
    else:
      print '[ERROR][%s][test_submit] No HCDIR found'%(app)
      return 0
    
    if os.environ.has_key('HCAPP'):
      HCAPP = os.environ['HCAPP']
    else:
      print '[ERROR][%s][test_submit] No HCAPP found'%(app)
      return 0

    # Check if the application has an specific script for this task
    if os.path.exists('%s/scripts/submit/test-submit.sh' % HCAPP):
      base = HCAPP
    else:
      print '[INFO][%s][test_submit] Specific test_submit does not exist.'%(app)
      base = HCDIR

    print '[INFO][%s][test_submit] /bin/sh %s/scripts/submit/test-submit.sh %d "%s %s"'%(app,base,test.id,test.extraargs,test.testoption.submit)
    result =  os.system('/bin/sh %s/scripts/submit/test-submit.sh %d "%s %s"'%(base,test.id,test.extraargs,test.testoption.submit))

    #0 means good in shell scripting.
    if result == 0:
      return 1
    return 0

  def run(self,app,dic):
    
    test = self.check(app,dic)
    if test:
      if self.submit(test,app,dic):
        test.state = 'running'
        test.save()
        print "[INFO][%s][test_submit] Test %d. Successfully submitted."%(app,test.id)
        return 1      
      else:
        test.state = 'error'
        test.save()
        print "[ERROR][%s][test_submit] Test %d. Marking as submitted anyway to prevent infinite submission loop."%(app,test.id)
        return 0
    else:
      return 0
