import { Controller, Get, Param } from "@nestjs/common";
import { ThreadService } from "./thread.service";

@Controller('/threads')
export class ThreadController{
    constructor(private readonly threadService: ThreadService) {}

    @Get(':id')
    getThreadById(@Param('id') threadId: string){
        return this.threadService.getThreadById(threadId);
    }

    @Get(':location')
    getThreadsByLocation(@Param('location') location: string ){
        return this.threadService.getThreadsByLocation(location);
    }

    @Get(':date')
    getThreadsByDate(@Param('date') date: string){
        return this.threadService.getThreadsByDate(date);
    }

}