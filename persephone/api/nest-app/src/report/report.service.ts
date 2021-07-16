import { Injectable } from "@nestjs/common";
import { InjectModel } from "@nestjs/mongoose";
import { Model } from 'mongoose';
import { Report } from "./report.model"


@Injectable()
export class ReportService{

    constructor(@InjectModel('Report') private readonly reportModel: Model<Report>){}

    async getReports(name: string, location: string){
        const reports = await this.reportModel.find({ extractedNames: name, threadLocation: location}).exec();
        return reports as Report[];
    }
}