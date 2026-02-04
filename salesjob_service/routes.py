from handlers import getSalesJobAddendum, getSalesJobCost, getSalesJobPayment, createSalesJobAddendum, createSalesJobCost, createSalesJobPayment
UUID_REGEX_PATTERN = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

available_methods = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
]

routes = {
    "GET": {
        "/sales-job-addendum": getSalesJobAddendum,
        "/sales-job-cost": getSalesJobCost,
        "/sales-job-payment": getSalesJobPayment
     
    },
    "POST": {
        "/sales-job-addendum": createSalesJobAddendum,
        "/sales-job-cost": createSalesJobCost,
        "/sales-job-payment": createSalesJobPayment
    },
    
}
