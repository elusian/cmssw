#ifndef RecoTracker_MkFit_plugins_convertHits_h
#define RecoTracker_MkFit_plugins_convertHits_h

#include "DataFormats/Provenance/interface/ProductID.h"

#include "FWCore/Utilities/interface/Likely.h"

#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "DataFormats/TrackerCommon/interface/TrackerDetSide.h"

#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit2DCollection.h"

#include "TrackingTools/TransientTrackingRecHit/interface/TransientTrackingRecHitBuilder.h"

#include "RecoTracker/MkFit/interface/MkFitGeometry.h"

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"

#include "RecoLocalTracker/ClusterParameterEstimator/interface/StripClusterParameterEstimator.h"

// ROOT
#include "Math/SVector.h"
#include "Math/SMatrix.h"

// mkFit includes
#include "RecoTracker/MkFitCore/interface/Hit.h"
#include "RecoTracker/MkFitCore/interface/HitStructures.h"

namespace mkfit {
  template <typename Traits, typename ClusterCollection>
  void convertClusters(const Traits& traits,
                      const edm::Handle<ClusterCollection>& clusterH,
                      mkfit::HitVec& mkFitHits,
                      SiStripRecHit2DCollection& stripRecHits,
                      std::vector<TrackingRecHit const*>& clusterIndexToHit,
                      std::vector<int>& layerIndexToHit,
                      std::vector<float>& clusterChargeVec,
                      const TrackerTopology& ttopo,
                      const TransientTrackingRecHitBuilder& ttrhBuilder,
                      const MkFitGeometry& mkFitGeom,
                      const TrackerGeometry& tracker,
                      const StripClusterParameterEstimator& parameterestimator,
                      std::size_t maxSizeGuess = 0) {

    const auto& clusters = *clusterH;
    auto const inputID = clusterH.id();
    auto const size = std::max((std::size_t)clusters.dataSize(), maxSizeGuess);
    if (mkFitHits.size() < size) {
      mkFitHits.resize(size);
      clusterIndexToHit.resize(size, nullptr);
      layerIndexToHit.resize(size, -1);
      if constexpr (Traits::applyCCC()) {
        clusterChargeVec.resize(size, -1.f);
      }
    }
    stripRecHits.reserve(clusters.size(), size);


    int clusterIndex = 0;

    for (auto const& clusterDS : clusters) {
      const DetId detid = clusterDS.detId();

      GeomDetUnit const& du = *(tracker.idToDetUnit(detid.rawId()));
      if (not dynamic_cast<const StripGeomDetUnit*>(&du))
        continue;

      const auto ilay = mkFitGeom.mkFitLayerNumber(detid);
      const auto uniqueIdInLayer = mkFitGeom.uniqueIdInLayer(ilay, detid.rawId());
      const auto chargeScale = traits.chargeScale(detid);
      const auto& surf = du.surface();

      SiStripRecHit2DCollection::FastFiller recHitFiller(stripRecHits, detid);

      for (auto const& cluster : clusterDS) {

        StripClusterParameterEstimator::LocalValues parameters = parameterestimator.localParameters(cluster, du);
        recHitFiller.push_back(SiStripRecHit2D(parameters.first, parameters.second, du, OmniClusterRef(inputID, &cluster, clusterDS.makeKeyOf(&cluster))));

        const auto charge = traits.clusterCharge(cluster, chargeScale);

        if (!traits.passCCC(charge))
          continue;

        const auto& gpos = surf.toGlobal(parameters.first);
        SVector3 pos(gpos.x(), gpos.y(), gpos.z());
        const auto& gerr = ErrorFrameTransformer::transform(parameters.second, surf);
        SMatrixSym33 err{{float(gerr.cxx()),
          float(gerr.cyx()),
          float(gerr.cyy()),
          float(gerr.czx()),
          float(gerr.czy()),
          float(gerr.czz())}};

        // LogTrace("MkFitHitConverter") << "Adding hit detid " << detid.rawId() << " subdet " << detid.subdetId()
        // << " layer " << ttopo.layer(detid) << " isStereo " << ttopo.isStereo(detid)
        // << " zplus "
        // << " index " << clusterIndex << " ilay " << ilay;

        mkFitHits[clusterIndex] = mkfit::Hit(pos, err);
        clusterIndexToHit[clusterIndex] = &recHitFiller.back();
        layerIndexToHit[clusterIndex] = ilay;
        if constexpr (Traits::applyCCC()) {
          clusterChargeVec[clusterIndex] = charge;
        }

        traits.setDetails(mkFitHits[clusterIndex], cluster, uniqueIdInLayer, charge);

        clusterIndex += 1;

      }
    }
  }
}  // namespace mkfit

#endif
