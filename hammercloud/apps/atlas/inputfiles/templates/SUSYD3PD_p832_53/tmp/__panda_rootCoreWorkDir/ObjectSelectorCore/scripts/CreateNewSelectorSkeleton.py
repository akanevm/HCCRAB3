#!/usr/bin/env python

#==============================================================================
#
# File:   PrintStatistics.py
#
# Author: Karsten Koeneke (karsten.koeneke@cernSPAMNOT.ch)
#
# Date:   April 2011
#
# Description: This is a helper to print statistics like lumi.
#
#==============================================================================

import user  # look for .pythonrc.py for user init
import os, sys
import getopt
from optparse import OptionParser


#===================================
# The main function... everything is done here
#===================================
def CreateNewSelectorSkeleton(options):
    # First, get the current working directory
    _baseDir = os.getenv("PWD")
    _baseDirList = _baseDir.split("/")

    # Get the name of the selector that should be created
    _selectorName = args[0]
    
    # Get the name of the current package
    try :
        assert isinstance( options.PackageName, str )
        _packageName = options.PackageName
        if _packageName != _baseDirList[ len(_baseDirList)-1 ] :
            print "Your don't seem to be in the main directory of your package. Exiting"
            exit(0)
    except AssertionError:
        _packageName = _baseDirList[ len(_baseDirList)-1 ]
        pass
    print "Using the name of the current package:", _packageName

    # Get the cut value name list
    try :
        assert isinstance( options.DoubleCutNameList, str )
        _doubleCutNameList = options.DoubleCutNameList.split(",")
    except AssertionError:
        _doubleCutNameList = []
        pass
    print "Using the name of the cuts:", _doubleCutNameList
    

    # =========================================================================
    # Create the cmt/ files
    # =========================================================================

    # Go to the Root directory and create the ROOT only package skeleton
    os.chdir(_baseDir)
    try:
        os.chdir("cmt")
        pass
    except OSError:
        print "Creating cmt/ directory..."
        os.mkdir("cmt")
        os.chdir("cmt")
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/cmt/requirements" % _baseDir ):
        print "cmt/requirements file already exist... skipping! Editing may be required; please use run: checkreq.py in the cmt directory to find problems!"
        pass
    else:
        CreateRequirementsFile( _packageName )
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/cmt/Makefile.RootCore" % _baseDir ):
        print "cmt/Makefile.RootCore file already exist... skipping!"
        pass
    else:
        CreateMakefileRootCoreFile( _packageName )
        pass
    os.chdir(_baseDir)

    
    # =========================================================================
    # Create the PackageName/ files
    # =========================================================================

    # Go to the Root directory and create the ROOT only package skeleton
    os.chdir(_baseDir)
    try:
        os.chdir(_packageName)
        pass
    except OSError:
        print "Creating %s/ directory..." % _packageName
        os.mkdir(_packageName)
        os.chdir(_packageName)
        pass
    # Check if the file to be created already exists
    doExit = False
    if os.path.exists( "%s/%s/Ath%s.h" % ( _baseDir, _packageName, _selectorName ) ) :
        print "%s/Ath%s.h file already exist. Exiting" % ( _packageName, _selectorName )
        doExit = True
        pass
    if os.path.exists( "%s/%s/ARA%s.h" % ( _baseDir, _packageName, _selectorName ) ) :
        print "%s/ARA%s.h file already exist. Exiting" % ( _packageName, _selectorName )
        doExit = True
        pass
    if os.path.exists( "%s/%s/T%s.h" % ( _baseDir, _packageName, _selectorName ) ) :
        print "%s/T%s.h file already exist. Exiting" % ( _packageName, _selectorName )
        doExit = True
        pass
    if doExit: exit(0)
    # Check if the file to be created already exists
    if os.path.exists( "%s/%s/%sDict.h" % ( _baseDir, _packageName, _packageName) ):
        print "%s/%s/%sDict.h file already exist... skipping! Some editing may be required" % ( _baseDir, _packageName, _packageName )
        pass
    else:
        CreateDictFile( _packageName, _selectorName )
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/%s/selection.xml" % ( _baseDir, _packageName) ):
        print "%s/%s/selection.xml file already exist... skipping! Some editing may be required" % ( _baseDir, _packageName )
        pass
    else:
        CreateSelectionFile( _packageName, _selectorName )
        pass

    CreateAthSelectorFile( _packageName, _selectorName )
    CreateARASelectorHeaderFile( _packageName, _selectorName )
    CreateTSelectorHeaderFile( _packageName, _selectorName, _doubleCutNameList )
    os.chdir(_baseDir)


    # =========================================================================
    # Create the Root/ files
    # =========================================================================

    # Go to the Root directory and create the ROOT only package skeleton
    os.chdir(_baseDir)
    try:
        os.chdir("Root")
        pass
    except OSError:
        print "Creating Root/ directory..."
        os.mkdir("Root")
        os.chdir("Root")
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/Root/LinkDef.h" % ( _baseDir ) ):
        print "%s/Root/LinkDef.h file already exist... skipping! Some editing may be required" % ( _baseDir )
        pass
    else:
        CreateLinkDefFile( _packageName, _selectorName )
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/Root/T%s.cxx" % ( _baseDir, _selectorName)) :
        print "Root/T%s.cxx file already exist. Exiting" % _selectorName
        exit(0)
        pass
    CreateTSelectorSourceFile( _packageName, _selectorName, _doubleCutNameList )
    os.chdir(_baseDir)


        
    # =========================================================================
    # Create the src/ files
    # =========================================================================

    # Go to the Root directory and create the ROOT only package skeleton
    os.chdir(_baseDir)
    try:
        os.chdir("src")
        pass
    except OSError:
        print "Creating src/ directory..."
        os.mkdir("src")
        os.chdir("src")
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/src/ARA%s.h" % ( _baseDir, _selectorName) ) :
        print "src/ARA%s.cxx file already exist. Exiting" % _selectorName
        exit(0)
        pass
    CreateARASelectorSourceFile( _packageName, _selectorName, _doubleCutNameList )
    try:
        os.chdir("components")
        pass
    except OSError:
        print "Creating src/components/ directory..."
        os.mkdir("components")
        os.chdir("components")
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/src/components/%s_load.cxx" % ( _baseDir, _packageName ) ):
        print "%s/src/components/%s_load.cxx file already exist... skipping!" % ( _baseDir, _packageName )
        pass
    else:
        CreateLoadFile( _packageName )
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/src/components/%s_entries.cxx" % ( _baseDir, _packageName ) ):
        print "%s/src/components/%s_entries.cxx file already exist... skipping! Some editing may be required" % ( _baseDir, _packageName )
        pass
    else:
        CreateEntriesFile( _packageName, _selectorName )
        pass
    os.chdir(_baseDir)





    # =========================================================================
    # Create the python/ files
    # =========================================================================

    # Go to the Root directory and create the ROOT only package skeleton
    os.chdir(_baseDir)
    try:
        os.chdir("python")
        pass
    except OSError:
        print "Creating python/ directory..."
        os.mkdir("python")
        os.chdir("python")
        pass
    # Check if the file to be created already exists
    if os.path.exists( "%s/python/ConfiguredAth%ss.py" % ( _baseDir, _selectorName) ) \
       or os.path.exists( "%s/python/ConfiguredARA%ss.py" % ( _baseDir, _selectorName) ) \
       or os.path.exists( "%s/python/ConfiguredT%ss.py" % ( _baseDir, _selectorName) ) \
       or os.path.exists( "%s/python/%sCutDefs.py" % ( _baseDir, _selectorName.rsplit("Tool",1)[0] ) ) :
        print "python/ConfiguredAth,ARA,T%ss.py files or python/%sCutDefs.py file already exist. Exiting" % ( _selectorName, _selectorName.rsplit("Tool",1)[0] )
        exit(0)
        pass
    CreateConfiguredAthPythonFile( _packageName, _selectorName )
    CreateConfiguredARAPythonFile( _packageName, _selectorName )
    CreateConfiguredTPythonFile( _packageName, _selectorName )
    CreateCutDefsPythonFile( _packageName, _selectorName, _doubleCutNameList )
    # Check if the file to be created already exists
    if os.path.exists( "%s/python/__init__.py" % ( _baseDir ) ):
        print "%s/python/__init__.py file already exist... skipping!" % ( _baseDir )
        pass
    else:
        os.system("touch __init__.py")
        pass


    
    os.chdir(_baseDir)
    print "Done!"
    print "Don't forget to add your new selector to the Root/LinkDef.h, and to the src/components/%s_entries.cxx files" % _packageName

    return





