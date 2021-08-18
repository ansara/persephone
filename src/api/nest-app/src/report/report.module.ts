import { Module } from "@nestjs/common";
import { ReportService } from "./report.service";
import { ReportController } from "./report.controller";
import { ReportSchema } from "./report.model";
import { MongooseModule } from '@nestjs/mongoose';


@Module({
    imports: [MongooseModule.forFeature([{name: 'Report', schema: ReportSchema}])],
    controllers: [ReportController],
    providers: [ReportService],
})
export class ReportModule {}