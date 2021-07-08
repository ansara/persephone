import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ThreadModule } from './thread/thread.module';

import { MongooseModule } from '@nestjs/mongoose';

const mongoURL = 'mongodb://localhost/persephonedb'

@Module({
  imports: [MongooseModule.forRoot(mongoURL), ThreadModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}