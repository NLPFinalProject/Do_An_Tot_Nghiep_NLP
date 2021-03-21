import { BaseDto } from '@app/core/models/base.dto';

export class ReportInputFileDto extends BaseDto implements IReportInputFile {
  id: string;
  totalFile: number;
  createdBy: string;
  createdDate: string;
  expand: boolean;
  isActive: boolean;
  childReport: IChildReportInputFile;

  static fromJS(data: any): ReportInputFileDto {
    return this.fromJSON(ReportInputFileDto, data);
  }

  constructor(data?: IReportInputFile) {
    super();
    if (data) {
      for (const property in data) {
        if (data.hasOwnProperty(property)) {
          (<any>this)[property] = (<any>data)[property];
        }
      }
    }
  }

  clone(): ReportInputFileDto {
    const json = this.toJSON();
    const result = new ReportInputFileDto();
    result.init(json);
    return result;
  }
}

export interface IReportInputFile {
  id: string;
  totalFile: number;
  createdBy: string;
  createdDate: string;
  expand: boolean;
  isActive: boolean;
  childReport: IChildReportInputFile;
}

export interface IChildReportInputFile {
  id: string;
  name: string;
  totalFile: number;
}
