import json
from db_models import EntityDispute
from schema import EntityDisputeSchema
from utils import api_response

def getEntityDisputes(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session')
        query_params = kwargs.get('query_params', {})
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        # Get page number from query parameters, default to 1 if not provided
        page = int(query_params.get('page', 1))
        # Set page size to 50 as per requirement
        page_size = 50
        
        # Calculate offset
        offset = (page - 1) * page_size

        schema = EntityDisputeSchema(many=True)
        
        # Get total count of records
        total_records = db_session.query(EntityDispute).count()
        
        # Get paginated records
        disputes = db_session.query(EntityDispute)\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        data = schema.dump(disputes)
        
        # Calculate total pages
        total_pages = (total_records + page_size - 1) // page_size

        response_data.update({
            "success": True,
            "data": data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "page_size": page_size,
                "total_records": total_records
            },
            "message": "Entity disputes retrieved successfully"
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)} 