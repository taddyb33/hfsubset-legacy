from pathlib import Path
from typing import Annotated, List

from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import Response
import rpy2.robjects as robjects
from rpy2.robjects.vectors import StrVector

from src.hfsubset.app.schemas import Subset
from src.hfsubset.app.core import get_settings
from src.hfsubset.app.core.settings import Settings
from src.hfsubset.app.core.utils import find_repo_root

router = APIRouter()

r = robjects.r
r('source("/app/subset_network.R")')


@router.get("/", response_model=Subset)
async def generate_hf_subset(
    settings: Annotated[Settings, Depends(get_settings)],
    feature_id: int = Query(..., description="The COMID for the subset"),
    lyrs: List[str] = Query(["divides", "nexus", "flowpaths", "lakes", "flowpath_attributes", "network", "layer_styles"], description="The layers to include in the subset"),
):

    subset_network = r['subset_network']
    output_path = settings.subset_output_path
    subset_file = output_path / f"{feature_id}/subset.gpkg"
    base_dir: str = "gpkg/"    

    if subset_file.exists():
        return Subset(
                status=200,
                message="Subset pulled from cache",
                feature_id=feature_id,
                layers=lyrs,
                output_file=subset_file.__str__()
            )
    else:
        print(subset_file.parent)
        subset_file.parent.mkdir(exist_ok=True)
        try:
            # Call the R function
            _ = subset_network(
                comid=feature_id,
                lyrs=StrVector(lyrs),
                base_dir=base_dir,
                outfile=subset_file.__str__()
            )
            
            # The R function might not return anything if it's just writing to a file
            # In this case, we'll just return a success message
            return Subset(
                status=200,
                message="Subset created successfully",
                feature_id=feature_id,
                layers=lyrs,
                output_file=subset_file.__str__()
            )
        except Exception as e:
            # TODO make this specific
            print(e)
            return {"error": str(e)}