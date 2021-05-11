import { Component, OnInit } from '@angular/core';

import { ReportInputFileDto } from './utils/models/report-InputFile.dto';
import { ReportInputFileService } from './utils/services/report-input-file.service';
import { RoutingService } from '@app/core/services/Routing/routing.services';

@Component({
  selector: 'app-report-input-file',
  templateUrl: './report-input-file.component.html',
  styleUrls: ['./report-input-file.component.scss'],
})
export class ReportInputFileComponent implements OnInit {
  loading = true;
  reportInputFile: ReportInputFileDto[] = [];
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  constructor(private reportInputFileService: ReportInputFileService, private routingService: RoutingService) {}

  ngOnInit(): void {
    this.getReportInputFile();
  }

  // Routing
  goToDetail(event: any): void {
    console.log(event);
    this.routingService.navigateToUpdate('/daovan/', event.id);
  }

  getReportInputFile(): void {
    this.reportInputFileService.getJSON().subscribe((res: any) => {
      setTimeout(() => {
        this.loading = false;
        console.log(res);
        this.reportInputFile = res;
        for (var i = 0; i < this.reportInputFile.length; i++) {
          console.log(this.reportInputFile[i]);
        }
      }, 3000);
    });
  }

  //#region
  sort(sort: { key: string; value: string }): void {
    this.sortName = sort.key;
    this.sortValue = sort.value;
    this.search();
  }

  search(): void {
    // sort data
    if (this.sortName && this.sortValue) {
      this.displayData = this.reportInputFile.sort((a, b) =>
        this.sortValue === 'ascend'
          ? a[this.sortName] > b[this.sortName]
            ? 1
            : -1
          : b[this.sortName] > a[this.sortName]
          ? 1
          : -1
      );
    } else {
      this.displayData = this.reportInputFile;
    }
  }
  //#endregion
}
