Job (
 name = 'SUSYValidation' ,
 outputsandbox = [] ,
 inputdata = DQ2Dataset (
    match_ce_all = False ,
    accessprotocol = '' ,
    guids = [] ,
    exclude_names = [] ,
    dataset = ####DATASET#### ,
    min_num_files = 0 ,
    tagdataset = [] ,
    names = [] ,
    number_of_files = 0 ,
    use_aodesd_backnav = False ,
    type = '####INPUTTYPE####' 
    ) ,
 merger = None ,
 inputsandbox = [ ] ,
 application = Athena (
    atlas_release = '14.5.0' ,
    atlas_project = '' ,
    atlas_production = '' ,
    exclude_package = [] ,
    options = '' ,
    atlas_cmtconfig = '' ,
    collect_stats = True ,
    exclude_from_user_area = [] ,
    atlas_exetype = 'ATHENA' ,
    user_setupfile = File (
       name = '' ,
       subdir = '.' 
       ) ,
    option_file = [ File (
       name = '####JOBOPTIONS####' ,
       subdir = '.' 
       ) , ] ,
    group_area = File (
       name = '' ,
       subdir = '.' 
       ) ,
    user_area = File (
       name = '####USERAREA####' ,
       subdir = '.' 
       ) 
    ) ,
 outputdata = DQ2OutputDataset (
    datasetname = '####OUTPUTDATASETNAME####' ,
    use_shortfilename = False ,
    outputdata = ['SUSYValidation.root'] ,
    local_location = '' ,
    location = '' 
    ) ,
 splitter = DQ2JobSplitter (
   numsubjobs = 1 ,
   numfiles = 0 ,
   use_lfc = False ,
   update_siteindex = False,
   use_blacklist = False
 ) ,
 backend = NG (
    check_availability = False ,
    submit_options = [] ,
    middleware = 'ARC' ,
    CE = ####SITES#### ,
    clean = [] ,
    RejectCE = '' ,
    requirements = NGRequirements (
       runtimeenvironment = ['APPS/HEP/ATLAS-14.5.0'] ,
       cputime = 1440 ,
       other = [] ,
       memory = 1500 ,
       disk = 1000 ,
       walltime = 1440
       )
    )

 ) 

