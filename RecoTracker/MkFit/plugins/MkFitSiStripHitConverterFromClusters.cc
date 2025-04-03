#include "FWCore/Framework/interface/global/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/SiStripCluster/interface/SiStripClusterTools.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit2DCollection.h"

#include "Geometry/Records/interface/TrackerTopologyRcd.h"

#include "TrackingTools/Records/interface/TransientRecHitRecord.h"

#include "RecoTracker/MkFit/interface/MkFitHitWrapper.h"
#include "RecoTracker/MkFit/interface/MkFitClusterIndexToHit.h"
#include "RecoTracker/MkFit/interface/MkFitGeometry.h"
#include "RecoTracker/Record/interface/TrackerRecoGeometryRecord.h"

#include "convertClusters.h"

namespace {
  class ConvertHitTraits {
  public:
    ConvertHitTraits(float minCharge) : minGoodStripCharge_(minCharge) {}
    using Clusters = edmNew::DetSetVector<SiStripCluster>;
    using Cluster = Clusters::data_type;

    static constexpr bool applyCCC() { return true; }
    static float chargeScale(DetId id) { return siStripClusterTools::sensorThicknessInverse(id); }
    static const Cluster& cluster(const Clusters& prod, unsigned int index) { return prod.data()[index]; }
    static float clusterCharge(const Cluster& clu, float scale) { return clu.charge() * scale; }
    bool passCCC(float charge) const { return charge > minGoodStripCharge_; }
    static void setDetails(mkfit::Hit& mhit, const Cluster& clu, int shortId, float charge) {
      mhit.setupAsStrip(shortId, charge, clu.size());
    }

  private:
    const float minGoodStripCharge_;
  };
}  // namespace

class MkFitSiStripHitConverterFromClusters : public edm::global::EDProducer<> {
public:
  explicit MkFitSiStripHitConverterFromClusters(edm::ParameterSet const& iConfig);
  ~MkFitSiStripHitConverterFromClusters() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const override;

  const edm::EDGetTokenT<edmNew::DetSetVector<SiStripCluster>> stripClusterToken_;
  const edm::ESGetToken<TransientTrackingRecHitBuilder, TransientRecHitRecord> ttrhBuilderToken_;
  const edm::ESGetToken<TrackerTopology, TrackerTopologyRcd> ttopoToken_;
  const edm::ESGetToken<MkFitGeometry, TrackerRecoGeometryRecord> mkFitGeomToken_;
  const edm::ESGetToken<TrackerGeometry, TrackerDigiGeometryRecord> trackerToken_;
  const edm::ESGetToken<StripClusterParameterEstimator, TkStripCPERecord> cpeToken_;
  const edm::EDPutTokenT<MkFitHitWrapper> wrapperPutToken_;
  const edm::EDPutTokenT<SiStripRecHit2DCollection> recHitPutToken_;
  const edm::EDPutTokenT<MkFitClusterIndexToHit> clusterIndexPutToken_;
  const edm::EDPutTokenT<std::vector<int>> layerIndexPutToken_;
  const edm::EDPutTokenT<std::vector<float>> clusterChargePutToken_;
  const ConvertHitTraits convertTraits_;
};

MkFitSiStripHitConverterFromClusters::MkFitSiStripHitConverterFromClusters(edm::ParameterSet const& iConfig)
    : stripClusterToken_{consumes(iConfig.getParameter<edm::InputTag>("clusters"))},
      ttrhBuilderToken_{esConsumes(iConfig.getParameter<edm::ESInputTag>("ttrhBuilder"))},
      ttopoToken_{esConsumes()},
      mkFitGeomToken_{esConsumes()},
      trackerToken_{esConsumes()},
      cpeToken_{esConsumes(iConfig.getParameter<edm::ESInputTag>("StripCPE"))},
      wrapperPutToken_{produces()},
      recHitPutToken_{produces()},
      clusterIndexPutToken_{produces()},
      layerIndexPutToken_{produces()},
      clusterChargePutToken_{produces()},
      convertTraits_{static_cast<float>(
          iConfig.getParameter<edm::ParameterSet>("minGoodStripCharge").getParameter<double>("value"))} {}

void MkFitSiStripHitConverterFromClusters::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;

  desc.add("clusters", edm::InputTag{"siStripClusters"});
  desc.add("ttrhBuilder", edm::ESInputTag{"", "WithTrackAngle"});
  desc.add("StripCPE", edm::ESInputTag{"hltESPStripCPEfromTrackAngle", "hltESPStripCPEfromTrackAngle"});

  edm::ParameterSetDescription descCCC;
  descCCC.add<double>("value");
  desc.add("minGoodStripCharge", descCCC);

  descriptions.add("mkFitSiStripHitConverterFromClustersDefault", desc);
}

void MkFitSiStripHitConverterFromClusters::produce(edm::StreamID iID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  const auto& ttrhBuilder = iSetup.getData(ttrhBuilderToken_);
  const auto& ttopo = iSetup.getData(ttopoToken_);
  const auto& mkFitGeom = iSetup.getData(mkFitGeomToken_);

  const auto& tracker = iSetup.getData(trackerToken_);
  const auto& parameterestimator = iSetup.getData(cpeToken_);

  MkFitHitWrapper hitWrapper;
  SiStripRecHit2DCollection stripRecHits;
  MkFitClusterIndexToHit clusterIndexToHit;
  std::vector<int> layerIndexToHit;
  std::vector<float> clusterCharge;

  auto clusterH = iEvent.getHandle(stripClusterToken_);
  auto const& clusters = *clusterH;
  const auto maxSizeGuess(clusters.dataSize());

  mkfit::convertClusters(convertTraits_,
                        clusterH,
                        hitWrapper.hits(),
                        stripRecHits,
                        clusterIndexToHit.hits(),
                        layerIndexToHit,
                        clusterCharge,
                        ttopo,
                        ttrhBuilder,
                        mkFitGeom,
                        tracker,
                        parameterestimator,
                        maxSizeGuess);

  hitWrapper.setClustersID(clusterH.id());

  iEvent.emplace(wrapperPutToken_, std::move(hitWrapper));
  iEvent.emplace(recHitPutToken_, std::move(stripRecHits));
  iEvent.emplace(clusterIndexPutToken_, std::move(clusterIndexToHit));
  iEvent.emplace(layerIndexPutToken_, std::move(layerIndexToHit));
  iEvent.emplace(clusterChargePutToken_, std::move(clusterCharge));
}

DEFINE_FWK_MODULE(MkFitSiStripHitConverterFromClusters);
