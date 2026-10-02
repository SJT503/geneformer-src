# ruff: noqa: F401
# VENDORED 2026-10-02 (SJT503): guarded per-module imports for constrained runtimes (Kaggle).
# Upstream __init__ eagerly imports all submodules, dragging anndata/loompy/scanpy/bitsandbytes
# whose pip resolution breaks precompiled numpy/scipy ABIs on Kaggle images. Missing modules are
# skipped with a warning; import the specific submodule you need instead.
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")  # noqa # isort:skip

GENE_MEDIAN_FILE = Path(__file__).parent / "gene_median_dictionary_gc104M.pkl"
TOKEN_DICTIONARY_FILE = Path(__file__).parent / "token_dictionary_gc104M.pkl"
ENSEMBL_DICTIONARY_FILE = Path(__file__).parent / "gene_name_id_dict_gc104M.pkl"
ENSEMBL_MAPPING_FILE = Path(__file__).parent / "ensembl_mapping_dict_gc104M.pkl"

GENE_MEDIAN_FILE_30M = Path(__file__).parent / "gene_dictionaries_30m/gene_median_dictionary_gc30M.pkl"
TOKEN_DICTIONARY_FILE_30M = Path(__file__).parent / "gene_dictionaries_30m/token_dictionary_gc30M.pkl"
ENSEMBL_DICTIONARY_FILE_30M = Path(__file__).parent / "gene_dictionaries_30m/gene_name_id_dict_gc30M.pkl"
ENSEMBL_MAPPING_FILE_30M = Path(__file__).parent / "gene_dictionaries_30m/ensembl_mapping_dict_gc30M.pkl"


def _guard(mod_name, names):
    try:
        m = __import__(f"geneformer.{mod_name}", fromlist=list(names))
        globals()[mod_name] = m
        for n in names:
            globals()[n] = getattr(m, n)
        return True
    except Exception as e:  # noqa: BLE001 — vendored guard for optional heavy deps
        warnings.warn(f"[geneformer-vendored] submodule '{mod_name}' not loaded: {e}")
        return False


_guard("collator_for_classification", ["DataCollatorForCellClassification", "DataCollatorForGeneClassification"])
_guard("emb_extractor", ["EmbExtractor", "get_embs"])
_guard("in_silico_perturber", ["InSilicoPerturber"])
_guard("in_silico_perturber_stats", ["InSilicoPerturberStats"])
_guard("pretrainer", ["GeneformerPretrainer"])
_guard("tokenizer", ["TranscriptomeTokenizer"])
_guard("classifier", ["Classifier"])
_guard("mtl_classifier", ["MTLClassifier"])
