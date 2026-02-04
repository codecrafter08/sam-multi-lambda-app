from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db_models import EntityDispute

class EntityDisputeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityDispute
        fields = (
            "entityDisputeID",
            "entityDisputeFirstName",
            "entityDisputeLastName",
            "parentEntityID",
            "parentEntityInboundRecordNumber",
            "entityDisputeSource",
            "entityDisputeSubSource",
            "entityDisputeProduct",
            "entityDisputeInitialDataReceivedDate",
            "entityDisputeIsProcessed",
            "created_at",
            "entityDisputeOriginalSource",
            "entityDisputeOriginalSubSource"
        )
        include_fk = True
        load_instance = True 