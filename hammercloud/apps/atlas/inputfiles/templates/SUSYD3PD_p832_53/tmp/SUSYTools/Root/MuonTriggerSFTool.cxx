/**
 *
 **/ 

#include "SUSYTools/MuonTriggerSFTool.h"
#include "math.h"


MuonTriggerSFTool::MuonTriggerSFTool() 
  : m_isloaded(false)
  , m_18or40(true)
  , m_verbose(false)
  , h_sf_endcap(0)
  , h_sf_barrel(0)
  , h_corr_barrel(0)
  , m_ax(0)
  , m_ay(0)
{
}


MuonTriggerSFTool::~MuonTriggerSFTool() 
{
  if ( h_sf_endcap!=0) { delete h_sf_endcap; h_sf_endcap=0; }
  if ( h_sf_barrel!=0) { delete h_sf_barrel; h_sf_barrel=0; }
  if ( h_corr_barrel!=0) { delete h_corr_barrel; h_corr_barrel=0; }

}


void MuonTriggerSFTool::initialize(std::string filename1, std::string filename2)
{
  TFile* file1 = new TFile(filename1.c_str());
  TFile* file2 = new TFile(filename2.c_str());

  h_sf_endcap   = (TH1F*)file1->Get("SF_Endcap_StacoCB_mu18MG_mu40MSonly_barrel") ;
  h_sf_endcap->SetDirectory(0);
  h_sf_barrel   = (TH2F*)file1->Get("SF_Barrel_StacoCB_mu18MG_mu40MSonly_barrel") ;
  h_sf_barrel->SetDirectory(0);
  h_corr_barrel = (TH1F*)file2->Get("SF_StacoCB_mu18MG_mu40MSonly_barrel") ;
  h_corr_barrel->SetDirectory(0);

  m_ax = h_sf_barrel->GetXaxis();
  m_ay = h_sf_barrel->GetYaxis();

  m_isloaded = true;
  
  file1->Close();
  file2->Close();
}


float
MuonTriggerSFTool::GetScaleFactor(float eta, float phi, float pt /* GeV */) 
{

  if (!m_isloaded) MuonTriggerSFTool::initialize();

  float sf  = 1.0;
  
  if (eta> -1.05 && eta < 1.05) { // barrel
    int etabin = m_ax->FindBin(eta);
    int phibin = m_ay->FindBin(phi);

    if ( etabin <= 0 ) { etabin = 1; }
    if ( phibin <= 0 ) { phibin = 1; }
    if ( etabin > h_sf_barrel->GetNbinsX() ) { etabin = h_sf_barrel->GetNbinsX(); }
    if ( phibin > h_sf_barrel->GetNbinsY() ) { phibin = h_sf_barrel->GetNbinsY(); }
    
    sf =  h_sf_barrel->GetBinContent(etabin,phibin) ;

    if (m_verbose) std::cout << "barrel: " << etabin << " " << phibin << " " << sf << std::endl;

    if ( !m_18or40 ) {
      int ptbin = h_corr_barrel->FindBin( pt*1000. );
      if (ptbin <=0 ) { ptbin = 1; }
      if (ptbin > h_corr_barrel->GetNbinsX() ) { ptbin = h_corr_barrel->GetNbinsX(); }
      float corr = h_corr_barrel->GetBinContent( ptbin );
      if (corr<=0) { corr=1.0; }

      if (m_verbose) std::cout << "barrel: " << ptbin << " " << corr << std::endl;

      sf /= corr;

      if (m_verbose) std::cout << "barrel: " << sf << std::endl;
    }

  } else { // endcap

      int ptbin = h_sf_endcap->FindBin( pt );
      if (ptbin <=0 ) { ptbin = 1; }
      if (ptbin > h_sf_endcap->GetNbinsX() ) { ptbin = h_sf_endcap->GetNbinsX(); }
      sf = h_sf_endcap->GetBinContent( ptbin );

      if (m_verbose) std::cout << "endcap: " << ptbin << " " << sf << std::endl;
  }

  if (sf<=0.0) { sf=1.0; }

  return sf;
}



