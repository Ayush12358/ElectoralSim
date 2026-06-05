# Copyright 2025-2026 Ayush Joshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Precinct/district election result ingestion pipeline.

Provides schema validation, CSV/Parquet loading, and normalization
for MIT Election Lab-style precinct-level returns and other common
election data formats.

Expected schema columns:
    - constituency: str (district/precinct identifier)
    - party: str (party/candidate name)
    - votes: int (vote count)
    - seats: int (optional, seats won)
    - year: int (optional, election year)
"""

import polars as pl

EXPECTED_SCHEMA = {
    "constituency": pl.Utf8,
    "party": pl.Utf8,
    "votes": pl.Int64,
}


def validate_schema(df: pl.DataFrame) -> list[str]:
    """Validate that a DataFrame has the expected election result schema.

    Args:
        df: Polars DataFrame with election results

    Returns:
        List of error strings (empty if valid)
    """
    errors = []
    required = ["constituency", "party", "votes"]
    for col in required:
        if col not in df.columns:
            errors.append(f"Missing required column: '{col}'")
    if df.height == 0 and not errors:
        errors.append("DataFrame is empty")
    if not errors and df["votes"].dtype not in (pl.Int64, pl.Int32, pl.Int8):
        errors.append("Column 'votes' must be integer type")
    return errors


def load_precinct_results(path: str) -> pl.DataFrame:
    """Load precinct/district results from CSV or Parquet.

    Supports MIT Election Lab-style CSV and Parquet files.
    Validates schema after loading.

    Args:
        path: File path to CSV or Parquet

    Returns:
        Polars DataFrame with election results

    Raises:
        ValueError: If schema validation fails
    """
    if path.endswith(".parquet"):
        df = pl.read_parquet(path)
    else:
        df = pl.read_csv(path, infer_schema_length=10000)

    errors = validate_schema(df)
    if errors:
        raise ValueError(f"Schema validation failed: {'; '.join(errors)}")

    return df


def normalize_party_names(df: pl.DataFrame, mapping: dict[str, str]) -> pl.DataFrame:
    """Normalize party names using a mapping dictionary.

    Args:
        df: Election results DataFrame
        mapping: Dict mapping raw names to normalized names

    Returns:
        DataFrame with normalized party column
    """
    return df.with_columns(pl.col("party").replace_strict(mapping, default=None))


def compute_incumbents(df: pl.DataFrame, year: int | None = None) -> list[str]:
    """Compute incumbent parties from election results.

    Args:
        df: Election results DataFrame (must have 'party' and optional 'seats', 'year' col)
        year: Filter by election year (if year column present)

    Returns:
        List of party names that won seats
    """
    filtered = df
    if year is not None and "year" in df.columns:
        filtered = df.filter(pl.col("year") == year)

    if "seats" in filtered.columns:
        return filtered.filter(pl.col("seats") > 0)["party"].unique().to_list()

    # Estimate incumbents by top party per constituency
    return (
        filtered.group_by("constituency")
        .agg(pl.col("party").sort_by("votes", descending=True).first())["party"]
        .unique()
        .to_list()
    )


def load_geometry(path: str) -> "dict[str, Any]":
    """
    Load constituency geometry from GeoJSON or Shapefile.

    Keeps heavy GIS dependencies optional. Raises ImportError with
    install guidance if required libraries are missing.

    Args:
        path: File path to GeoJSON (.geojson) or Shapefile (.shp)

    Returns:
        Dict with 'type' (FeatureCollection), 'features' list,
        'crs' string, and 'n_features' count.
    """
    ext = path.lower().rsplit(".", 1)[-1] if "." in path else ""
    features = []

    if ext == "geojson":
        import json

        with open(path) as f:
            data = json.load(f)
        features = data.get("features", [])
        crs = data.get("crs", {}).get("properties", {}).get("name", "WGS84")
    elif ext == "shp":
        try:
            import shapefile
        except ImportError:
            raise ImportError("Shapefile support requires pyshp. Install with: pip install pyshp")
        with shapefile.Reader(path) as sf:
            for record in sf.shapeRecords():
                features.append(
                    {
                        "type": "Feature",
                        "geometry": record.shape.__geo_interface__,
                        "properties": dict(
                            zip(
                                [f[0] for f in sf.fields[1:]],
                                record.record,
                            )
                        ),
                    }
                )
        crs = "Unknown"
    else:
        raise ValueError(f"Unsupported geometry format: '{ext}'. Use .geojson or .shp")

    return {
        "type": "FeatureCollection",
        "features": features,
        "crs": crs,
        "n_features": len(features),
    }
