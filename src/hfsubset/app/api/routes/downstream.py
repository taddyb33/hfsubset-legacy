from pathlib import Path
from typing import Annotated, List

from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import Response
import rpy2.robjects as robjects
from rpy2.robjects.vectors import StrVector
import pandas as pd

from src.hfsubset.app.schemas import DownstreamLinks
from src.hfsubset.app.core import get_settings
from src.hfsubset.app.core.settings import Settings
from src.hfsubset.app.core.utils import find_repo_root

router = APIRouter()

r = robjects.r
r('source("/app/subset_network.R")')


@router.get("/", response_model=DownstreamLinks)
async def generate_hf_downstream(
    settings: Annotated[Settings, Depends(get_settings)],
    feature_id: int = Query(..., description="The COMID for the subset"),
    downstream_feature_id: int = Query(..., description="The downstream LID to route until"),
    lyrs: List[str] = Query(["divides", "nexus", "flowpaths", "lakes", "flowpath_attributes", "network", "layer_styles"], description="The layers to include in the subset"),
):
    subset_network = r['subset_network']
    output_path = settings.subset_output_path
    downstream_file = output_path / f"{feature_id}/downstream.gpkg"
    base_dir: str = "gpkg/"    

    if downstream_file.exists():
        return DownstreamLinks(
                status=200,
                message="Downstream geopackage retrieved from cache",
                feature_id=feature_id,
                downstream_feature_id=downstream_feature_id,
                layers=lyrs,
                output_file=downstream_file.__str__()
            )
    else:
        print(downstream_file.parent)
        downstream_file.parent.mkdir(exist_ok=True)
        try:
            # Call the R function
            _ = subset_network(
                comid=feature_id,
                lyrs=StrVector(lyrs),
                base_dir=base_dir,
                outfile=downstream_file.__str__()
            )
            return DownstreamLinks(
                status=200,
                message="Downstream geopackage created successfully",
                feature_id=feature_id,
                downstream_feature_id=feature_id,
                layers=lyrs,
                output_file=downstream_file.__str__()
            )
        except Exception as e:
            # TODO make this specific
            print(e)
            return {"error": str(e), "status": 500}
