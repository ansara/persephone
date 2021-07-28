import * as mongoose from 'mongoose';

export const ReportSchema = new mongoose.Schema({
    threadLocation: { type: String, required: true},
    extractedNames: Array,
    extractedLocations: Array,
    datePosted: {type: String, required: true},
    dateProcessed: {type: String, required: true},
})

export interface Report {
    id: string;
    threadLocation: string;
    extractedNames: Array<string>;
    extractedLocations: Array<string>;
    datePosted: string;
    dateProcessed: string;
}