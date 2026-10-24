
from rest_framework import serializers
from apps.logistics.models import Commande, Entrepot, EtlRun, Expedition, Transporteur


class TransporteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporteur
        fields = ["id", "code", "nom"]
class EntrepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepot
        fields = ["id", "code", "nom"]
class ExpeditionSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="commande.order_id", read_only=True)
    region = serializers.CharField(source="commande.region", read_only=True)
    date_commande = serializers.DateTimeField(source="commande.date_commande", read_only=True)
    transporteur = TransporteurSerializer(read_only=True)
    entrepot = EntrepotSerializer(read_only=True)
    class Meta:
        model = Expedition
        fields = ["id", "order_id", "region", "date_commande", "transporteur", "entrepot", "date_expedition", "delai_prevu_jours", 
                    "delai_reel_jours", "ecart_jours", "statut_livraison", "en_retard", "cout_estime"]

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = ["id", "order_id", "date_commande", "statut", "segment_client", "marche", "region",
                "pays", "ville", "nb_articles", "montant_total", "profit_total"]
class CommandeDetailSerializer(CommandeSerializer):
    expedition = ExpeditionSerializer(read_only=True)
    class Meta(CommandeSerializer.Meta):
        fields = CommandeSerializer.Meta.fields + ["expedition"]
class EtlRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtlRun
        fields = "__all__"