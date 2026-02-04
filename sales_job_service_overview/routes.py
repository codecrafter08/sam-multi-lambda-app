from handlers import (getSalesJobs, getSalesJobById, getSalesJobAddendumList, getPayrollAddendumList, rejectSalesJobAddendum)
UUID_REGEX_PATTERN = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
INTEGER_REGEX_PATTERN = "[0-9]{0,}"
available_methods = [
    "GET",
    "DELETE"
]


routes = {
    "GET": {
        "/sales-jobs/?$": getSalesJobs,
        f"/sales-jobs/(?P<sales_job_id>{UUID_REGEX_PATTERN})/?$": getSalesJobById,
        "/sales-jobs/addendum/list/?$": getSalesJobAddendumList,
        "/sales-jobs/addendum/payroll/?$": getPayrollAddendumList,
    },
    "DELETE": {
        f"/sales-jobs/addendum/(?P<addendum_id>{UUID_REGEX_PATTERN})/?$": rejectSalesJobAddendum,
    }
} 