from handlers import getEmployeePayrollBonus, createEmployeePayrollBonus, getMasterPayrollPeriod, createMasterPayrollPeriod, updateMasterPayrollPeriod, getCommissionReports, deleteMasterPayrollPeriod, getSalesJobMilestoneDate
UUID_REGEX_PATTERN = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

available_methods = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
]

routes = {
    "GET": {
        "/payroll-bonus": getEmployeePayrollBonus,
        f"/master-payroll-period/?(?P<master_payroll_period_id>{UUID_REGEX_PATTERN})?/?$": getMasterPayrollPeriod,
        f"/payroll/commissions/?(?P<sales_job_id>{UUID_REGEX_PATTERN})?/?$": getCommissionReports,
        "/sales-job-milestone-date": getSalesJobMilestoneDate
     
    },
    "POST": {
        "/payroll-bonus": createEmployeePayrollBonus,
        "/master-payroll-period": createMasterPayrollPeriod,
    },
    "PATCH": {
        "/master-payroll-period": updateMasterPayrollPeriod
    },
    "DELETE" : {
        f"/master-payroll-period/?(?P<master_payroll_period_id>{UUID_REGEX_PATTERN})?/?$": deleteMasterPayrollPeriod,
    }
    
}
