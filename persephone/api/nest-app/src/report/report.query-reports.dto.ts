import { IsNotEmpty } from 'class-validator'

export class QueryReportsDto{

    // @ApiModelProperty()
    @IsNotEmpty()
    // @IsString()
    name: string;

    @IsNotEmpty()
    location: string;
}