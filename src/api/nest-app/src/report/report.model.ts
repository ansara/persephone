import * as mongoose from 'mongoose';

export const ReportSchema = new mongoose.Schema({
    threadId: { type: String, required: true},
    threadLocation: { type: String, required: true},
    aggregateNames: Array,
    commentInferences: Array,
    dateProcessed: {type: String, required: true},
})

export interface Report {
    id: string;
    threadLocation: string;
    aggregateNames: Array<string>;
    commentInferences: Array<string>;
    dateProcessed: string;
}