def CreateMakefileRootCoreFile( _packageName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('# Author: Karsten Koeneke (karsten.koeneke@cernSPAMNOT.ch)\n')
    _lineList.append('# %s root stand-alone makefile\n' % _packageName )
    _lineList.append('\n')
    _lineList.append('PACKAGE          = %s\n' % _packageName )
    _lineList.append('PACKAGE_CXXFLAGS = \n')
    _lineList.append('PACKAGE_LDFLAGS  =\n')
    _lineList.append('PACKAGE_DEP      = ObjectSelectorCore\n')
    _lineList.append('\n')
    _lineList.append('include $(ROOTCOREDIR)/Makefile-common\n')

    # Create a file object: in "write" mode
    _file = open( "Makefile.RootCore","w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()
    
    print "Created cmt/Makefile.RootCore"
    return




def CreateRequirementsFile( _packageName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('package %s\n' % _packageName )
    _lineList.append('\n')
    _lineList.append('author Karsten Koeneke <karsten.koeneke@cern.ch>\n')
    _lineList.append('\n')
    _lineList.append('## For Athena policies: it has to be the first use statement\n')
    _lineList.append('use AtlasPolicy                 AtlasPolicy-*\n')
    _lineList.append('\n')
    _lineList.append('use AtlasPyROOT                 AtlasPyROOT-*           External\n')
    _lineList.append('use AtlasROOT                   AtlasROOT-*             External\n')
    _lineList.append('use GaudiInterface              GaudiInterface-*        External\n')
    _lineList.append('use EventKernel                 EventKernel-*           Event\n')
    _lineList.append('use AraTool                     AraTool-*               PhysicsAnalysis\n')
    _lineList.append('use ObjectSelectorCore          ObjectSelectorCore-*    PhysicsAnalysis/AnalysisCommon\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('## macros   \n')
    _lineList.append('apply_tag       ROOTBasicLibs\n')
    _lineList.append('apply_tag       ROOTMathLibs\n')
    _lineList.append('\n')
    _lineList.append('macro_append ROOT_linkopts " -lPyROOT"\n')
    _lineList.append('\n')
    _lineList.append('## declare the directories CMT should know about\n')
    _lineList.append('branches %s python share src Root\n' % _packageName )
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('# Create a named installed library\n')
    _lineList.append('library %sLib *.cxx ../Root/*.cxx\n' % _packageName )
    _lineList.append('apply_pattern named_installed_library library=%sLib\n' % _packageName )
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('## create a component library\n')
    _lineList.append('library %s *.cxx components/*.cxx\n' % _packageName )
    _lineList.append('macro_append %s_dependencies " %sLib"\n' % ( _packageName, _packageName ) )
    _lineList.append('apply_pattern component_library\n')
    _lineList.append('\n')
    _lineList.append('## install our python modules\n')
    _lineList.append('apply_pattern declare_python_modules files="*.py"\n')
    _lineList.append('\n')
    _lineList.append('## install our job options files\n')
    _lineList.append('apply_pattern declare_joboptions files="*.py"\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('## For reflex dictionary generation\n')
    _lineList.append('use AtlasReflex   AtlasReflex-*   External -no_auto_imports\n')
    _lineList.append('apply_pattern lcgdict dict=%s selectionfile=selection.xml headerfiles="..\/%s/%sDict.h"\n'
                     % ( _packageName, _packageName, _packageName ) )

    # Create a file object: in "write" mode
    _file = open( "requirements","w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created cmt/requirements (Editing may be required; please use run: checkreq.py in the cmt directory to find problems!)"
    return





def CreateDictFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('// Dear emacs, this is -*-c++-*-\n')
    _lineList.append('\n')
    _lineList.append('#ifndef __%sDICT__\n' % _packageName.upper() )
    _lineList.append('#define __%sDICT__\n' % _packageName.upper() )
    _lineList.append('\n')
    _lineList.append('/**\n')
    _lineList.append('   @brief For dictionary generation.\n')
    _lineList.append('\n')
    _lineList.append('   @author Karsten Koeneke (CERN)\n')
    _lineList.append('   @date   July 2011\n')
    _lineList.append('\n')
    _lineList.append('*/\n')
    _lineList.append('\n')
    _lineList.append('#include "%s/T%s.h"\n' % ( _packageName, _selectorName ) )
    _lineList.append('#include "%s/ARA%s.h"\n' % ( _packageName, _selectorName ) )
    _lineList.append('#include "%s/Ath%s.h"\n' % ( _packageName, _selectorName ) )
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('#endif\n')

    # Create a file object: in "write" mode
    _file = open( "%sDict.h" % _packageName,"w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created %s/%sDict.h" % ( _packageName, _packageName )
    return




def CreateSelectionFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('<lcgdict>\n')
    _lineList.append('    <class name="Root::T%s" />\n' % _selectorName )
    _lineList.append('    <class name="ARA%s" />\n' % _selectorName )
    _lineList.append('    <class name="Ath%s" />\n' % _selectorName )
    _lineList.append('</lcgdict>\n')

    # Create a file object: in "write" mode
    _file = open( "selection.xml","w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created %s/selection.xml" % ( _packageName )
    return





def CreateLinkDefFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('#ifndef __%s__\n' % _packageName.upper() )
    _lineList.append('#define __%s__\n' % _packageName.upper() )
    _lineList.append('\n')
    _lineList.append('#include <vector>\n')
    _lineList.append('#include <string>\n')
    _lineList.append('#include "TString.h"\n')
    _lineList.append('#include "%s/T%s.h"\n' % ( _packageName, _selectorName ) )
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('#ifdef __CINT__\n')
    _lineList.append('\n')
    _lineList.append('#pragma link off all globals;\n')
    _lineList.append('#pragma link off all classes;\n')
    _lineList.append('#pragma link off all functions;\n')
    _lineList.append('\n')
    _lineList.append('#pragma link C++ namespace Root ;\n')
    _lineList.append('\n')
    _lineList.append('#pragma link C++ class Root::T%s+ ;\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('#endif\n')
    _lineList.append('\n')
    _lineList.append('#endif\n')
    _lineList.append('\n')

    # Create a file object: in "write" mode
    _file = open( "LinkDef.h","w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created Root/LinkDef.h"
    return



def CreateTSelectorSourceFile( _packageName, _selectorName, _doubleCutNameList ) :
    # Create the lines to write to the file
    _tcLineList = []
    _tcLineList.append('// Dear emacs, this is -*-c++-*-\n')
    _tcLineList.append('\n')
    _tcLineList.append('/******************************************************************************\n')
    _tcLineList.append('Name:        T%s\n' % _selectorName )
    _tcLineList.append('\n')
    _tcLineList.append('Author:      Karsten Koeneke (CERN)\n')
    _tcLineList.append('Created:     April 2011\n')
    _tcLineList.append('\n')
    _tcLineList.append('Description: Example tool to select objects in pure ROOT\n')
    _tcLineList.append('******************************************************************************/\n')
    _tcLineList.append('\n')
    _tcLineList.append('// Preprocessor magic for debugging\n')
    _tcLineList.append('#define XXX std::cout << "I am here: " << __FILE__ << ":" << __LINE__ << std::endl;\n')
    _tcLineList.append('\n')
    _tcLineList.append('// This class header\n')
    _tcLineList.append('#include "%s/T%s.h"\n' % ( _packageName, _selectorName ) )
    _tcLineList.append('\n')
    _tcLineList.append('// STL includes\n')
    _tcLineList.append('#include <iostream>\n')
    _tcLineList.append('#include <cfloat>\n')
    _tcLineList.append('#include <math.h>\n')
    _tcLineList.append('\n')
    _tcLineList.append('// ROOT includes\n')
    _tcLineList.append('#include <TString.h>\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('ClassImp(Root::T%s)\n' % _selectorName )
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('// Constructor\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('Root::T%s::T%s(const char* name) :\n' % (_selectorName, _selectorName) )
    _tcLineList.append('  TSelectorToolBase(name),\n')
    for doubleCutName in _doubleCutNameList:
        bound = ""
        if doubleCutName.endswith("Max"): bound = "DBL_MAX"
        elif doubleCutName.endswith("Min"): bound = "DBL_MIN"
        _tcLineList.append('  %s(%s),\n' % ( doubleCutName, bound ) )
        pass
    _tcLineList.append('  m_cutName0("myZeroCut"),\n')
    _tcLineList.append('  m_cutName1("myFirstCut")\n')
    _tcLineList.append('{\n')
    _tcLineList.append('}\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('// Destructor\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('Root::T%s::~T%s()\n' % (_selectorName, _selectorName) )
    _tcLineList.append('{\n')
    _tcLineList.append('}\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('// Initialize this selector tool\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('int Root::T%s::initialize()\n' % _selectorName )
    _tcLineList.append('{\n')
    _tcLineList.append('  // use an int as a StatusCode\n')
    _tcLineList.append('  int sc(1);\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('  // --------------------------------------------------------------------------\n')
    _tcLineList.append('  // Register the cuts and check that the registration worked:\n')
    _tcLineList.append('  // NOTE: THE ORDER IS IMPORTANT!!! Cut0 corresponds to bit 0, Cut1 to bit 1,...\n')
    _tcLineList.append('\n')
    _tcLineList.append('  // Cut 0\n')
    _tcLineList.append('  m_cutPosition0 = m_accept.addCut( m_cutName0, Form("var0 < %g", CutValue0Max) );\n')
    _tcLineList.append('  if ( m_cutPosition0 < 0 ) sc = 0; // Exceeded the number of allowed cuts\n')
    _tcLineList.append('\n')
    _tcLineList.append('  // Cut 1\n')
    _tcLineList.append('  m_cutPosition1 = m_accept.addCut( m_cutName1, Form("var1 < %g", CutValue1Max) );\n')
    _tcLineList.append('  if ( m_cutPosition1 < 0 ) sc = 0; // Exceeded the number of allowed cuts\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('  return sc;\n')
    _tcLineList.append('}\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('// Calculate the actual accept of each cut individually.\n')
    _tcLineList.append('//=============================================================================\n')
    _tcLineList.append('const Root::TAccept& Root::T%s::accept( /*Here, you need to put your doubles and ints to cut on*/ )\n' % _selectorName )
    _tcLineList.append('{\n')
    _tcLineList.append('  // Reset the cut result bits to zero (= fail cut)\n')
    _tcLineList.append('  m_accept.clear();\n')
    _tcLineList.append('\n')
    _tcLineList.append('  // -----------------------------------------------------------\n')
    _tcLineList.append('  // Do the actual selection\n')
    _tcLineList.append('\n')
    _tcLineList.append('  // Cut 0\n')
    _tcLineList.append('  m_accept.setCutResult( m_cutPosition0, ( var0 < CutValue0fMax ) ? true : false );\n')
    _tcLineList.append('\n')
    _tcLineList.append('  // Cut 1\n')
    _tcLineList.append('  m_accept.setCutResult( m_cutPosition1, ( var1 < CutValue1fMax ) ? true : false );\n')
    _tcLineList.append('\n')
    _tcLineList.append('\n')
    _tcLineList.append('  return m_accept;\n')
    _tcLineList.append('}\n')
    _tcLineList.append('\n')

    # Create a file object: in "write" mode
    _tcFile = open( "T%s.cxx" % _selectorName,"w")

    # Write all the lines at once:
    _tcFile.writelines(_tcLineList)
    _tcFile.close()

    print "Created Root/T%s.cxx (editing required!)" % _selectorName
    return






def CreateTSelectorHeaderFile( _packageName, _selectorName, _doubleCutNameList  ) :
    # Create the lines to write to the file
    _thLineList = []
    _thLineList.append('// Dear emacs, this is -*-c++-*-\n')
    _thLineList.append('\n')
    _thLineList.append('#ifndef __T%s__\n' % _selectorName.upper() )
    _thLineList.append('#define __T%s__\n' % _selectorName.upper() )
    _thLineList.append('\n')
    _thLineList.append('/**\n')
    _thLineList.append('   @class T%s\n' % _selectorName )
    _thLineList.append('   @brief Example tool to select objects in pure ROOT\n')
    _thLineList.append('\n')
    _thLineList.append('   @author Karsten Koeneke (CERN)\n')
    _thLineList.append('   @date   April 2011\n')
    _thLineList.append('*/\n')
    _thLineList.append('\n')
    _thLineList.append('\n')
    _thLineList.append('// ROOT includes\n')
    _thLineList.append('#include <TString.h>\n')
    _thLineList.append('\n')
    _thLineList.append('// Include the return object and the base class\n')
    _thLineList.append('#include "ObjectSelectorCore/TAccept.h"\n')
    _thLineList.append('#include "ObjectSelectorCore/TSelectorToolBase.h"\n')
    _thLineList.append('\n')
    _thLineList.append('\n')
    _thLineList.append('namespace Root {\n')
    _thLineList.append('  class T%s : public TSelectorToolBase\n' % _selectorName )
    _thLineList.append('  {\n')
    _thLineList.append('\n')
    _thLineList.append('  public: \n')
    _thLineList.append('    /** Standard constructor */\n')
    _thLineList.append('    T%s(const char* name="T%s");\n' % ( _selectorName, _selectorName ) )
    _thLineList.append('\n')
    _thLineList.append('    /** Standard destructor */\n')
    _thLineList.append('    ~T%s();\n' % _selectorName )
    _thLineList.append('\n')
    _thLineList.append('\n')
    _thLineList.append('    // Main methods\n')
    _thLineList.append('  public:\n')
    _thLineList.append('    /** Initialize this class */\n')
    _thLineList.append('    int initialize();\n')
    _thLineList.append('\n')
    _thLineList.append('    /** Finalize this class; everything that should be done after the event loop should go here */\n')
    _thLineList.append('    inline int finalize() { return 1; };\n')
    _thLineList.append('\n')
    _thLineList.append('    /** The main accept method: the actual cuts are applied here */\n')
    _thLineList.append('    const Root::TAccept& accept( /*Here, you need to put your doubles and ints to cut on*/ );\n')
    _thLineList.append('\n')
    _thLineList.append('\n')
    _thLineList.append('    // Public members (the cut values)\n')
    _thLineList.append('  public:\n')
    _thLineList.append('\n')
    for doubleCutName in _doubleCutNameList:
        boundName = ""
        if doubleCutName.endswith("Max"): boundName = "maximum "
        elif doubleCutName.endswith("Min"): boundName = "minimum "
        _thLineList.append('    /** %s%sHECf cut value */\n' % ( boundName, doubleCutName.rstrip("Max").rstrip("Min")  ) )
        _thLineList.append('    double %s;\n' % doubleCutName )
        _thLineList.append('\n')
        pass
    _thLineList.append('\n')
    _thLineList.append('    // Private members\n')
    _thLineList.append('  private:\n')
    _thLineList.append('\n')
    _thLineList.append('    /** Name of the zeroth cut */\n')
    _thLineList.append('    const TString m_cutName0;\n')
    _thLineList.append('\n')
    _thLineList.append('    /** Position of the zeroth cut */\n')
    _thLineList.append('    int m_cutPosition0;\n')
    _thLineList.append('\n')
    _thLineList.append('\n')
    _thLineList.append('    /** Name of the first cut */\n')
    _thLineList.append('    const TString m_cutName1;\n')
    _thLineList.append('\n')
    _thLineList.append('    /** Position of the first cut */\n')
    _thLineList.append('    int m_cutPosition1;\n')
    _thLineList.append('\n')
    _thLineList.append('\n')
    _thLineList.append('  }; // End: class definition\n')
    _thLineList.append('\n')
    _thLineList.append('} // End: namespace Root\n')
    _thLineList.append('\n')
    _thLineList.append('#endif\n')
    _thLineList.append('\n')

    # Create a file object: in "write" mode
    _thFile = open( "T%s.h" % _selectorName,"w")

    # Write all the lines at once:
    _thFile.writelines(_thLineList)
    _thFile.close()

    print "Created %s/T%s.h (editing required!)" % ( _packageName, _selectorName )
    return







def CreateARASelectorSourceFile( _packageName, _selectorName, _doubleCutNameList ) :
    # Create the lines to write to the file
    _aracLineList = []
    _aracLineList.append('// Dear emacs, this is -*-c++-*-\n')
    _aracLineList.append('\n')
    _aracLineList.append('/**\n')
    _aracLineList.append('   @class ARA%s\n' % _selectorName )
    _aracLineList.append('   @brief Example tool to select objects in AthenaRootAccess using an underlying pure ROOT tool.\n')
    _aracLineList.append('\n')
    _aracLineList.append('   @author Karsten Koeneke (CERN)\n')
    _aracLineList.append('   @date   April 2011\n')
    _aracLineList.append('\n')
    _aracLineList.append('*/\n')
    _aracLineList.append('\n')
    _aracLineList.append('// Include this class\'s header\n')
    _aracLineList.append('#include "%s/ARA%s.h"\n' % ( _packageName, _selectorName ) )
    _aracLineList.append('\n')
    _aracLineList.append('// STL includes\n')
    _aracLineList.append('#include <string>\n')
    _aracLineList.append('#include <cfloat>\n')
    _aracLineList.append('#include <iostream>\n')
    _aracLineList.append('\n')
    _aracLineList.append('// Include the return object\n')
    _aracLineList.append('#include "ObjectSelectorCore/TAccept.h"\n')
    _aracLineList.append('\n')
    _aracLineList.append('// Atlas includes\n')
    _aracLineList.append('#include "EventKernel/INavigable4Momentum.h"\n')
    _aracLineList.append('\n')
    _aracLineList.append('\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('// Standard constructor\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('ARA%s::ARA%s( PropertyMgr *pmgr ):\n' % (_selectorName, _selectorName) )
    _aracLineList.append('  AraToolBase(pmgr),n')
    _aracLineList.append('  ARASelectorToolBase(pmgr),\n')
    _aracLineList.append('  m_rootTool(0)\n')
    _aracLineList.append('{\n')
    _aracLineList.append('  m_rootTool = new Root::TJetCleaningTool();\n')
    _aracLineList.append('  // Declare the needed properties\n')
    for doubleCutName in _doubleCutNameList:
        _aracLineList.append('  declareProperty( "%s",              m_rootTool->%s,              "Cut %s");\n'
                             % (doubleCutName, doubleCutName, doubleCutName) )
        pass
    _aracLineList.append('}\n')
    _aracLineList.append('\n')
    _aracLineList.append('\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('// Standard destructor\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('ARA%s::~ARA%s()\n' % (_selectorName, _selectorName) )
    _aracLineList.append('{\n')
    _aracLineList.append('  if ( m_rootTool ) delete m_rootTool;\n')
    _aracLineList.append('}\n')
    _aracLineList.append('\n')
    _aracLineList.append('\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('// Athena initialize method\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('StatusCode ARA%s::initialize()\n' % _selectorName )
    _aracLineList.append('{\n')
    _aracLineList.append('  // The standard status code\n')
    _aracLineList.append('  StatusCode sc = StatusCode::SUCCESS ;\n')
    _aracLineList.append('\n')
    _aracLineList.append('  // We need to initialize the underlying ROOT TSelectorTool\n')
    _aracLineList.append('  if ( 0 == m_rootTool->initialize() )\n')
    _aracLineList.append('    {\n')
    _aracLineList.append('      std::cerr << "ERROR! Could not initialize the T%s!" << std::endl;\n' % _selectorName )
    _aracLineList.append('      sc = StatusCode::FAILURE;\n')
    _aracLineList.append('      return sc;\n')
    _aracLineList.append('    }\n')
    _aracLineList.append('\n')
    _aracLineList.append('  return sc ;\n')
    _aracLineList.append('}\n')
    _aracLineList.append('\n')
    _aracLineList.append('\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('// Athena finalize method\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('StatusCode ARA%s::finalize()\n' % _selectorName )
    _aracLineList.append('{\n')
    _aracLineList.append('  // The standard status code\n')
    _aracLineList.append('  StatusCode sc = StatusCode::SUCCESS ;\n')
    _aracLineList.append('\n')
    _aracLineList.append('  if ( !(m_rootTool->finalize()) )\n')
    _aracLineList.append('    {\n')
    _aracLineList.append('      std::cerr << "ERROR! Something went wrong at finalize!" << std::endl;\n')
    _aracLineList.append('      sc = StatusCode::FAILURE;\n')
    _aracLineList.append('    }\n')
    _aracLineList.append('\n')
    _aracLineList.append('  return sc ;\n')
    _aracLineList.append('}\n')
    _aracLineList.append('\n')
    _aracLineList.append('\n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('// The main accept method: the actual cuts are applied here \n')
    _aracLineList.append('//=============================================================================\n')
    _aracLineList.append('const Root::TAccept& ARA%s::accept( const INavigable4Momentum* part )\n' % _selectorName )
    _aracLineList.append('{\n')
    _aracLineList.append('  if ( part )\n')
    _aracLineList.append('    {\n')
    _aracLineList.append('      // Here, you have to make the translation from the ATLAS EDM object to the variables of simple type\n')
    _aracLineList.append('      return m_rootTool->accept( /*Here, you need to put your translation from the ATLAS EDM to the doubles*/ );\n')
    _aracLineList.append('    }\n')
    _aracLineList.append('  else\n')
    _aracLineList.append('    {\n')
    _aracLineList.append('      return m_acceptDummy;\n')
    _aracLineList.append('    }\n')
    _aracLineList.append('}\n')
    _aracLineList.append('\n')

    # Create a file object: in "write" mode
    _aracFile = open( "ARA%s.cxx" % _selectorName,"w")

    # Write all the lines at once:
    _aracFile.writelines(_aracLineList)
    _aracFile.close()

    print "Created src/ARA%s.cxx (editing required!)" % _selectorName
    return



def CreateARASelectorHeaderFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _arahLineList = []
    _arahLineList.append('// Dear emacs, this is -*-c++-*-\n')
    _arahLineList.append('\n')
    _arahLineList.append('#ifndef __ARA%s__\n' % _selectorName.upper() )
    _arahLineList.append('#define __ARA%s__\n' % _selectorName.upper() )
    _arahLineList.append('\n')
    _arahLineList.append('/**\n')
    _arahLineList.append('   @class ARA%s\n' % _selectorName )
    _arahLineList.append('   @brief Tool to select objects in AthenaRootAccess using an underlying pure ROOT tool.\n')
    _arahLineList.append('\n')
    _arahLineList.append('   @author Karsten Koeneke (CERN)\n')
    _arahLineList.append('   @date   April 2011\n')
    _arahLineList.append('\n')
    _arahLineList.append('*/\n')
    _arahLineList.append('\n')
    _arahLineList.append('\n')
    _arahLineList.append('// Include the return object and the underlying ROOT tool\n')
    _arahLineList.append('#include "ObjectSelectorCore/TAccept.h"\n')
    _arahLineList.append('#include "%s/T%s.h"\n' % ( _packageName, _selectorName ) )
    _arahLineList.append('\n')
    _arahLineList.append('// Include the base class\n')
    _arahLineList.append('#include "ObjectSelectorCore/ARASelectorToolBase.h"\n')
    _arahLineList.append('\n')
    _arahLineList.append('// Atlas includes\n')
    _arahLineList.append('#include "AraTool/AraToolBase.h"\n')
    _arahLineList.append('#include "EventKernel/INavigable4Momentum.h"\n')
    _arahLineList.append('\n')
    _arahLineList.append('\n')
    _arahLineList.append('static const InterfaceID IID_ARA%s("ARA%s", 1, 0);\n' % (_selectorName, _selectorName) )
    _arahLineList.append('\n')
    _arahLineList.append('\n')
    _arahLineList.append('class ARA%s : public ARASelectorToolBase, virtual public AraToolBase\n' % _selectorName )
    _arahLineList.append('{\n')
    _arahLineList.append('\n')
    _arahLineList.append('public:\n')
    _arahLineList.append('  /** Standard constructor */\n')
    _arahLineList.append('  ARA%s(PropertyMgr *pmgr=0);\n' % _selectorName )
    _arahLineList.append('\n')
    _arahLineList.append('  /** Standard destructor */\n')
    _arahLineList.append('  virtual ~ARA%s();\n' % _selectorName )
    _arahLineList.append('\n')
    _arahLineList.append('public:\n')
    _arahLineList.append('  /** AlgTool interface methods */\n')
    _arahLineList.append('  static const InterfaceID& interfaceID() { return IID_ARA%s; }\n' % _selectorName )
    _arahLineList.append('\n')
    _arahLineList.append('public:\n')
    _arahLineList.append('  /** Gaudi Service Interface method implementations */\n')
    _arahLineList.append('  virtual StatusCode initialize();\n')
    _arahLineList.append('\n')
    _arahLineList.append('  /** Gaudi Service Interface method implementations */\n')
    _arahLineList.append('  virtual StatusCode finalize();\n')
    _arahLineList.append('\n')
    _arahLineList.append('\n')
    _arahLineList.append('  // Main methods\n')
    _arahLineList.append('public:\n')
    _arahLineList.append('  /** The main accept method: the actual cuts are applied here */\n')
    _arahLineList.append('  const Root::TAccept& accept( const INavigable4Momentum* part );\n')
    _arahLineList.append('\n')
    _arahLineList.append('\n')
    _arahLineList.append('  // Public methods\n')
    _arahLineList.append('public:\n')
    _arahLineList.append('  /** Method to get the underlying ROOT tool */\n')
    _arahLineList.append('  inline Root::T%s* getRootTool() { return m_rootTool; };\n' % _selectorName )
    _arahLineList.append('\n')
    _arahLineList.append('\n')
    _arahLineList.append('\n')
    _arahLineList.append('  // Private member variables\n')
    _arahLineList.append('private:\n')
    _arahLineList.append('  /** Pointer to the underlying ROOT based tool */\n')
    _arahLineList.append('  Root::T%s* m_rootTool;\n' % _selectorName )
    _arahLineList.append('\n')
    _arahLineList.append('}; // End: class definition\n')
    _arahLineList.append('\n')
    _arahLineList.append('#endif\n')
    _arahLineList.append('\n')

    # Create a file object: in "write" mode
    _arahFile = open( "ARA%s.h" % _selectorName,"w")

    # Write all the lines at once:
    _arahFile.writelines(_arahLineList)
    _arahFile.close()

    print "Created %s/ARA%s.h" % ( _packageName, _selectorName )
    return





def CreateAthSelectorFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _athhLineList = []
    _athhLineList.append('// Dear emacs, this is -*-c++-*-\n')
    _athhLineList.append('\n')
    _athhLineList.append('#ifndef __ATH%s__\n' % _selectorName.upper() )
    _athhLineList.append('#define __ATH%s__\n' % _selectorName.upper() )
    _athhLineList.append('\n')
    _athhLineList.append('/**\n')
    _athhLineList.append('   @class Ath%s\n' % _selectorName )
    _athhLineList.append('   @brief Tool to select objects in Athena using an underlying ARA and pure ROOT tool.\n')
    _athhLineList.append('\n')
    _athhLineList.append('   @author Karsten Koeneke (CERN)\n')
    _athhLineList.append('   @date   April 2011\n')
    _athhLineList.append('\n')
    _athhLineList.append('*/\n')
    _athhLineList.append('\n')
    _athhLineList.append('// Include the athena/ARA dual use wrapper\n')
    _athhLineList.append('#include "AraTool/AraAlgToolWrapper.h"\n')
    _athhLineList.append('\n')
    _athhLineList.append('// Include the AthenaRootAccess tool\n')
    _athhLineList.append('#include "ARA%s.h"\n' % _selectorName )
    _athhLineList.append('\n')
    _athhLineList.append('\n')
    _athhLineList.append('class Ath%s : public  AraAlgToolWrapper< ARA%s >\n' % (_selectorName, _selectorName) )
    _athhLineList.append('{\n')
    _athhLineList.append('\n')
    _athhLineList.append('public: \n')
    _athhLineList.append('  /** Standard constructor */\n')
    _athhLineList.append('  Ath%s( const std::string& type,\n' % _selectorName )
    _athhLineList.append('                          const std::string& name,\n')
    _athhLineList.append('                          const IInterface* parent )\n')
    _athhLineList.append('    : AlgTool( type, name, parent ),\n')
    _athhLineList.append('      AraAlgToolWrapper< ARA%s > ( type, name, parent )\n' % _selectorName )
    _athhLineList.append('  {\n')
    _athhLineList.append('    AlgTool::declareInterface< ARA%s >(this);\n' % _selectorName )
    _athhLineList.append('  };\n')
    _athhLineList.append('\n')
    _athhLineList.append('}; // End: class definition\n')
    _athhLineList.append('\n')
    _athhLineList.append('\n')
    _athhLineList.append('#endif\n')
    _athhLineList.append('\n')

    # Create a file object: in "write" mode
    _athhFile = open( "Ath%s.h" % _selectorName,"w")

    # Write all the lines at once:
    _athhFile.writelines(_athhLineList)
    _athhFile.close()

    print "Created %s/Ath%s.h" % ( _packageName, _selectorName )
    return



def CreateLoadFile( _packageName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('#include "GaudiKernel/LoadFactoryEntries.h"\n')
    _lineList.append('LOAD_FACTORY_ENTRIES(%s)\n' % _packageName)

    # Create a file object: in "write" mode
    _file = open( "%s_load.cxx" % _packageName,"w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created src/components/%s_load.cxx" % _packageName
    return



def CreateEntriesFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('#include "GaudiKernel/DeclareFactoryEntries.h"\n')
    _lineList.append('\n')
    _lineList.append('#include "%s/Ath%s.h"\n' % ( _packageName, _selectorName ) )
    _lineList.append('\n')
    _lineList.append('DECLARE_TOOL_FACTORY( Ath%s )\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('DECLARE_FACTORY_ENTRIES( %s ) \n' % _packageName )
    _lineList.append('{\n')
    _lineList.append('  DECLARE_ALGTOOL( Ath%s )\n' % _selectorName )
    _lineList.append('}\n')
    _lineList.append('\n')
    _lineList.append('\n')

    # Create a file object: in "write" mode
    _file = open( "%s_entries.cxx" % _packageName,"w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created src/components/%s_entries.cxx (editing required!)" % _packageName
    return







def CreateConfiguredAthPythonFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('##=============================================================================\n')
    _lineList.append('## Name:        ConfiguredAth%ss\n' % _selectorName )
    _lineList.append('##\n')
    _lineList.append('## Author:      Karsten Koeneke (CERN)\n')
    _lineList.append('## Created:     July 2011\n')
    _lineList.append('##\n')
    _lineList.append('## Description: Apply the default configurations for the Ath%s,\n' % _selectorName )
    _lineList.append('##              but allow for overwriting them with user-defined values.\n')
    _lineList.append('##\n')
    _lineList.append('##=============================================================================\n')
    _lineList.append('\n')
    _lineList.append('# Import the needed general stuff\n')
    _lineList.append('from ObjectSelectorCore.HelperUtils import *\n')
    _lineList.append('from AthenaCommon import CfgMgr\n')
    _lineList.append('\n')
    _lineList.append('# Import the needed stuff specific to the %s\n' % _packageName )
    _lineList.append('from %s.%sConf import Ath%s\n' % ( _packageName, _packageName, _selectorName ) )
    _lineList.append('from %s.%sCutDefs import *\n' % ( _packageName, _selectorName.rsplit("Tool",1)[0] ) )
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def ConfiguredAth%s_Loose( name, **kw ):\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the Ath%s with the default Loose cuts\n' % _selectorName )
    _lineList.append('    and allow for (re-)setting of all provided cuts.\n')
    _lineList.append('    """    \n')
    _lineList.append('    # Create and instance of the tool\n')
    _lineList.append('    tool = CfgMgr.Ath%s(name, **kw)\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('    # Configure it with the standard configuration\n')
    _lineList.append('    %sConfig_Loose( tool )\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('    # Get all provided properties and overwrite the default values with them\n')
    _lineList.append('    SetToolProperties( tool, **kw )\n')
    _lineList.append('    \n')
    _lineList.append('    return tool\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def ConfiguredAth%s_Medium( name, **kw ):\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the Ath%s with the default Medium cuts\n' % _selectorName )
    _lineList.append('    and allow for (re-)setting of all provided cuts.\n')
    _lineList.append('    """    \n')
    _lineList.append('    # Create and instance of the tool\n')
    _lineList.append('    tool = CfgMgr.Ath%s(name, **kw)\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('    # Configure it with the standard configuration\n')
    _lineList.append('    %sConfig_Medium( tool )\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('    # Get all provided properties and overwrite the default values with them\n')
    _lineList.append('    SetToolProperties( tool, **kw )\n')
    _lineList.append('    \n')
    _lineList.append('    return tool\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def ConfiguredAth%s_Tight( name, **kw ):\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the Ath%s with the default Tight cuts\n' % _selectorName )
    _lineList.append('    and allow for (re-)setting of all provided cuts.\n')
    _lineList.append('    """    \n')
    _lineList.append('    # Create and instance of the tool\n')
    _lineList.append('    tool = CfgMgr.Ath%s(name, **kw)\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('    # Configure it with the standard configuration\n')
    _lineList.append('    %sConfig_Tight( tool )\n' % _selectorName )
    _lineList.append('\n')
    _lineList.append('    # Get all provided properties and overwrite the default values with them\n')
    _lineList.append('    SetToolProperties( tool, **kw )\n')
    _lineList.append('    \n')
    _lineList.append('    return tool\n')
    _lineList.append('\n')

    # Create a file object: in "write" mode
    _file = open( "ConfiguredAth%ss.py" % _selectorName,"w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created python/ConfiguredAth%ss.py (editing may be required!)" % _selectorName
    return





def CreateConfiguredARAPythonFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('##=============================================================================\n')
    _lineList.append('## Name:        ConfiguredARA%ss\n' % _selectorName )
    _lineList.append('##\n')
    _lineList.append('## Author:      Karsten Koeneke (CERN)\n')
    _lineList.append('## Created:     July 2011\n')
    _lineList.append('##\n')
    _lineList.append('## Description: Apply the default configurations for the ARA%s.\n' % _selectorName )
    _lineList.append('##\n')
    _lineList.append('## Usage: In your pyARA session:\n')
    _lineList.append('##        from %s.ConfiguredARA%ss import *\n' % ( _packageName, _selectorName ) )
    _lineList.append('##        myLoose%s = ConfiguredARA%s_Loose()\n' % ( _selectorName, _selectorName ) )
    _lineList.append('##        myLoose%s->initialize();\n' % _selectorName)
    _lineList.append('##\n')
    _lineList.append('##=============================================================================\n')
    _lineList.append('\n')
    _lineList.append('# import the needed Reflex and ROOT stuff\n')
    _lineList.append('import PyCintex\n')
    _lineList.append('PyCintex.Cintex.Enable()\n')
    _lineList.append('import ROOT\n')
    _lineList.append('\n')
    _lineList.append('# Import the needed stuff specific to the %ss\n' % ( _selectorName ) )
    _lineList.append('from %s.%sCutDefs import *\n' % ( _packageName, _selectorName.rsplit("Tool",1)[0] ) )
    _lineList.append('\n')
    _lineList.append('def ConfiguredARA%s_Loose():\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the ARA%s with the default Loose cuts\n' % _selectorName )
    _lineList.append('    """    \n')
    _lineList.append('    tool = ROOT.ARA%s()\n' % _selectorName )
    _lineList.append('    %sConfig_Loose(tool)\n' % _selectorName )
    _lineList.append('    return tool\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def ConfiguredARA%s_Medium():\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the ARA%s with the default Medium cuts\n' % _selectorName )
    _lineList.append('    """    \n')
    _lineList.append('    tool = ROOT.ARA%s()\n' % _selectorName )
    _lineList.append('    %sConfig_Medium(tool)\n' % _selectorName )
    _lineList.append('    return tool\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def ConfiguredARA%s_Tight():\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the ARA%s with the default Tight cuts\n' % _selectorName )
    _lineList.append('    """    \n')
    _lineList.append('    tool = ROOT.ARA%s()\n' % _selectorName )
    _lineList.append('    %sConfig_Tight(tool)\n' % _selectorName )
    _lineList.append('    return tool\n')

    # Create a file object: in "write" mode
    _file = open( "ConfiguredARA%ss.py" % _selectorName,"w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created python/ConfiguredARA%ss.py (editing may be required!)" % _selectorName
    return





def CreateConfiguredTPythonFile( _packageName, _selectorName ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('##=============================================================================\n')
    _lineList.append('## Name:        ConfiguredT%ss\n' % _selectorName )
    _lineList.append('##\n')
    _lineList.append('## Author:      Karsten Koeneke (CERN)\n')
    _lineList.append('## Created:     July 2011\n')
    _lineList.append('##\n')
    _lineList.append('## Description: Apply the default configurations for the T%s.\n' % _selectorName )
    _lineList.append('##\n')
    _lineList.append('## Usage: In your ROOT session (after loading the libraries from RootCore):\n')
    _lineList.append('##        TPython::LoadMacro("./path/to/this/file/ConfiguredT%ss.py");\n' % _selectorName )
    _lineList.append('##        Root::T%s* myLooseTool = (void*)TPython::Eval("ConfiguredT%s_Loose()");\n' % ( _selectorName, _selectorName ) )
    _lineList.append('##        myLooseTool->initialize();\n')
    _lineList.append('##\n')
    _lineList.append('##=============================================================================\n')
    _lineList.append('\n')
    _lineList.append('# import the needed Reflex and ROOT stuff\n')
    _lineList.append('import PyCintex\n')
    _lineList.append('PyCintex.Cintex.Enable()\n')
    _lineList.append('import ROOT\n')
    _lineList.append('\n')
    _lineList.append('# Import the needed stuff specific to the %s\n' % _selectorName )
    _lineList.append('from %s.%sCutDefs import *\n' % ( _packageName, _selectorName.rsplit("Tool",1)[0] ) )
    _lineList.append('\n')
    _lineList.append('def ConfiguredT%s_Loose():\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the T%s with the default Loose cuts\n' % _selectorName )
    _lineList.append('    """    \n')
    _lineList.append('    tool = ROOT.Root.T%s()\n' % _selectorName )
    _lineList.append('    %sConfig_Loose(tool)\n' % _selectorName )
    _lineList.append('    return tool\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def ConfiguredT%s_Medium():\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the T%s with the default Medium cuts\n' % _selectorName )
    _lineList.append('    """    \n')
    _lineList.append('    tool = ROOT.Root.T%s()\n' % _selectorName )
    _lineList.append('    %sConfig_Medium(tool)\n' % _selectorName )
    _lineList.append('    return tool\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def ConfiguredT%s_Tight():\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    Configure the T%s with the default Tight cuts\n' % _selectorName )
    _lineList.append('    """    \n')
    _lineList.append('    tool = ROOT.Root.T%s()\n' % _selectorName )
    _lineList.append('    %sConfig_Tight(tool)\n' % _selectorName )
    _lineList.append('    return tool\n')

    # Create a file object: in "write" mode
    _file = open( "ConfiguredT%ss.py" % _selectorName,"w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()

    print "Created python/ConfiguredT%ss.py (editing may be required!)" % _selectorName
    return




def CreateCutDefsPythonFile( _packageName, _selectorName, _doubleCutNameList ) :
    # Create the lines to write to the file
    _lineList = []
    _lineList.append('##=============================================================================\n')
    _lineList.append('## Name:        %sCutDefs\n'% _selectorName.rsplit("Tool",1)[0] )
    _lineList.append('##\n')
    _lineList.append('## Author:      Karsten Koeneke (CERN)\n')
    _lineList.append('## Created:     July 2011\n')
    _lineList.append('##\n')
    _lineList.append('## Description: Define the cut values for the %ss\n' % _selectorName )
    _lineList.append('##\n')
    _lineList.append('##=============================================================================\n')
    _lineList.append('\n')
    _lineList.append('# import the needed Reflex and ROOT stuff\n')
    _lineList.append('import PyCintex\n')
    _lineList.append('PyCintex.Cintex.Enable()\n')
    _lineList.append('import ROOT\n')
    _lineList.append('\n')
    _lineList.append('# Import a needed helper\n')
    _lineList.append('from ObjectSelectorCore.HelperUtils import *\n')
    _lineList.append('\n')
    _lineList.append('# Define GeV\n')
    _lineList.append('GeV = 1000.0\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def %sConfig_Loose(theTool) :\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    This defines the cut values for the Loose operating point.\n')
    _lineList.append('    """\n')
    _lineList.append('    theTool = GetTool(theTool)\n')
    for doubleCutName in _doubleCutNameList:
        _lineList.append('    theTool.%s = \n' % doubleCutName )
        pass
    _lineList.append('    pass\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def %sConfig_Medium(theTool) :\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    This defines the cut values for the Medium operating point.\n')
    _lineList.append('    """\n')
    _lineList.append('    theTool = GetTool(theTool)\n')
    for doubleCutName in _doubleCutNameList:
        _lineList.append('    theTool.%s = \n' % doubleCutName )
        pass
    _lineList.append('    pass\n')
    _lineList.append('\n')
    _lineList.append('\n')
    _lineList.append('def %sConfig_Tight(theTool) :\n' % _selectorName )
    _lineList.append('    """\n')
    _lineList.append('    This defines the cut values for the Tight operating point.\n')
    _lineList.append('    """\n')
    _lineList.append('    theTool = GetTool(theTool)\n')
    for doubleCutName in _doubleCutNameList:
        _lineList.append('    theTool.%s = \n' % doubleCutName )
        pass
    _lineList.append('    pass\n')
    _lineList.append('\n')

    # Create a file object: in "write" mode
    _file = open( "%sCutDefs.py" % _selectorName.rsplit("Tool",1)[0],"w")

    # Write all the lines at once:
    _file.writelines(_lineList)
    _file.close()
    print "Created python/%sCutDefs.py (editing required!)" % _selectorName.rsplit("Tool",1)[0]
    return





if __name__ == "__main__":
    # Get the command line arguments, if given
    usage = "usage: %prog [options] SelectorName"
    parser = OptionParser(usage=usage)
    parser.add_option('--packageName', dest='PackageName',
                      help="Set the name of your current package where your new selector should go")
    parser.add_option('--doubleCutNameList', dest='DoubleCutNameList',
                      help='Give a comma-seperated list of cut value names. Each one HAST TO end in either "Min" or "Max" (default=[])')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect number of arguments")
        exit(0)
        pass
    CreateNewSelectorSkeleton(options)
    pass
