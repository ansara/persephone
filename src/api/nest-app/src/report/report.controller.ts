import { Controller, Get, Param, Query } from "@nestjs/common";
// import { Query } from "mongoose";
import { ReportService } from "./report.service";
import { QueryReportsDto } from "./report.query-reports.dto";

@Controller('/report')
export class ReportController{
    constructor(private readonly reportService: ReportService){}

    @Get()
    async getReport(@Query() query: QueryReportsDto){
        const reports = await this.reportService.getReports(query.name, query.location);
        return reports;
    }
}