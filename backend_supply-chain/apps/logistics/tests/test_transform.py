
import pandas as pd
import pytest
from pathlib import Path
from apps.logistics.etl.extract import extract
from apps.logistics.etl.transform import transform

SAMPLE = Path(__file__).resolve().parents[4] / "data" / "samples" / "mini.csv"

@pytest.fixture(scope="module")
def result():
    return transform(extract(SAMPLE))

def test_une_ligne_par_commande(result):
    orders, _, _ = result
    assert orders["order_id"].is_unique
    
def test_les_lignes_invalides_sont_rejetees_avec_motif(result):
    _, rejects, stats = result
    assert stats["rows_rejected"] == len(rejects) >= 1
    assert rejects["motif"].str.len().min() > 0
    
def test_ecart_et_retard_coherents(result):
    orders, _, stats = result
    assert (orders["ecart_jours"] == orders["delai_reel"] - orders["delai_prevu"]).all()
    assert stats["incoherences_retard"] == 0
    
def test_cout_estime_positif(result):
    orders, _, _ = result
    assert (orders["cout_estime"] > 0).all()
    
@pytest.mark.django_db
def test_chargement_idempotent(result):
    from apps.logistics.etl.load import load
    from apps.logistics.models import Commande, Expedition
    orders, _, _ = result
    load(orders)
    n1 = (Commande.objects.count(), Expedition.objects.count())
    load(orders)
    assert (Commande.objects.count(), Expedition.objects.count()) == n1
