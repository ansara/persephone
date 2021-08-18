import { Module } from "@nestjs/common";
import { ThreadService } from "./thread.service";
import { ThreadController } from "./thread.controller";
import { MongooseModule } from "@nestjs/mongoose";

@Module({
    imports: [],
    controllers: [ThreadController],
    providers: [ThreadService],
  })
  export class ThreadModule {}