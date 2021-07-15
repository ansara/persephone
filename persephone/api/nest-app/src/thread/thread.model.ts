export class Thread {
    constructor(
        public id: string,
        public originalPostText: string,
        public originalPostDate: string,
        public originalPostImageInfo: string,
        public url: string,
        public location: string,
        public subject: string,
        public comments: Array<string>,
    ) {}
}