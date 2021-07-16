import { IsNotEmpty } from 'class-validator'

export class QueryReportsDto{

    // @ApiModelProperty()
    // @IsString()

    @IsNotEmpty()
    name: string;

    @IsNotEmpty()
    location: string;
}