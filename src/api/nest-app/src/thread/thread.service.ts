import { Injectable } from "@nestjs/common";

import { Thread } from "./thread.model";

@Injectable()
export class ThreadService{

    getThreadById(threadId: string){
        return 'ThreadID 12345'
    }

    getThreadsByLocation(location: string){
        return 'location not found'
    }

    getThreadsByDate(date: string){
        return 'no threads for date found'
    }

    //elasticsearch?
    getThreadByKeyword(keyword:string){
        return 'keyword not found'
    }

}