export class Thread {
    constructor(
        public id: string,
        public OriginalPostText: string,
        public OriginalPostDate: string,
        public OriginalPostImageInfo: string,
        public url: string,
        public location: string,
        public subject: string,
        public comments: Array<string>,
    ) {}
}