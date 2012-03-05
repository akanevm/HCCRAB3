from scripts.server import create_functional_tests,robot,compress_summary_table,blacklist,external_queue_update,add_site_to_ft,remove_site_from_templates,event_processor
from scripts.submit import register_host,create_at_job,test_generate,test_submit,test_report,test_alarm,test_summary

class CronActions:

  def event_processor(self,app,dic):
    ep = event_processor.EventProcessor()
    ep.run(app,dic)

  def blacklist(self,app,dic):
    bl = blacklist.Blacklist()
    bl.run(app,dic)

  def add_site_to_ft(self,app,dic):
    af = add_site_to_ft.AddSiteToFT()
    af.run(app,dic)

  def remove_site_from_templates(self,app,dic):
    rs= remove_site_from_templates.RemoveSiteFromTemplates()
    rs.run(app,dic)

  def external_queue_update(self,app,dic):
    qu = external_queue_update.ExternalQueueUpdate()
    qu.run(app,dic)

  def create_functional_tests(self,app,dic):
    cft = create_functional_tests.CreateFunctionalTests()
    cft.run(app,dic)

  def compress_summary_table(self,app,dic):
    cst = compress_summary_table.CompressSummaryTable()
    cst.run(app,dic)   

  def register_host(self,app,dic):
    rh = register_host.RegisterHost()
    rh.run(app,dic)

  def create_at_job(self,app,dic):
    caj = create_at_job.CreateAtJob()
    caj.run(app,dic)

  def test_generate(self,app,dic):
    tg = test_generate.TestGenerate()
    tg.run(app,dic)

  def test_submit(self,app,dic):
    ts = test_submit.TestSubmit()
    ts.run(app,dic)

  def test_report(self,app,dic):
    tr = test_report.TestReport()
    tr.run(app,dic)

  def robot(self,app,dic):
    r = robot.Robot()
    r.run(app,dic)

  def test_alarm(self,app,dic):
    ta = test_alarm.TestAlarm()
    ta.run(app,dic)

  def test_summary(self,app,dic):
    tp = test_summary.TestSummary()
    tp.run(app,dic)
