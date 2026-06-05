"""Tests for country presets, data loaders, and constituency management."""

import tempfile

import numpy as np
import polars as pl
import pytest

# =============================================================================
# PRESET LOADING
# =============================================================================


class TestAllPresets:
    """All preset configs loadable and runnable."""

    def test_all_presets_loadable(self):
        from electoral_sim import PRESETS

        for name, factory in PRESETS.items():
            config = factory()
            assert config is not None, f"Preset {name} failed to load"

    @pytest.mark.parametrize(
        "preset",
        [
            "india",
            "usa",
            "uk",
            "germany",
            "france",
            "australia_house",
            "brazil",
            "japan",
            "south_africa",
            "canada",
            "eu",
            "israel",
            "netherlands",
            "switzerland",
            "mexico",
            "nz",
            "ireland",
            "scotland",
            "wales",
            "chile",
            "spain",
            "norway",
            "sweden",
        ],
    )
    def test_all_presets_run(self, preset):
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset(preset, n_voters=5000)
        results = model.run_election()
        assert results is not None
        assert "seats" in results
        assert "turnout" in results

    def test_usa_preset_structure(self):
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("usa", n_voters=5000)
        assert model.electoral_system == "FPTP"
        assert model.parties.n_parties == 2

    def test_germany_preset_structure(self):
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("germany", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.threshold == 0.05
        assert model.parties.n_parties == 6

    def test_india_preset_structure(self):
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("india", n_voters=5000)
        assert model.electoral_system == "FPTP"

    def test_uk_preset_structure(self):
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("uk", n_voters=5000)
        assert model.electoral_system == "FPTP"
        assert model.parties.n_parties == 5

    def test_australia_house_uses_fptp(self):
        """Australia House preset uses FPTP (IRV not yet wired into model)."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("australia_house", n_voters=5000)
        assert model.electoral_system == "FPTP"

    def test_australia_senate_uses_pr(self):
        """Australia Senate preset uses PR (STV not yet wired into model)."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("australia_senate", n_voters=5000)
        assert model.electoral_system == "PR"

    def test_eu_preset_structure(self):
        """EU preset structure test."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("eu", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.allocation_method == "dhondt"
        assert model.parties.n_parties == 8

    def test_canada_preset_structure(self):
        """Canada preset uses FPTP with 338 ridings."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("canada", n_voters=5000)
        assert model.electoral_system == "FPTP"
        assert model.parties.n_parties == 5

    def test_israel_preset_structure(self):
        """Israel preset uses nationwide PR with 3.25% threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("israel", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.threshold == 0.0325
        assert model.parties.n_parties == 6

    def test_netherlands_preset_structure(self):
        """Netherlands preset uses nationwide PR with 0.67% threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("netherlands", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.threshold == 0.0067
        assert model.parties.n_parties == 8

    def test_switzerland_preset_structure(self):
        """Switzerland preset uses PR with 26 cantons."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("switzerland", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.parties.n_parties == 5

    def test_mexico_preset_structure(self):
        """Mexico preset uses FPTP with 300 districts."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("mexico", n_voters=5000)
        assert model.electoral_system == "FPTP"
        assert model.parties.n_parties == 6

    def test_nz_preset_structure(self):
        """NZ preset uses MMP (FPTP base) with 5% threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("nz", n_voters=5000)
        assert model.electoral_system == "FPTP"
        assert model.threshold == 0.05
        assert model.parties.n_parties == 6

    def test_ireland_preset_structure(self):
        """Ireland preset uses PR with 39 multi-member constituencies."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("ireland", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.parties.n_parties == 6

    def test_scotland_preset_structure(self):
        """Scotland preset uses FPTP with 5 parties."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("scotland", n_voters=5000)
        assert model.electoral_system == "FPTP"
        assert model.parties.n_parties == 5

    def test_wales_preset_structure(self):
        """Wales preset uses FPTP with 4 parties."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("wales", n_voters=5000)
        assert model.electoral_system == "FPTP"
        assert model.parties.n_parties == 4

    def test_chile_preset_structure(self):
        """Chile preset uses D'Hondt PR with 6 parties."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("chile", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.parties.n_parties == 6

    def test_spain_preset_structure(self):
        """Spain preset uses D'Hondt PR with 3% threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("spain", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.threshold == 0.03
        assert model.parties.n_parties == 6

    def test_norway_preset_structure(self):
        """Norway preset uses Sainte-Lague PR with 4% threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("norway", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.threshold == 0.04
        assert model.allocation_method == "sainte_lague"
        assert model.parties.n_parties == 7

    def test_sweden_preset_structure(self):
        """Sweden preset uses Sainte-Lague PR with 4% threshold."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("sweden", n_voters=5000)
        assert model.electoral_system == "PR"
        assert model.threshold == 0.04
        assert model.allocation_method == "sainte_lague"
        assert model.parties.n_parties == 7

    def test_preset_provenance_metadata(self):
        """from_preset() stores provenance metadata on the model."""
        from electoral_sim import ElectionModel

        model = ElectionModel.from_preset("usa", n_voters=500)
        assert hasattr(model, "_provenance")
        assert model._provenance["calibration"] == "structural_demo"
        assert model._provenance["electoral_system"] == "FPTP"

    def test_preset_provenance_for_all(self):
        """All presets have provenance metadata."""
        from electoral_sim import ElectionModel, PRESETS

        from electoral_sim.core.config import PRESET_PROVENANCE

        for preset_name in PRESETS:
            assert preset_name in PRESET_PROVENANCE, f"Missing provenance for {preset_name}"
            prov = PRESET_PROVENANCE[preset_name]
            assert "calibration" in prov


# =============================================================================
# INDIA PRESET
# =============================================================================


class TestIndiaPreset:
    """India-specific preset tests."""

    def test_india_states_import(self):
        from electoral_sim.presets.india.election import INDIA_STATES

        assert len(INDIA_STATES) > 30
        assert sum(INDIA_STATES.values()) == 543

    def test_india_parties_import(self):
        from electoral_sim.presets.india.election import INDIA_PARTIES

        assert len(INDIA_PARTIES) > 10
        assert "BJP" in INDIA_PARTIES
        assert "INC" in INDIA_PARTIES

    def test_simulate_india_election(self):
        from electoral_sim import simulate_india_election

        result = simulate_india_election(n_voters_per_constituency=500, seed=42, verbose=False)
        assert result is not None
        assert sum(result.seats.values()) <= 543
        assert 0 < result.turnout <= 1.0

    def test_india_election_result_class(self):
        from electoral_sim import simulate_india_election

        result = simulate_india_election(n_voters_per_constituency=500, seed=42, verbose=False)
        result_str = str(result)
        assert "INDIA GENERAL ELECTION" in result_str

    def test_india_with_nota(self):
        from electoral_sim import simulate_india_election

        result = simulate_india_election(
            n_voters_per_constituency=500, seed=42, verbose=False, include_nota=True
        )
        assert result is not None
        assert result.nota_contested_seats >= 0

    def test_india_verbose(self):
        """India simulation with verbose=True prints output."""
        from electoral_sim import simulate_india_election

        result = simulate_india_election(n_voters_per_constituency=200, seed=42, verbose=True)
        assert result is not None

    def test_phase_states_total_seats(self):
        from electoral_sim.presets.india.election import get_phase_states, INDIA_STATES

        phases = get_phase_states()
        unique_states_in_phases = set()
        for states in phases.values():
            unique_states_in_phases.update(states)
        assert len(unique_states_in_phases) > 0


# =============================================================================
# EU PRESET
# =============================================================================


class TestEUPreset:
    """EU Parliament preset tests."""

    def test_eu_member_states(self):
        from electoral_sim import EU_MEMBER_STATES

        assert len(EU_MEMBER_STATES) == 27
        assert sum(EU_MEMBER_STATES.values()) == 720

    def test_eu_political_groups(self):
        from electoral_sim import EU_POLITICAL_GROUPS

        assert len(EU_POLITICAL_GROUPS) >= 7

    def test_eu_simulation(self):
        from electoral_sim import simulate_eu_election

        result = simulate_eu_election(n_voters_per_mep=500, seed=42, verbose=False)
        assert result is not None

    def test_eu_result_str(self):
        """EUElectionResult __str__ produces readable output."""
        from electoral_sim import simulate_eu_election

        result = simulate_eu_election(n_voters_per_mep=200, seed=42, verbose=False)
        result_str = str(result)
        assert "EUROPEAN PARLIAMENT" in result_str
        assert "Turnout" in result_str
        assert "Pro-EU" in result_str

    def test_eu_verbose(self):
        """EU simulation with verbose=True prints output."""
        from electoral_sim import simulate_eu_election

        result = simulate_eu_election(n_voters_per_mep=200, seed=42, verbose=True)
        assert result is not None


# =============================================================================
# CONSTITUENCY MANAGEMENT
# =============================================================================


class TestConstituencyManager:
    """ConstituencyManager from metadata list and DataFrame."""

    def test_from_metadata_list(self):
        from electoral_sim.core.constituency import ConstituencyManager, ConstituencyMetadata

        metadata = [
            ConstituencyMetadata(id=0, name="Varanasi", state="Uttar Pradesh"),
            ConstituencyMetadata(id=1, name="Lucknow", state="Uttar Pradesh"),
            ConstituencyMetadata(id=2, name="Mumbai South", state="Maharashtra"),
        ]
        manager = ConstituencyManager(metadata)
        assert manager.get_name(0) == "Varanasi"
        assert manager.get_state(1) == "Uttar Pradesh"

    def test_from_dataframe(self):
        from electoral_sim.core.constituency import ConstituencyManager

        df = pl.DataFrame(
            {
                "id": [0, 1, 2],
                "name": ["A", "B", "C"],
                "state": ["X", "Y", "Z"],
                "seats": [1, 1, 1],
                "type": ["General", "General", "SC"],
                "lat": [25.3, 26.8, 19.0],
                "lon": [82.9, 80.9, 72.8],
            }
        )
        manager = ConstituencyManager(df)
        assert manager.get_name(1) == "B"

    def test_get_name_unknown_id(self):
        from electoral_sim.core.constituency import ConstituencyManager, ConstituencyMetadata

        manager = ConstituencyManager([ConstituencyMetadata(id=0, name="A", state="X")])
        assert manager.get_name(99) == "District 99"

    def test_get_state_unknown_id(self):
        from electoral_sim.core.constituency import ConstituencyManager, ConstituencyMetadata

        manager = ConstituencyManager([ConstituencyMetadata(id=0, name="A", state="X")])
        assert manager.get_state(99) == "Unknown"

    def test_to_dict_list(self):
        from electoral_sim.core.constituency import ConstituencyManager, ConstituencyMetadata

        manager = ConstituencyManager([ConstituencyMetadata(id=0, name="A", state="X")])
        result = manager.to_dict_list()
        assert isinstance(result, list)
        assert result[0]["name"] == "A"


# =============================================================================
# INDIA CONSTITUENCY DATA
# =============================================================================


class TestIndiaConstituencyData:
    """India PC data loader."""

    def test_total_543(self):
        from electoral_sim.data.india_pc import get_india_constituencies

        manager = get_india_constituencies()
        assert len(manager.df) == 543

    def test_known_names_present(self):
        from electoral_sim.data.india_pc import get_india_constituencies

        names = get_india_constituencies().df["name"].to_list()
        assert "Varanasi" in names
        assert "Lucknow" in names
        assert "Mumbai South" in names

    def test_filler_names_format(self):
        from electoral_sim.data.india_pc import get_india_constituencies

        names = get_india_constituencies().df["name"].to_list()
        assert sum(1 for n in names if " PC " in n) > 0

    def test_all_states_covered(self):
        from electoral_sim.presets.india.election import INDIA_STATES
        from electoral_sim.data.india_pc import get_india_constituencies

        covered = set(get_india_constituencies().df["state"].unique().to_list())
        for state in INDIA_STATES:
            assert state in covered


# =============================================================================
# HISTORICAL DATA LOADERS
# =============================================================================


class TestHistoricalDataLoader:
    """Historical data loader tests."""

    @pytest.fixture
    def sample_csv(self):
        content = (
            "constituency,party,votes,seats,year\n"
            "North,PartyA,50000,1,2020\n"
            "North,PartyB,35000,0,2020\n"
            "South,PartyA,20000,0,2020\n"
            "South,PartyB,45000,1,2020\n"
            "East,PartyA,60000,1,2020\n"
            "East,PartyC,15000,0,2020\n"
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(content)
            return f.name

    def test_file_not_found(self):
        from electoral_sim.data.loaders import HistoricalDataLoader

        with pytest.raises(FileNotFoundError):
            HistoricalDataLoader("/nonexistent/path.csv")

    def test_viability_weights(self, sample_csv):
        from electoral_sim.data.loaders import HistoricalDataLoader

        loader = HistoricalDataLoader(sample_csv)
        weights = loader.get_viability_weights()
        assert abs(sum(weights.values()) - 1.0) < 0.001
        assert "PartyA" in weights

    def test_viability_weights_by_year(self, sample_csv):
        from electoral_sim.data.loaders import HistoricalDataLoader

        loader = HistoricalDataLoader(sample_csv)
        weights = loader.get_viability_weights(year=2020)
        assert len(weights) == 3

    def test_incumbents_from_seats(self, sample_csv):
        from electoral_sim.data.loaders import HistoricalDataLoader

        loader = HistoricalDataLoader(sample_csv)
        incumbents = loader.get_incumbents()
        assert "PartyA" in incumbents
        assert "PartyC" not in incumbents

    def test_incumbents_from_votes(self, sample_csv):
        from electoral_sim.data.loaders import HistoricalDataLoader

        loader = HistoricalDataLoader(sample_csv)
        loader.df = loader.df.drop("seats")
        incumbents = loader.get_incumbents()
        assert "PartyA" in incumbents

    def test_constituency_viability(self, sample_csv):
        from electoral_sim.data.loaders import HistoricalDataLoader

        loader = HistoricalDataLoader(sample_csv)
        viab = loader.get_constituency_viability()
        for key, party_shares in viab.items():
            assert abs(sum(party_shares.values()) - 1.0) < 0.001

    def test_constituency_viability_by_year(self, sample_csv):
        """get_constituency_viability with year filter exercises the year branch."""
        from electoral_sim.data.loaders import HistoricalDataLoader

        loader = HistoricalDataLoader(sample_csv)
        viab = loader.get_constituency_viability(year=2020)
        assert len(viab) == 3  # North, South, East

    def test_incumbents_by_year(self, sample_csv):
        """get_incumbents with year filter exercises the year-filtering branch."""
        from electoral_sim.data.loaders import HistoricalDataLoader

        loader = HistoricalDataLoader(sample_csv)
        incumbents = loader.get_incumbents(year=2020)
        assert "PartyA" in incumbents
        assert "PartyB" in incumbents


# =============================================================================
# VOTER GENERATION - PARTY FRAME WITH NOTA
# =============================================================================


class TestVoterGeneration:
    """Tests for voter_generation module edge cases."""

    def test_generate_party_frame_with_nota(self):
        """generate_party_frame with include_nota=True adds NOTA party."""
        from electoral_sim.core.voter_generation import generate_party_frame

        parties = [
            {"name": "A", "position_x": -0.3, "position_y": 0.0, "valence": 50},
            {"name": "B", "position_x": 0.3, "position_y": 0.0, "valence": 50},
        ]
        df = generate_party_frame(parties, include_nota=True)
        assert len(df) == 3
        assert "NOTA" in df["name"].to_list()
        nota_row = df.filter(pl.col("is_nota"))
        assert len(nota_row) == 1

    def test_generate_party_frame_without_nota(self):
        """generate_party_frame without NOTA."""
        from electoral_sim.core.voter_generation import generate_party_frame

        parties = [
            {"name": "A", "position_x": -0.3, "position_y": 0.0, "valence": 50},
        ]
        df = generate_party_frame(parties, include_nota=False)
        assert len(df) == 1
        assert df["is_nota"].sum() == 0

    def test_voter_frame_personality_columns(self):
        """Voter frame includes Big Five personality columns."""
        from electoral_sim.core.voter_generation import generate_voter_frame

        rng = np.random.default_rng(42)
        df = generate_voter_frame(100, 5, rng)
        for col in [
            "openness",
            "conscientiousness",
            "extraversion",
            "agreeableness",
            "neuroticism",
        ]:
            assert col in df.columns
            assert df[col].min() >= 0
            assert df[col].max() <= 1

    def test_voter_frame_moral_foundations(self):
        """Voter frame includes moral foundations columns."""
        from electoral_sim.core.voter_generation import generate_voter_frame

        rng = np.random.default_rng(42)
        df = generate_voter_frame(100, 5, rng)
        for col in ["mf_care", "mf_fairness", "mf_loyalty", "mf_authority", "mf_sanctity"]:
            assert col in df.columns


class TestDataIngestion:
    """Tests for precinct/district result ingestion pipeline."""

    def test_validate_schema_valid(self):
        """Valid schema returns no errors."""
        from electoral_sim.data.ingestion import validate_schema
        import polars as pl

        df = pl.DataFrame({"constituency": ["A"], "party": ["X"], "votes": [100]})
        errors = validate_schema(df)
        assert len(errors) == 0

    def test_validate_schema_missing_cols(self):
        """Missing required columns returns errors."""
        from electoral_sim.data.ingestion import validate_schema
        import polars as pl

        df = pl.DataFrame({"constituency": ["A"]})
        errors = validate_schema(df)
        assert any("party" in e for e in errors)
        assert any("votes" in e for e in errors)

    def test_validate_schema_empty(self):
        """Empty DataFrame returns errors."""
        from electoral_sim.data.ingestion import validate_schema
        import polars as pl

        df = pl.DataFrame({"constituency": [], "party": [], "votes": []},
                          schema={"constituency": pl.Utf8, "party": pl.Utf8, "votes": pl.Int64})
        errors = validate_schema(df)
        assert len(errors) > 0

    def test_load_precinct_results_csv(self, tmp_path):
        """CSV loading with valid schema succeeds."""
        from electoral_sim.data.ingestion import load_precinct_results

        csv_path = tmp_path / "test.csv"
        csv_path.write_text("constituency,party,votes\nA,X,100\nB,Y,200\n")
        df = load_precinct_results(str(csv_path))
        assert df.height == 2

    def test_compute_incumbents_from_seats(self):
        """compute_incumbents detects winners from seats column."""
        from electoral_sim.data.ingestion import compute_incumbents
        import polars as pl

        df = pl.DataFrame({
            "constituency": ["A", "A", "B", "B"],
            "party": ["X", "Y", "X", "Z"],
            "votes": [100, 80, 90, 60],
            "seats": [1, 0, 0, 1],
        })
        incumbents = compute_incumbents(df)
        assert "X" in incumbents
        assert "Z" in incumbents

    def test_load_geometry_geojson(self, tmp_path):
        """load_geometry loads GeoJSON files."""
        from electoral_sim.data.ingestion import load_geometry

        geojson = tmp_path / "test.geojson"
        geojson.write_text('{"type":"FeatureCollection","features":[],"crs":{"type":"name","properties":{"name":"EPSG:4326"}}}')
        result = load_geometry(str(geojson))
        assert result["crs"] == "EPSG:4326"
        assert result["n_features"] == 0


class TestPresetContracts:
    """Contract tests: every preset must expose config, metadata, provenance, and smoke."""

    def test_every_preset_has_provenance(self):
        """All PRESETS keys must have a PRESET_PROVENANCE entry."""
        from electoral_sim import PRESETS
        from electoral_sim.core.config import PRESET_PROVENANCE

        for name in PRESETS:
            assert name in PRESET_PROVENANCE, (
                f"Preset '{name}' missing from PRESET_PROVENANCE"
            )

    def test_every_preset_config_loads_and_runs(self):
        """Every preset config loads and runs a smoke simulation."""
        from electoral_sim import ElectionModel, PRESETS

        for name in PRESETS:
            model = ElectionModel.from_preset(name, n_voters=500)
            result = model.run_election()
            assert result is not None, f"Preset '{name}' returned None"
            assert "turnout" in result, f"Preset '{name}' missing turnout"
            assert result["turnout"] >= 0, f"Preset '{name}' negative turnout"

    def test_every_preset_has_expected_system(self):
        """Every preset's electoral system is valid."""
        from electoral_sim import PRESETS
        from electoral_sim.core.config import VALID_ELECTORAL_SYSTEMS

        for name, factory in PRESETS.items():
            config = factory()
            assert config.electoral_system in VALID_ELECTORAL_SYSTEMS, (
                f"Preset '{name}' has unknown system: {config.electoral_system}"
            )
