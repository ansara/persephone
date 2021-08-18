import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

import { MongooseModule } from '@nestjs/mongoose';
import { ReportModule } from './report/report.module';
import { ThreadModule } from './thread/thread.module';

const mongoURL = 'mongodb://localhost/persephonedb'

@Module({
  imports: [MongooseModule.forRoot(mongoURL), ThreadModule, ReportModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}